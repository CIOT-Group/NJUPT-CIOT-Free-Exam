import os
import torch
import argparse
from omegaconf import OmegaConf
from pytorch_lightning import Trainer, LightningModule, seed_everything
from pytorch_lightning.callbacks import ModelCheckpoint, TQDMProgressBar, EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.strategies.ddp import DDPStrategy
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from torch.optim.lr_scheduler import ExponentialLR
from sklearn.metrics import accuracy_score
from model import CloudSentimentModel, FocalLoss
from preprocess import extract_bert_features

torch.set_float32_matmul_precision("high")


class FeatureDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


class CloudSentimentModelLightning(LightningModule):
    def __init__(self, model: CloudSentimentModel, lr=1e-4, weight_decay=0.01, lr_decay=0.95, gamma=2):
        super(CloudSentimentModelLightning, self).__init__()
        self.strict_loading = False
        self.model = model
        self.lr = lr
        self.weight_decay = weight_decay
        self.lr_decay = lr_decay
        self.loss_fn = FocalLoss(gamma=gamma)

    def forward(self, features):
        return self.model(features)

    def training_step(self, batch, batch_idx):
        features, labels = batch
        logits, mu = self(features)
        loss = self.loss_fn(logits, labels)
        train_acc = accuracy_score(labels.cpu(), torch.argmax(logits, dim=1).cpu())
        current_lr = self.trainer.optimizers[0].param_groups[0]['lr']

        self.log("lr", current_lr, prog_bar=True, logger=True)
        self.log("train/loss", loss, prog_bar=False, logger=True)
        self.log("train/acc", train_acc, prog_bar=False, logger=True)
        self.log("train/mu_mean", mu.mean(), prog_bar=False, logger=True)
        self.log("train/mu_std", mu.std(), prog_bar=False, logger=True)

        return loss

    def validation_step(self, batch, batch_idx):
        features, labels = batch
        logits, mu = self(features)
        loss = self.loss_fn(logits, labels)
        preds = torch.argmax(logits, dim=1)
        acc = accuracy_score(labels.cpu(), preds.cpu())

        self.log("val_acc", acc, prog_bar=True, logger=True, rank_zero_only=True)
        self.log("val/loss", loss, prog_bar=True, logger=True, rank_zero_only=True)
        self.log("val/mu_mean", mu.mean(), prog_bar=False, logger=True)
        self.log("val/mu_std", mu.std(), prog_bar=False, logger=True)
        

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=self.lr, weight_decay=self.weight_decay)
        scheduler = ExponentialLR(optimizer, gamma=self.lr_decay)
        return {"optimizer": optimizer,"lr_scheduler": {"scheduler": scheduler,"interval": "epoch","frequency": 1}}


class CustomModelCheckpoint(ModelCheckpoint):
    def __init__(self, config, *args, **kwargs):
        super(CustomModelCheckpoint, self).__init__(*args, **kwargs)
        self.config = config

    def on_save_checkpoint(self, trainer, pl_module, checkpoint):
        checkpoint["config"] = config
        super().on_save_checkpoint(trainer, pl_module, checkpoint)


class LitProgressBar(TQDMProgressBar):
    def get_metrics(self, trainer, model):
        items = super().get_metrics(trainer, model)
        items.pop("v_num", None)
        return items


def train(config, model_path=None):
    seed_everything(config.seed, workers=True)

    train_features_path = os.path.join(config.exp_dir, config.exp_name, "train_features.pt")
    val_features_path = os.path.join(config.exp_dir, config.exp_name, "val_features.pt")
    features_info_path = os.path.join(config.exp_dir, config.exp_name, "features_info.pt")

    if (not os.path.exists(train_features_path) or not os.path.exists(val_features_path)
        or not os.path.exists(features_info_path)):
        extract_bert_features(config)
    else:
        print(f"Loading old features from {os.path.join(config.exp_dir, config.exp_name)}")

    train_data = torch.load(train_features_path)
    val_data = torch.load(val_features_path)
    feature_info = torch.load(features_info_path)
    print(f"Feature info: {feature_info}")

    train_features = train_data["features"]
    train_labels = train_data["labels"]
    val_features = val_data["features"]
    val_labels = val_data["labels"]
    hidden_size = feature_info["hidden_size"]
    config.model.hidden_size = hidden_size # 把BERT的hidden_size保存到配置文件中

    # 创建数据集和加载器
    train_ds = FeatureDataset(train_features, train_labels)
    val_ds = FeatureDataset(val_features, val_labels)

    train_loader = DataLoader(
        train_ds,
        batch_size=config.train.batch_size,
        shuffle=True,
        num_workers=config.data.num_workers,
        pin_memory=config.data.pin_memory,
        persistent_workers=config.data.persistent_workers if config.data.num_workers > 0 else False
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=config.train.batch_size,
        shuffle=False,
        num_workers=config.data.num_workers,
        pin_memory=config.data.pin_memory,
        persistent_workers=config.data.persistent_workers if config.data.num_workers > 0 else False
    )

    model = CloudSentimentModel(
        input_size=hidden_size,
        cloud_drop_num=config.model.cloud_drop_num,
        cloud_dim=config.model.cloud_dim,
        features=config.model.features,
        dropout=config.model.dropout,
        attention=config.model.attention,
        output_feature=len(config.model.labels)
    )

    lightning_model = CloudSentimentModelLightning(
        model,
        lr=config.train.lr,
        weight_decay=config.train.weight_decay,
        lr_decay=config.train.lr_decay,
        gamma=config.train.gamma
    )

    checkpoint_callback = CustomModelCheckpoint(
        config=config,
        monitor=config.train.monitor,
        dirpath=os.path.join(config.exp_dir, config.exp_name, "checkpoints"),
        filename=config.train.save_name,
        save_top_k=config.train.save_top_k,
        mode=config.train.mode,
        save_last=config.train.save_last,
        verbose=config.train.verbose,
    )

    early_stopping_callback = EarlyStopping(
        monitor=config.train.monitor,
        patience=config.train.patience,
        verbose=config.train.verbose,
        mode=config.train.mode
    )

    logger = TensorBoardLogger(
        name="logs",
        save_dir=os.path.join(config.exp_dir, config.exp_name),
        version=config.exp_version,
    )

    strategy = "auto"
    if len(config.train.devices) > 1:
        strategy = DDPStrategy(
            find_unused_parameters=True, 
            process_group_backend='gloo' if os.name == "nt" else 'nccl'
        )

    trainer = Trainer(
        accelerator="gpu" if torch.cuda.is_available() else "cpu",
        devices=config.train.devices,
        strategy=strategy,
        max_epochs=config.train.max_epochs,
        logger=logger,
        log_every_n_steps=config.train.log_every_n_steps,
        callbacks=[checkpoint_callback, early_stopping_callback, LitProgressBar()],
        default_root_dir=os.path.join(config.exp_dir, config.exp_name),
    )

    trainer.fit(lightning_model, train_loader, val_loader, ckpt_path=model_path)
    print("Training completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default="configs/config.yaml", help="Path to the config file")
    parser.add_argument("-m", "--model", type=str, default=None, help="Path to the model checkpoint file to resume training")
    args = parser.parse_args()

    os.environ["USE_LIBUV"] = "0"
    os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"
    config = OmegaConf.load(args.config)
    os.makedirs(os.path.join(config.exp_dir, config.exp_name), exist_ok=True)
    OmegaConf.save(config, os.path.join(config.exp_dir, config.exp_name, "config.yaml"))
    print(config)

    train(config, args.model)