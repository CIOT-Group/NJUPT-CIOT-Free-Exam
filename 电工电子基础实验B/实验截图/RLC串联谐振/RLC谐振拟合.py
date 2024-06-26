import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import curve_fit

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为雅黑

# 数据
x_data = np.array([2.0, 4.0, 6.08, 6.3, 6.6, 7.09, 7.4, 7.9, 8.28, 12, 16, 20])
y_data = np.array([0.20575, 0.3539, 1.06445, 1.21875, 1.43505, 1.55285, 1.49085, 1.22315, 1.0336, 0.3786, 0.24395, 0.18335])

# 定义拟合函数（Lorentzian 函数）
def lorentzian(x, A, x0, gamma, C):
    return A / (1 + ((x - x0) / gamma)**2) + C

# 使用curve_fit函数进行拟合
popt, pcov = curve_fit(lorentzian, x_data, y_data, p0=[1, 7, 1, 0])

# 绘制原始数据点
plt.scatter(x_data, y_data, label='Data')

# 绘制拟合曲线
x_fit = np.linspace(min(x_data), max(x_data), 100)
plt.plot(x_fit, lorentzian(x_fit, *popt), 'r-', label='Fit')

# 标记特定点及其数值
plt.annotate(f'f1(6.08, 1.06445)', xy=(6.08, 1.06445), xytext=(3.0, 1.0), arrowprops=dict(facecolor='black', arrowstyle='->'))
plt.annotate(f'f0(7.09, 1.55285)', xy=(7.09, 1.55285), xytext=(7.5, 1.55), arrowprops=dict(facecolor='black', arrowstyle='->'))
plt.annotate(f'f2(8.28, 1.03360)', xy=(8.28, 1.03360), xytext=(8.7, 1.0), arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.xlabel('频率 (f/kHz)')
plt.ylabel('电流 (I/mA)')
plt.title('RLC串联谐振曲线')
plt.grid(True)
plt.show()
