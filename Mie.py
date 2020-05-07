﻿import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib import rc

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
# mpl.rcParams['font.sans-serif'] = ['Times New Roman']
# mpl.rcParams['text.usetex'] = True

def generateData(alpha,rm,im =0.0,N_ta = 2**13-1):
    origin_path = os.getcwd()
    os.chdir(r"miedebye")
    exeName = "Mie_Calculation.exe"
    txtName = 'ParaMie.txt'

    Ta_min, Ta_max = 0,180
    with open(txtName,'w') as f1:
        f1.write('{}\n{:.3f}\t{:.3f}\n{}\t{:.2f}\t{:.2f}'
                .format(alpha,rm,im,N_ta,Ta_min,Ta_max))

    os.system(exeName)

    dataName = "ScatteringLightAngleDistribution.txt"
    # 如果本机默认不是utf8编码，这里需要encoding='gbk'，后面这个delimiter随便要不要
    data = pd.read_csv(dataName,sep ='\t',engine='python',encoding='gbk',delimiter='\s+')
    os.remove(dataName)
    os.chdir(origin_path)

    return data

def plotMie(alpha = 9000, rm = 1.7, im= 0.0, N_ta = 2**13-1, figsize=(15, 6)):
    data = generateData(alpha, rm, im, N_ta=N_ta)
    theta = data['ScatterAngle']
    theta = theta.to_numpy()
    i1, i2 = data['I1'], data['I2']
    i1, i2 = i1.to_numpy(), i2.to_numpy()
    fig = plt.figure(figsize=figsize)
    ax1 = plt.subplot(1, 1, 1)
    tick_dict = dict(direction='in', top=1, right=1, length=4, width=0.7, labelsize=15)
    ax1.tick_params(**tick_dict)
    plt.plot(theta, np.log(i1), theta, np.log(i2))

    # **************************************************************************
    xySize = 17
    plt.xlabel('Scattering Angle(deg)', fontproperties='Times New Roman', fontsize=xySize)
    plt.ylabel('Logarithm of scattering intensity (a.u.)', fontproperties='Times New Roman', fontsize=xySize)
    legend_dict = dict(family='Times New Roman', size=17)
    # ***************************************************************
    plt.legend(['$I_1$', '$I_2$'], prop=legend_dict)
    return fig

def plotMie_dop(alpha = 9000, rm = 1.7, im= 0.0, N_ta = 2**13-1, figsize=(20, 12)):

    data = generateData(alpha,rm,im, N_ta = N_ta)

    theta = data['ScatterAngle']
    theta = theta.to_numpy()
    i1, i2, DOP = data['I1'], data['I2'], data['DOP']
    i1,i2, DOP = i1.to_numpy(), i2.to_numpy(), DOP.to_numpy()
    fig = plt.figure(figsize=figsize)
    ax1 = plt.subplot(2,1,1)
    tick_dict = dict(direction='in', top=1, right=1, length=4, width=0.7, labelsize=15)
    ax1.tick_params(**tick_dict)
    plt.plot(theta,np.log(i1),theta,np.log(i2))

    #**************************************************************************
    xySize=17
    plt.xlabel('Scattering Angle(deg)',fontproperties = 'Times New Roman',fontsize=xySize)
    plt.ylabel('Logarithm of scattering intensity (a.u.)',fontproperties = 'Times New Roman',fontsize=xySize)
    legend_dict = dict(family='Times New Roman',size=17)
    #***************************************************************
    plt.legend(['$I_1$','$I_2$'],prop=legend_dict)

    ax2 = plt.subplot(2,1,2)
    ax2.tick_params(**tick_dict)
    plt.plot(theta,(DOP))
    plt.xlabel('Scattering Angle(deg)',fontproperties = 'Times New Roman',fontsize=xySize)
    plt.ylabel('DOP',fontproperties = 'Times New Roman',fontsize=xySize)

    # plt.show()
    return fig
    
if __name__ == '__main__':
    # alpha,rm,im = eval(input('please input alpha, rm, im \nFor example:1000,0.7,0.\n'))

    fig = plotMie_dop(alpha=1000, rm=0.7, im=0)
    # plt.show()
    fig.show()
