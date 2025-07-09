import torch
import torch.nn as nn
import torch.nn.functional as F


class CloudSentimentModel(nn.Module):
    def __init__(
        self,
        input_size: int,  # BERT特征维度
        cloud_drop_num: int = 512,  # 云滴采样数量
        cloud_dim: int = 1,  # 云模型维度
        features: list[int] = [128, 64],  # 分类器隐藏层维度
        dropout: float = 0.2,  # Dropout率
        attention: bool = False,  # 是否使用attention
        output_feature: int = 2,  # 输出类别数
    ):
        super(CloudSentimentModel, self).__init__()
        self.cloud_drop_num = cloud_drop_num
        self.cloud_dim = cloud_dim
        self.dropout = dropout
        self.features = features
        self.attention = attention
        self.output_feature = output_feature

        self.fc_ex = nn.Linear(input_size, cloud_dim)  # [B, cloud_dim]
        self.fc_en = nn.Sequential(
            nn.Linear(input_size, cloud_dim), 
            nn.Softplus()
        )  # [B, cloud_dim]
        self.fc_he = nn.Sequential(
            nn.Linear(input_size, cloud_dim), 
            nn.Softplus()
        )  # [B, cloud_dim]

        if self.attention:
            self.attn_q = nn.Linear(cloud_dim, cloud_dim)
            self.attn_k = nn.Linear(cloud_dim, cloud_dim)
            self.attn_v = nn.Linear(cloud_dim, cloud_dim)

        self.classifier = nn.Sequential()
        input_dim = cloud_drop_num * cloud_dim

        for i, feature_dim in enumerate(features[:-1]):
            self.classifier.add_module(f'linear_{i}', nn.Linear(input_dim, feature_dim))
            self.classifier.add_module(f'relu_{i}', nn.ReLU())
            if dropout > 0:
                self.classifier.add_module(f'dropout_{i}', nn.Dropout(dropout))
            input_dim = feature_dim

        self.classifier.add_module('output', nn.Linear(input_dim, self.output_feature))

    def forward(self, features):
        ex = self.fc_ex(features)  # [B, cloud_dim]
        en = self.fc_en(features)  # [B, cloud_dim]
        he = self.fc_he(features)  # [B, cloud_dim]

        device = next(self.parameters()).device
        B = ex.size(0)
        D = self.cloud_drop_num
        C = self.cloud_dim

        # 生成噪声
        noise1 = torch.randn(B, D, C).to(device)  # [B, D, C]
        noise2 = torch.randn(B, D, C).to(device)  # [B, D, C]

        # 云模型
        drops = ex.unsqueeze(1) + (en.unsqueeze(1) + he.unsqueeze(1) * noise1) * noise2  # [B, D, C]

        # 多维度隶属度
        mu = torch.exp(
            -((drops - ex.unsqueeze(1)) ** 2) / 
            (2 * (en.unsqueeze(1) ** 2 + 1e-6)) # 防止除0错误
        )  # [B, D, C]

        if self.attention:
            # Q, K, V: [B, D, C]
            Q = self.attn_q(mu)
            K = self.attn_k(mu)
            V = self.attn_v(mu)
            # (B, num_heads, seq_len, head_dim)
            Q = Q.unsqueeze(1)  # [B, 1, D, C]
            K = K.unsqueeze(1)  # [B, 1, D, C]
            V = V.unsqueeze(1)  # [B, 1, D, C]
            attn_out = F.scaled_dot_product_attention(Q, K, V)  # [B, 1, D, C]
            mu = attn_out.squeeze(1)  # [B, D, C]

        # 展平结果
        mu_flat = mu.view(B, -1)  # [B, D*C]

        return self.classifier(mu_flat), mu


class FocalLoss(nn.Module):
    def __init__(self, gamma=2):
        super().__init__()
        self.gamma = gamma
        self.ce = nn.CrossEntropyLoss()

    def forward(self, input, target):
        logp = F.log_softmax(input, dim=1)
        p = torch.exp(logp)
        loss = self.ce(input, target)
        modulating_factor = (1 - p[range(len(target)), target]) ** self.gamma
        return (modulating_factor * loss).mean()