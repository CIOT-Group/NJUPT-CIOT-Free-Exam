import torch
import os
import argparse
from omegaconf import OmegaConf
from transformers import BertTokenizer, BertModel
from model import CloudSentimentModel


def extract_bert_features(config, text, tokenizer, bert_model, max_length=128, device="cuda"):
    bert_model.eval()
    with torch.no_grad():
        encoded = tokenizer(
            text,
            max_length=max_length,
            padding=config["preprocess"]["padding"],
            truncation=config["preprocess"]["truncation"],
            return_tensors=config["preprocess"]["return_tensors"],
        )
        input_ids = encoded["input_ids"].to(device)
        attention_mask = encoded["attention_mask"].to(device)
        features = bert_model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:, 0, :]
    return features


def predict_single(model: CloudSentimentModel, features):
    model.eval()
    with torch.no_grad():
        logits, _ = model(features)
        pred = torch.argmax(logits, dim=1).item()
        probs = torch.softmax(logits, dim=1)
        uncertainty = 1.0 - probs.max(dim=1).values.item()
        return pred, uncertainty


def load_models(model_path, custom_config=None) -> tuple:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    checkpoint = torch.load(model_path, map_location=device, weights_only=False)
    state_dict = {k.replace("model.", ""): v for k, v in checkpoint["state_dict"].items()}

    if custom_config:
        config = OmegaConf.load(custom_config)
    else:
        config = checkpoint["config"]
    hidden_size = checkpoint["config"]["model"]["hidden_size"]

    print("Loading tokenizer and model...")
    try:
        if config.bert.download:
            tokenizer = BertTokenizer.from_pretrained(config.bert.model, cache_dir=config.bert.cache_dir)
            bert_model = BertModel.from_pretrained(config.bert.model, cache_dir=config.bert.cache_dir)
        else:
            assert os.path.exists(config.bert.model), f"Model path does not exist: {config.bert.model}"
            tokenizer = BertTokenizer.from_pretrained(config.bert.model)
            bert_model = BertModel.from_pretrained(config.bert.model)
    except: # compatible with old versions
        assert os.path.exists("pretrain/chinese-roberta-wwm-ext-large"), "Model path does not exist: pretrain/chinese-roberta-wwm-ext-large"
        tokenizer = BertTokenizer.from_pretrained("pretrain/chinese-roberta-wwm-ext-large")
        bert_model = BertModel.from_pretrained("pretrain/chinese-roberta-wwm-ext-large")
    bert_model = bert_model.to(device)

    model = CloudSentimentModel(
        input_size=hidden_size,
        cloud_drop_num=config.model.cloud_drop_num,
        cloud_dim=config.model.get("cloud_dim", 1),
        features=config.model.features,
        dropout=config.model.get("dropout", 0.2),
        attention=config.model.get("attention", False),
        output_feature=len(config.model.labels) if config.model.get("labels") else 2,
    )
    model.load_state_dict(state_dict)

    return model, tokenizer, bert_model, config, device


def predict(model, tokenizer, bert_model, config, text, max_length=128, device="cuda"):
    features = extract_bert_features(config, text, tokenizer, bert_model, max_length, device)
    pred, uncertainty = predict_single(model, features)
    return pred, uncertainty


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=str, help="Path to the model checkpoint")
    parser.add_argument("-t", "--text", type=str, default=None, help="Text to predict sentiment")
    parser.add_argument("--max_length", type=int, default=128, help="Maximum length of the input text")
    parser.add_argument("--config", type=str, default=None, help="Path to the custom config file")
    args = parser.parse_args()

    assert os.path.exists(args.model), f"Model checkpoint not found: {args.model}"

    model, tokenizer, bert_model, config, device = load_models(args.model, args.config)
    model.to(device)
    labels = config.model.labels if config.model.get("labels") else {0: "Negative", 1: "Positive"}

    if args.text:
        pred, uncertainty = predict(model, tokenizer, bert_model, config, args.text, args.max_length, device)
        print(f"[Input]: {args.text}")
        print(f"[Prediction]: {labels[pred]}, [Uncertainty]: {uncertainty}")
    else:
        try:
            while True:
                text = input(">>> ")
                if text:
                    pred, uncertainty = predict(model, tokenizer, bert_model, config, text, args.max_length, device)
                    print(f"Prediction: {labels[pred]}, Uncertainty: {uncertainty}")
        except KeyboardInterrupt:
            os._exit(0)