import numpy as np
import matplotlib.pyplot as plt

class GaussianCloudGenerator:
    def __init__(self, expectation, entropy, hyper_entropy, num_points=1000):
        self.expectation = expectation # ex
        self.entropy = entropy # en
        self.hyper_entropy = hyper_entropy # he
        self.num_points = num_points

    def generate(self):
        # 根据超熵生成熵的正态分布
        entropy_deviation = np.random.normal(self.entropy, self.hyper_entropy, self.num_points)

        # 根据熵生成正态分布的输入值
        x = np.random.normal(self.expectation, entropy_deviation, self.num_points)

        # 计算隶属度
        y = np.exp(-((x - self.expectation) ** 2) / (2 * (entropy_deviation ** 2)))

        return x, y

    def plot(self):
        x, y = self.generate()
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, alpha=0.5, s=10, color='red')
        plt.title("Gaussian Cloud Model")
        plt.xlabel("X")
        plt.ylabel("Membership Degree")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    expectation = 10  # 期待值
    entropy = 1      # 熵
    hyper_entropy = 0.1  # 超熵
    num_points = 1000  # 点的数量
    np.random.seed(1)  # 设置随机种子以确保可重复性

    cloud_generator = GaussianCloudGenerator(expectation, entropy, hyper_entropy, num_points)
    cloud_generator.plot()