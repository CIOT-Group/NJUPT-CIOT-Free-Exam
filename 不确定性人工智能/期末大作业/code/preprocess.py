import os
import torch
import pandas as pd
import numpy as np
from tqdm import tqdm
from transformers import BertTokenizer, BertModel
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, config):
        self.texts = texts
        self.tokenizer = tokenizer
        self.padding = config.preprocess.padding
        self.max_length = config.preprocess.max_length
        self.truncation = config.preprocess.truncation
        self.return_tensors = config.preprocess.return_tensors

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        # 确保文本是字符串类型
        text = self.texts[idx]
        if not isinstance(text, str):
            text = "" if text is None else str(text)

        encoded = self.tokenizer(
            text,
            padding=self.padding,
            truncation=self.truncation,
            max_length=self.max_length,
            return_tensors=self.return_tensors,
        )
        for k in encoded:
            encoded[k] = encoded[k].squeeze(0)
        return encoded, idx

def extract_bert_features(config):
    print("Loading data...")

    texts, labels = list(), list()
    for file in os.listdir(config.data.path):
        if file.endswith(".tsv"):
            data = pd.read_csv(os.path.join(config.data.path, file), sep="\t")
            texts.extend(data["text"].tolist())
            labels.extend(data["label"].tolist())
        elif file.endswith(".csv"):
            data = pd.read_csv(os.path.join(config.data.path, file))
            texts.extend(data["text"].tolist())
            labels.extend(data["label"].tolist())
        else:
            print(f"[WARNING] Unsupported file format: {file}. Only .tsv and .csv are supported.")

    print(f"Total samples: {len(texts)}")

    valid_samples = []
    for i, (text, label) in enumerate(zip(texts, labels)):
        if text is not None:  # 过滤None值
            if not isinstance(text, str):
                text = str(text)  # 转换非字符串为字符串
            valid_samples.append((text, label))

    if len(valid_samples) < len(texts):
        print(f"Filtered out {len(texts) - len(valid_samples)} invalid samples.")
        texts, labels = zip(*valid_samples)
        texts, labels = list(texts), list(labels)

    print(f"Valid samples: {len(texts)}")

    if config.data.train_ratio < 1.0:
        combined = list(zip(texts, labels))
        random_state = np.random.RandomState(config.seed)
        random_state.shuffle(combined)
        num_samples = int(len(combined) * config.data.train_ratio)
        combined = combined[:num_samples]
        texts, labels = zip(*combined)
        texts, labels = list(texts), list(labels)
        print(f"Using {len(texts)} samples for training and validation.")

    # 分割训练集和验证集
    X_train, X_val, y_train, y_val = train_test_split(texts, labels, test_size=config.data.val_size, random_state=config.seed)

    print("Loading tokenizer and bert model...")

    # 加载BERT tokenizer和模型
    if config.bert.download:
        tokenizer = BertTokenizer.from_pretrained(config.bert.model, cache_dir=config.bert.cache_dir)
        bert_model = BertModel.from_pretrained(config.bert.model, cache_dir=config.bert.cache_dir)
    else:
        assert os.path.exists(config.bert.model), f"Model path does not exist: {config.bert.model}"
        tokenizer = BertTokenizer.from_pretrained(config.bert.model)
        bert_model = BertModel.from_pretrained(config.bert.model)
    bert_model.eval().cuda()

    # 创建数据集和加载器
    train_ds = TextDataset(X_train, tokenizer, config)
    val_ds = TextDataset(X_val, tokenizer, config)

    train_loader = DataLoader(
        train_ds,
        batch_size=config.preprocess.batch_size,
        shuffle=False,
        num_workers=config.preprocess.num_workers,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=config.preprocess.batch_size,
        shuffle=False,
        num_workers=config.preprocess.num_workers,
        pin_memory=True
    )

    # 预处理并保存特征
    output_dir = os.path.join(config.exp_dir, config.exp_name)
    os.makedirs(output_dir, exist_ok=True)

    train_features = []
    train_processed_indices = []
    with torch.no_grad():
        for batch, indices in tqdm(train_loader, desc="Extracting train features"):
            input_ids = batch["input_ids"].cuda()
            attention_mask = batch["attention_mask"].cuda()
            try:
                outputs = bert_model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:, 0, :]
                train_features.append(outputs.cpu())
                train_processed_indices.extend(indices.tolist())
            except Exception as e:
                print(f"Error processing batch: {e}")
                continue

    if len(train_processed_indices) < len(X_train):
        print(f"Warning: Only processed {len(train_processed_indices)} out of {len(X_train)} training samples")
        # 只保留成功处理的样本标签
        y_train_filtered = [y_train[i] for i in train_processed_indices]
    else:
        y_train_filtered = y_train
    
    train_features = torch.cat(train_features, dim=0)
    torch.save({
        "features": train_features,
        "labels": torch.tensor(y_train_filtered, dtype=torch.long)
    }, os.path.join(output_dir, "train_features.pt"))

    print(f"Saving train features to: {os.path.join(output_dir, 'train_features.pt')}")

    val_features = []
    val_processed_indices = []
    with torch.no_grad():
        for batch, indices in tqdm(val_loader, desc="Extracting val features"):
            input_ids = batch["input_ids"].cuda()
            attention_mask = batch["attention_mask"].cuda()
            try:
                outputs = bert_model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:, 0, :]
                val_features.append(outputs.cpu())
                val_processed_indices.extend(indices.tolist())
            except Exception as e:
                print(f"Error processing batch: {e}")
                continue

    if len(val_processed_indices) < len(X_val):
        print(f"Warning: Only processed {len(val_processed_indices)} out of {len(X_val)} validation samples")
        # 只保留成功处理的样本标签
        y_val_filtered = [y_val[i] for i in val_processed_indices]
    else:
        y_val_filtered = y_val

    val_features = torch.cat(val_features, dim=0)
    torch.save({
        "features": val_features,
        "labels": torch.tensor(y_val_filtered, dtype=torch.long)
    }, os.path.join(output_dir, "val_features.pt"))

    print(f"Saving val features to: {os.path.join(output_dir, 'val_features.pt')}")

    info = {
        "hidden_size": train_features.size(1),
        "train_samples": len(train_features),
        "val_samples": len(val_features)
    }
    print(f"Feature info: {info}")
    torch.save(info, os.path.join(output_dir, "features_info.pt"))
    print(f"Saving feature info to: {os.path.join(output_dir, 'features_info.pt')}")