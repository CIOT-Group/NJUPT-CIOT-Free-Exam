import torch
import numpy as np
import matplotlib.pyplot as plt
import os
from torch import nn
from torch.nn import functional as F
from tensorflow.keras.datasets import mnist
from sklearn.metrics import *

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

rootpath=str(os.getcwd()).replace("\\", "/") 
path=rootpath + "/MNIST_data/mnist.npz"
print(path)
(X_train, y_train), (X_test, y_test) = mnist.load_data(path)

X_train = torch.from_numpy(X_train.reshape(-1, 1, 28, 28)) / 255
X_test = torch.from_numpy(X_test.reshape(-1, 1, 28, 28)) / 255
y_train = torch.from_numpy(y_train)
y_test = torch.from_numpy(y_test)

learning_rate = 0.001
batch_size = 64
n_epochs = 30
in_channels = 1
n_outputs = 10

train_ds = torch.utils.data.TensorDataset(X_train, y_train)
train_loader = torch.utils.data.DataLoader(dataset = train_ds, batch_size = batch_size, shuffle = True)
test_ds = torch.utils.data.TensorDataset(X_test, y_test)
test_loader = torch.utils.data.DataLoader(dataset = test_ds, batch_size = batch_size, shuffle = True)


class ConvolutionalNeuralNet(nn.Module):
    def __init__(self, in_channels = 1, n_outputs = 10):
        super(ConvolutionalNeuralNet, self).__init__()
        self.conv1 = nn.Conv2d(in_channels = in_channels, out_channels = 8, kernel_size = (3, 3), stride = (1, 1), padding = (1, 1)) # 28 -> 14
        self.conv2 = nn.Conv2d(in_channels = 8, out_channels = 16, kernel_size = (5, 5), stride = (1, 1), padding = (1, 1)) # 14 -> 7
        self.fc1 = nn.Linear(16 * 6 * 6, 10)
        self.pool = nn.MaxPool2d(kernel_size = (2, 2), stride = (2, 2))
        
    def forward(self, x):
        out = F.relu(self.conv1(x))
        out = self.pool(out)
        out = F.relu(self.conv2(out))
        out = self.pool(out)
        out = out.reshape(out.shape[0], -1)
        out = self.fc1(out)
        return out

# model - Convolutional
model = ConvolutionalNeuralNet().to(device)

# loss
critirion = nn.CrossEntropyLoss()

# optimizer
optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)


def predict(model, X_batch):
    X_batch = X_batch.to(device)
    y_pred = model(X_batch)
    return y_pred.max(dim = 1)[1]

def batch_accuracy(model, X_batch, y_batch):
    X_batch = X_batch.to(device)
    y_batch = y_batch.to(device)
    y_pred = predict(model, X_batch)
    return (y_pred == y_batch).sum() / batch_size

def val_accuracy(model, test_loader):
    sum = 0
    mx = 0
    for i, (samples, labels) in enumerate(test_loader):
        mx = max(mx, i)
        sum += batch_accuracy(model, samples, labels)
    return sum / (mx + 1)

for epoch in range(n_epochs):
    for i, (samples, labels) in enumerate(train_loader):
        
        samples = samples.to(device)
        labels = labels.to(device)
        predictions = model(samples)
        labels=labels.long()

        loss = critirion(predictions, labels)
        
        loss.backward()
        
        optimizer.step()
        optimizer.zero_grad()
    if (epoch + 1) % 1 == 0:
        print(f"epoch = {epoch + 1} | loss = {loss:.5f} | train accuracy = {val_accuracy(model, train_loader):.4f}  | val accuracy = {val_accuracy(model, test_loader):.4f}")



model.eval()
y_pred = predict(model, X_test).to('cpu')

print(f1_score(y_pred, y_test.to('cpu'), average = 'macro'))
CM = confusion_matrix(y_pred, y_test.to('cpu'))
print(CM)

p = np.random.randint(1, 10000)
plt.imshow(X_test[p].reshape(28, 28), cmap = 'Blues')
plt.title(f"predicted: {y_pred[p]} | True: {y_test[p]}")
plt.show()

