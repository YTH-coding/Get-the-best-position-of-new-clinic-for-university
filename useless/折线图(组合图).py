import math
import numpy as np
import matplotlib.pylab as plt

plt.rcParams['font.sans-serif'] = ['SimHei'] #中文显示设置

#碳酸和草酸的一些数据     
pk1_h2c2o4 = 1.20
pk2_h2c2o4 = 4.20
pk1_h2co3 = 6.38
pk2_h2co3 = 10.25

k1c2 = math.pow(10, -pk1_h2c2o4)
k2c2 = math.pow(10, -pk2_h2c2o4)
k1c1 = math.pow(10, -pk1_h2co3)
k2c1 = math.pow(10, -pk2_h2co3)

kw = math.pow(10,-14)

def concentration(c1, c2):
    c_h2c2o4 = c1
    c_h2co3 = c2

    #以下是用于得到6次方程的系数的代码
    m1 = np.array([[k1c1*k2c1, k1c1, 1.]])
    m1_pow = np.array([[math.pow(math.e, 0), math.pow(math.e, 1), math.pow(math.e, 2)]])

    m1o = np.array([[k1c1, 2.]])
    m1o_pow = np.array([[math.pow(math.e, 1), math.pow(math.e, 2)]])

    m2 = np.array([[k1c2*k2c2, k1c2, 1.]])
    m2_pow = np.array([[math.pow(math.e, 0), math.pow(math.e, 1), math.pow(math.e, 2)]])

    m2o = np.array([[k1c2, 2.*k1c2*k2c2]])
    m2o_pow = np.array([[math.pow(math.e, 1), math.pow(math.e, 0)]])

    result1 = m1.T @ m2
    result1_pow = np.log(m1_pow.T @ m2_pow * math.pow(math.e, 2))

    result2 = m1o.T @ m2 * c_h2co3
    result2_pow = np.log(m1o_pow.T @ m2_pow * math.pow(math.e, 1))

    result3 = m1.T @ m2 * kw
    result3_pow = np.log(m1_pow.T @ m2_pow)

    result4 = m2o.T @ m1 * c_h2c2o4
    result4_pow = np.log(m2o_pow.T @ m1_pow * math.pow(math.e, 1))

    #得到的系数存储在列表number里面
    number = [0., 0., 0., 0., 0., 0., 0.]
    def count(matrix, matrix_pow, a):
        for i in range(len(matrix_pow)):
            for j in range(len(matrix_pow[0])):
                index = int(matrix_pow[i][j])
                number[6-index] += matrix[i][j]*math.pow(-1,a)

    count(result1,result1_pow, 0)
    count(result2,result2_pow, 0)
    count(result3,result3_pow, 1)
    count(result4,result4_pow, 1)

    roots = np.roots(number) #得到系数，用roots函数会得到6个解，选那个正的

    for i in range(6):
        if roots[i]>0:
            return -math.log10(roots[i]) #函数返回值在这里

if __name__ == "__main__":

    f = [0.01*i for i in range(1,201)] # 比例选取：0~2
    pH = [concentration(i*0.1, 0.1) for i in f] # pH计算

    #这是f = 0.2那条竖线
    max_pH = max(pH)
    min_pH = min(pH)
    f1 = [0.2 for i in range(101)]
    pH1 = [min_pH+(max_pH-min_pH)/100*i for i in range(101)]

    #绘制图1：曲线图.png
    plt.figure(figsize=(6, 10))
    plt.plot(f,pH)
    plt.scatter(f1,pH1,s=1,c="gray",marker=".")
    plt.title(r'$pH-\frac{n(H_2C_2O_4)}{n(Na_2CO_3)}$曲线图',x=0.5, y=1.025)
    plt.xlabel(r'$f = \frac{n(H_2C_2O_4)}{n(Na_2CO_3)}$')
    plt.ylabel("pH")
    plt.savefig("曲线图.png", dpi=600)
    plt.show()


    #绘制图2：数据整合.png（整合了4个图）
    ##co3_\delta，子图1
    H = [math.pow(10,-i) for i in pH]
    delta0 = [(k1c1*k2c1)/(k1c1*k2c1+k1c1*H[i]+H[i]*H[i]) for i in range(0,200)]
    delta1 = [(k1c1*H[i])/(k1c1*k2c1+k1c1*H[i]+H[i]*H[i]) for i in range(0,200)]
    delta2 = [(H[i]*H[i])/(k1c1*k2c1+k1c1*H[i]+H[i]*H[i]) for i in range(0,200)]

    plt.figure(figsize=(15, 9))
    plt.subplot(2, 2, 1)
    plt.plot(f, delta0, label = r"$\delta 0$")
    plt.plot(f, delta1, label = r"$\delta 1$")
    plt.plot(f, delta2, label = r"$\delta 2$")
    plt.title(r"碳酸类$\delta - f$",x=0, y=1.025)
    plt.xlabel(r'$f = \frac{n(H_2C_2O_4)}{n(Na_2CO_3)}$')
    plt.ylabel(r"分布分数$\delta$(%)")
    plt.legend()

    ##co3_c，子图2
    delta0 = [0.1*i for i in delta0]
    delta1 = [0.1*i for i in delta1]
    delta2 = [0.1*i for i in delta2]

    plt.subplot(2, 2, 2)
    plt.plot(f, delta0, label = r"$CO_3^{2-}$")
    plt.plot(f, delta1, label = r"$HCO_3^-$")
    plt.plot(f, delta2, label = r"$H_2CO_3$")
    plt.title(r"碳酸类$c - f$",x=0, y=1.025)
    plt.xlabel(r'$f = \frac{n(H_2C_2O_4)}{n(Na_2CO_3)}$')
    plt.ylabel(r"浓度$c(mol/L)$")
    plt.legend()

    ##c2o4_\delta，子图3
    delta0 = [(k1c2*k2c2)/(k1c2*k2c2+k1c2*H[i]+H[i]*H[i]) for i in range(0,200)]
    delta1 = [(k1c2*H[i])/(k1c2*k2c2+k1c2*H[i]+H[i]*H[i]) for i in range(0,200)]
    delta2 = [(H[i]*H[i])/(k1c2*k2c2+k1c2*H[i]+H[i]*H[i]) for i in range(0,200)]

    plt.subplot(2, 2, 3)
    plt.plot(f, delta0, label = r"$\delta 0$")
    plt.plot(f, delta1, label = r"$\delta 1$")
    plt.plot(f, delta2, label = r"$\delta 2$")
    plt.title(r"草酸类$\delta - f$",x=0, y=1.025)
    plt.xlabel(r'$f = \frac{n(H_2C_2O_4)}{n(Na_2CO_3)}$')
    plt.ylabel(r"分布分数$\delta$(%)")
    plt.legend()

    ##c2o4_c，子图4
    delta0 = [(k1c2*k2c2)/(k1c2*k2c2+k1c2*H[i]+H[i]*H[i])*f[i]*0.1 for i in range(0,200)]
    delta1 = [(k1c2*H[i])/(k1c2*k2c2+k1c2*H[i]+H[i]*H[i])*f[i]*0.1 for i in range(0,200)]
    delta2 = [(H[i]*H[i])/(k1c2*k2c2+k1c2*H[i]+H[i]*H[i])*f[i]*0.1 for i in range(0,200)]

    plt.subplot(2, 2, 4)
    plt.plot(f, delta0, label = r"$C_2O_4^{2-}$")
    plt.plot(f, delta1, label = r"$HC_2O_4^-$")
    plt.plot(f, delta2, label = r"$H_2C_2O_4$")
    plt.title(r"草酸类$c - f$",x=0, y=1.025)
    plt.xlabel(r'$f = \frac{n(H_2C_2O_4)}{n(Na_2CO_3)}$')
    plt.ylabel(r"浓度$c$(mol/L)")
    plt.legend()

    plt.tight_layout(h_pad=0.5) #子图垂直间隔
    plt.savefig("数据整合.png", dpi=600)
    plt.show()