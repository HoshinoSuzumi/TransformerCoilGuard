import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

# 采样点选择1400个，因为设置的信号频率分量最高为600赫兹，根据采样定理知采样频率要大于信号频率2倍，所以这里设置采样频率为1400赫兹（即一秒内有1400个采样点，一样意思的）
x = np.linspace(0, 1, 1400)

# xx = [-1.3307264053722179, -1.1825933274806744, -1.0122402879053993, -0.8246050559094442, -0.6567209009656949,
#       -0.4197079763392253, -0.1851639363442814, 0.08888225775507408, 0.31108187459238934, 0.565376991639539,
#       0.7554811082670199, 0.9480541095260264, 1.0838427642599413, 1.2146936497308047, 1.293697957939628,
#       1.3677644968853997, 1.409735535621337, 1.4245488434104914, 1.4122044202528627, 1.3776400354115026,
#       1.3060423810972566, 1.2097558804677533, 1.1011249566806214, 0.9085519554216148, 0.6320368766907336,
#       0.42958833690562415, 0.25429752806729766, 0.05431787291371393, -0.09875297424088103, -0.2616993599215789,
#       -0.41723909170769957, -0.5999365544406032, -0.8122606327518156, -0.9752070184325135, -1.0986512500087997,
#       -1.239377674005766, -1.3183819822145892, -1.3726974441081552, -1.3998551750549382, -1.4072618289495153,
#       -1.4072618289495153, -1.3973862904234124, -1.3801040980027324, -1.348008597792898, -1.3085064436884863,
#       -1.2739420588471262, -1.2369087893742403, -1.1850622121122, -1.1208712116925312, -1.0640868651674396,
#       -1.0073025186423479, -0.9332359796965761, -0.8641072100138558, -0.7949784403311355, -0.7085674782277351,
#       -0.6246254007558605, -0.5530277464416145, -0.4369901687599054, -0.350579206656505, -0.2715748984476818,
#       -0.18763282097580714, -0.07406412792562378, 0.034566795861508126, 0.11603998870185706, 0.1999820661737317,
#       0.28392414364560636, 0.3653973364859553, 0.48884156806224155, 0.5752525301656419, 0.6789456846897224,
#       0.7480744543724427, 0.8295476472127916, 0.9036141861585634, 0.9924940328934895, 1.0468094947870554,
#       1.1011249566806214, 1.167784841731816, 1.229506957519959, 1.283822419413525]

# 设置需要采样的信号，频率分量有180，390和600

y = 7 * np.sin(2 * np.pi * 180 * x) + 2.8 * np.sin(2 * np.pi * 390 * x) + 5.1 * np.sin(2 * np.pi * 600 * x)

# yy = fft(y)  # 快速傅里叶变换
# yreal = yy.real  # 获取实数部分
# yimag = yy.imag  # 获取虚数部分

yf = abs(fft(y))  # 取绝对值
yf1 = abs(fft(y)) / len(x)  # 归一化处理
yf2 = yf1[range(int(len(x) / 2))]  # 由于对称性，只取一半区间

xf = np.arange(len(y))  # 频率
xf1 = xf
xf2 = xf[range(int(len(x) / 2))]  # 取一半区间

plt.subplot(221)
plt.plot(x[0:50], y[0:50])
plt.title('Original wave')

plt.subplot(222)
plt.plot(xf, yf, 'r')
plt.title('FFT of Mixed wave(two sides frequency range)', fontsize=7, color='#7A378B')  # 注意这里的颜色可以查询颜色代码表

plt.subplot(223)
plt.plot(xf1, yf1, 'g')
plt.title('FFT of Mixed wave(normalization)', fontsize=9, color='r')

plt.subplot(224)
plt.plot(xf2, yf2, 'b')
plt.title('FFT of Mixed wave)', fontsize=10, color='#F08080')

plt.show()