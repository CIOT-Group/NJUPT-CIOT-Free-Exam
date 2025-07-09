import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

class CloudParameterNetwork(nn.Module):
    def __init__(self):
        super(CloudParameterNetwork, self).__init__()
        # [N, 2] -> [ex, en, he]
        self.network = nn.Sequential(
            nn.Linear(2, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 3)
        )
        self.softplus = nn.Softplus() # 确保为正数

    def forward(self, x):
        output = self.network(x)
        expectation = output[:, 0] # ex
        entropy = self.softplus(output[:, 1]) + 1e-6 # en, he > 0
        hyper_entropy = self.softplus(output[:, 2]) + 1e-6 # 防止为0
        return expectation, entropy, hyper_entropy


class InverseCloudGenerator:
    def __init__(self, device='cpu'):
        self.device = device
        self.model = CloudParameterNetwork().to(device)
        
    def calculate_membership(self, x, expectation, entropy):
        return torch.exp(-((x - expectation) ** 2) / (2 * (entropy ** 2))) # 隶属度

    def train(self, cloud_points, epochs=10000, lr=1e-3, decay=1e-4) -> CloudParameterNetwork:
        # cloud_points: [N, 2]
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        scheduler = None
        if decay > 0:
            scheduler = optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda epoch: (1 - decay) ** epoch)

        if not isinstance(cloud_points, torch.Tensor):
            cloud_points = torch.tensor(cloud_points, dtype=torch.float32).to(self.device)

        x_values = cloud_points[:, 0] # x
        y_true = cloud_points[:, 1] # y

        for epoch in range(epochs):
            optimizer.zero_grad()
            expectation, entropy, _ = self.model(cloud_points)

            # 计算预测的隶属度
            y_pred = self.calculate_membership(x_values, expectation, entropy)

            # 计算损失（均方误差）
            loss = torch.mean((y_pred - y_true) ** 2)

            loss.backward()
            optimizer.step()
            if scheduler:
                scheduler.step()

            if epoch % 500 == 0:
                current_lr = optimizer.param_groups[0]['lr']
                print(f'Epoch {epoch}, Loss: {loss.item()}, LR: {current_lr:.6f}')

        return self.model


    def infer_parameters(self, cloud_points):
        # cloud_points: [N, 2]
        if not isinstance(cloud_points, torch.Tensor):
            cloud_points = torch.tensor(cloud_points, dtype=torch.float32).to(self.device)

        self.model.eval()
        with torch.no_grad():
            expectation, entropy, hyper_entropy = self.model(cloud_points)
            return (expectation.mean().item(), entropy.mean().item(), hyper_entropy.mean().item()) # ex, en, he


    def generate_cloud_from_parameters(self, params, num_points=1000):
        # params: (ex, en, he)
        expectation, entropy, hyper_entropy = params

        # 确保熵和超熵为正值
        entropy = abs(entropy)
        hyper_entropy = abs(hyper_entropy)

        # 根据超熵生成熵的正态分布
        entropy_values = np.random.normal(entropy, hyper_entropy, num_points)

        # 确保所有熵值都为正
        entropy_values = np.abs(entropy_values)

        # 生成输入值
        x = np.random.normal(expectation, entropy_values)

        # 计算隶属度
        y = np.exp(-((x - expectation) ** 2) / (2 * (entropy_values ** 2)))

        return x, y # (x, y)


    def plot_comparison(self, original_points, inferred_params):
        # 原始点
        x_original, y_original = zip(*original_points)

        # 生成反推云模型的点
        x_inferred, y_inferred = self.generate_cloud_from_parameters(inferred_params, 1000)
        plt.figure(figsize=(12, 6))

        # 绘制原始点
        plt.scatter(x_original, y_original, alpha=0.6, label='Original Points', color='blue')
        # 绘制反推的云模型点
        plt.scatter(x_inferred, y_inferred, alpha=0.3, label='Inferred Model', color='red')

        plt.title('Comparison of Original Points and Inferred Cloud Model')
        plt.xlabel('X')
        plt.ylabel('Membership Degree')
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    # 设置随机种子
    torch.manual_seed(1)
    np.random.seed(1)

    # 生成云点数据
    def generate_sample_cloud_points(expectation=5, entropy=1, hyper_entropy=0.1, num_points=500):
        entropy_values = np.random.normal(entropy, hyper_entropy, num_points)
        x = np.random.normal(expectation, entropy_values)
        y = np.exp(-((x - expectation) ** 2) / (2 * (entropy_values ** 2)))
        return list(zip(x, y))

    # 生成示例数据，真实参数(5, 1, 0.1)
    cloud_points = generate_sample_cloud_points(5, 1, 0.1, 500)

    # 创建逆向云发生器并训练
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    inverse_generator = InverseCloudGenerator(device)
    inverse_generator.train(cloud_points, epochs=5000)

    # 推断云模型参数
    inferred_params = inverse_generator.infer_parameters(cloud_points)
    print(f"推断的参数: 期望值={inferred_params[0]:.4f}, 熵={inferred_params[1]:.4f}, 超熵={inferred_params[2]:.4f}")

    # 绘制对比图
    inverse_generator.plot_comparison(cloud_points, inferred_params)