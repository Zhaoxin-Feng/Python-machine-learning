# 导入必要的库
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from scipy import stats
import scipy.io as scio
import matplotlib.font_manager as mfm
from matplotlib import style

mu1_array = []
mu2_array = []
sigma1_array = []
sigma2_array = []
w1_array = []
w2_array = []

# EM算法的实现
def em(h, mu1, sigma1, w1, mu2, sigma2, w2, time):
    '''
    h为输入的数据
    mu1，sigma1,w1分别为A的初始均值，方差，权重
    mu2，sigma2,w2分别为B的初始均值，方差，权重
    time代表迭代次数
    '''
    for i in range(time):
        # 计算响应，E-step
        r1, r2 = E(myData, mu1, sigma1, w1, mu2, sigma2, w2)
        # mu、sigmal、w的更新，M-step
        mu1, sigma1, w1, mu2, sigma2, w2 = M(myData, mu1, mu2, r1, r2)
    return mu1, sigma1, w1, mu2, sigma2, w2

def Gauss(myData, mu, sigma):
    P = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-1 * np.square(myData - mu) / (2 * np.square(sigma)))
    return P

def E(myData, mu1, sigma1, w1, mu2, sigma2, w2):
    # 计算响应度
    r1 = w1 * Gauss(myData, mu1, sigma1)
    r2 = w2 * Gauss(myData, mu2, sigma2)
    # 归一化
    sum = r1 + r2
    r1 = r1 / sum
    r2 = r2 / sum
    return r1, r2

def M(myData, mu1_old, mu2_old, r1, r2):
    # 更新参数mu
    mu1_new = np.dot(r1, myData) / np.sum(r1)
    mu2_new = np.dot(r2, myData) / np.sum(r2)
    global mu1_array
    mu1_array.append(mu1_new)
    global mu2_array
    mu2_array.append(mu2_new)
    # 更新参数sigma
    sigma1_new = np.sqrt(np.dot(r1, np.square(myData - mu1_old)) / np.sum(r1))
    sigma2_new = np.sqrt(np.dot(r2, np.square(myData - mu2_old)) / np.sum(r2))
    global sigma1_array
    sigma1_array.append(sigma1_new)
    global sigma2_array
    sigma2_array.append(sigma2_new)
    # 更新参数w
    m = len(myData)
    w1_new = np.sum(r1) / m
    w2_new = np.sum(r2) / m
    global w1_array
    w1_array.append(w1_new)
    global w2_array
    w2_array.append(w2_new)
    return mu1_new, sigma1_new, w1_new, mu2_new, sigma2_new, w2_new

# GMM的构造
# Step 1.首先根据经验来分别对A,B班级的均值、方差和权值进行初始化,如：
mu1 = 77
sigma1 = 5
w1 = 0.5  # A
mu2 = 75
sigma2 = 6
w2 = 0.5  # B

# 加载数据
myDataFile = 'Data.mat'
h = scio.loadmat(myDataFile)
myData = []
for i in range(0, 200):
    for j in range(0, 10):
        myData.append(h['C'][i][j])
myData = np.array(myData)

# 开始EM算法的主循环
final_mu1, final_sigma1, final_w1, final_mu2, final_sigma2, final_w2 = em(myData, mu1, sigma1, w1, mu2, sigma2, w2, 100)
print('均值1:', final_mu1, '方差1:', final_sigma1, '权重1:', final_w1, '均值2:', final_mu2, '方差2:', final_sigma2, '权重2:', final_w2)
# 作图
# 直方图
style.use('ggplot')  # 加载'ggplot'风格
plt.rcParams['font.family'] = 'SimHei'
plt.bar(range(len(myData)), myData)
plt.title('柱图')
plt.savefig("柱图.png", dpi=700)
plt.show()

#Python绘制正态分布曲线
u1 = final_mu1  # 第一个高斯分布的均值
sigma1 = final_sigma1  # 第一个高斯分布的标准差
u2 = final_mu2  # 第二个高斯分布的均值
sigma2 = final_sigma2  # 第二个高斯分布的标准差
x = np.arange(65, 95, 1)
# 表示第一个高斯分布函数
y1 = np.multiply(np.power(np.sqrt(2 * np.pi) * sigma1, -1), np.exp(-np.power(x - u1, 2) / 2 * sigma1 ** 2))
# 表示第二个高斯分布函数
y2 = np.multiply(np.power(np.sqrt(2 * np.pi) * sigma2, -1), np.exp(-np.power(x - u2, 2) / 2 * sigma2 ** 2))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决pythonmatplotlib绘图无法显示中文的问题
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.subplot(121)
plt.plot(x, y1, 'b-', linewidth=2)
plt.title("高斯分布函数图像A")
plt.subplot(122)
plt.plot(x, y2, 'r-', linewidth=2)
plt.title('高斯分布函数图像B')
plt.show()
# 参数更新
# 模型1的均值
plt.plot(np.arange(1,101), mu1_array, linestyle='none', marker='o')
plt.title("模型1的均值")
plt.show()
# 模型2的均值
plt.plot(np.arange(1,101), mu2_array, linestyle='none', marker='o')
plt.title("模型2的均值")
plt.show()
# # 模型1的标准差
plt.plot(np.arange(1,101), sigma1_array, linestyle='none', marker='o')
plt.title("模型1的标准差")
plt.show()
# # 模型2的标准差
plt.plot(np.arange(1,101), sigma2_array, linestyle='none', marker='o')
plt.title("模型2的标准差")
plt.show()
# # 模型1的权值
plt.plot(np.arange(1,101), w1_array, linestyle='none', marker='o')
plt.title("模型1的权值")
plt.show()
# # 模型2的均值
plt.plot(np.arange(1,101), w2_array, linestyle='none', marker='o')
plt.title("模型2的均值")
plt.show()
