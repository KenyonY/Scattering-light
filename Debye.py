import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# plt.rcParams['font.sans-serif'] = ['Times New Roman']
# plt.rcParams['text.usetex'] = True

def generateData(alpha,rm,p1,p2,im =0.0,N_ta = 2**13-1):
    '''
    生成p1——p2阶分波叠加分布，p1 <0绘制总光强
    '''
    origin_path = os.getcwd()
    os.chdir("./miedebye")
    exeName = "debye.exe"
    txtName = 'Parameter_in.txt'

    Ta_min, Ta_max = 0,180
    with open(txtName,'w') as f1:
        f1.write('{}\n{:.6f}\t{:.5f}\n{}\t{:.2f}\t{:.2f}\n{}\t{}'
                .format(alpha,rm,im,N_ta,Ta_min,Ta_max,p1,p2))

    os.system(exeName)

    dataName = "DebyeSeris,p={:.0f},m={:.6f},a={:.2f}.txt".format(p1,rm,alpha)
    # c写出来的不是utf-8编码的，所以这里encoding='gbk'，后面这个delimiter随便要不要
    data = pd.read_csv(dataName,sep ='\t',encoding='gbk',delimiter='\s+')
    os.remove(dataName)
    os.chdir(origin_path)
    return data

def superposition_intensity(alpha=2000, rm=1.7, im=0., p=[0, 1], N_ta=2 ** 13 - 1):
    """Return tuple(theta, i1, i2)"""
    Rs1, Is1, Rs2, Is2 = 0, 0, 0, 0

    N = len(p)

    for i in range(N):
        data = generateData(alpha, rm, p1=p[i], p2=p[i], im=im, N_ta=N_ta)
        theta = data['ScatteringAngle']
        theta = theta.to_numpy()
        #    i1, i2 = data['I1'], data['I2']
        #    i1,i2 = i1.to_numpy(), i2.to_numpy()

        rs1, is1, rs2, is2 = data['rs1'], data['is1'], data['rs2'], data['is2']
        rs1, is1, rs2, is2 = rs1.to_numpy(), is1.to_numpy(), rs2.to_numpy(), is2.to_numpy()
        Rs1 += rs1
        Is1 += is1
        Rs2 += rs2
        Is2 += is2

    i1 = Rs1 * Rs1 + Is1 * Is1
    i2 = Rs2 * Rs2 + Is2 * Is2
    return theta,i1, i2

def plot_debye(alpha=2000, rm=1.7, im=0.0, p=[0, 1], N_ta=2 ** 13 - 1, figsize=(15, 6),
               show_critial_angle=True, show_brewster_angle=True):

    theta, i1, i2 = superposition_intensity(alpha, rm, im, p, N_ta)
    fig = plt.figure(figsize=figsize)
    xySize = 17

    major_tick_dict = dict(which='major', direction='in', top=0, right=0, length=6, width=0.7, labelsize=15)
    minor_tick_dict = dict(which='minor', direction='in', top=0, right=0, length=3, width=0.7, labelsize=15)

    ax = plt.subplot(1, 1, 1)  # 两行一列第二个(N=2)
    # y1 = np.log(i1)
    # y2 = np.log(i2)
    # plt.plot(theta, y1, theta, y2)
    plt.semilogy(theta, i1, theta, i2)
    plt.xlabel('Scattering Angle(deg)', fontproperties='Times New Roman', fontsize=xySize)
    plt.ylabel('Scattering intensity (a.u.)', fontproperties='Times New Roman', fontsize=xySize)

    legend_dict = dict(family='Times New Roman', size=17)
    
    plt.minorticks_on()
    ax.tick_params(**major_tick_dict)
    ax.tick_params(**minor_tick_dict)
    plt.legend(['$I_1$', '$I_2$'], prop=legend_dict)
    p_name = []
    for pi in p:
        p_name.append(f'$p_{{{pi}}}$ ')
    #     plt.title('The superposition of {}'.format(''.join(p_name)), fontsize=xySize)
    plt.text(70, max(i1.max(), i2.max())**(4/5), f'The superposition of {p_name[0]}and {p_name[1]}', fontsize=17)
    if show_critial_angle:
        theta_c = np.degrees(np.pi - 2 * np.arcsin(rm))
        plt.vlines(theta_c, ymin=0, ymax=max(i1.max(), i2.max())**(3/5), color='r')
        plt.text(theta_c+1, max(i1.max(), i2.max()) ** (4/7), f'Critical Angle',
                 fontsize=17)
    if show_brewster_angle:
        theta_b = np.degrees(np.pi - 2 * np.arctan(rm))
        plt.vlines(theta_b, ymin=0, ymax=max(i1.max(), i2.max())**(3/5), color='r')
        plt.text(theta_b+1, max(i1.max(), i2.max()) ** (4/7), f'Brewster Angle',
                 fontsize=17)
    fig.set_tight_layout(tight='rect')
    return fig

def plotData_multi(alpha=2000, rm=1.7, im=0.0, p=[0, 1], N_ta=2 ** 13 - 1, figsize=(20, 12)):
    '''N表示分波个数'''
    Rs1, Is1, Rs2, Is2 = 0, 0, 0, 0

    N = len(p)
    fig = plt.figure(figsize=figsize)
    ax1 = plt.subplot(2, 1, 1)  # 画在一起
    xySize = 17
    tick_dict = dict(direction='in', top=1, right=1, length=4, width=0.7, labelsize=15)
    ax1.tick_params(**tick_dict)
    for i in range(N):
        data = generateData(alpha, rm, p1=p[i], p2=p[i], im=im, N_ta=N_ta)
        theta = data['ScatteringAngle']
        theta = theta.to_numpy()
        rs1, is1, rs2, is2 = data['rs1'], data['is1'], data['rs2'], data['is2']
        rs1, is1, rs2, is2 = rs1.to_numpy(), is1.to_numpy(), rs2.to_numpy(), is2.to_numpy()
        Rs1 += rs1
        Is1 += is1
        Rs2 += rs2
        Is2 += is2
        #        plt.subplot(2,2,i+1)# 两行两列，第i+1个，分开画
        plt.plot(theta, np.log(rs1 * rs1 + is1 * is1), theta, np.log(rs2 * rs2 + is2 * is2))
        plt.ylabel('Logarithm of scattering amplitude (a.u.)', fontproperties='Times New Roman', fontsize=xySize)

    legendName = []
    for i in range(N):
        legendName.append('$A_1$ of $p_{}$'.format(p[i]))
        legendName.append('$A_2$ of $p_{}$'.format(p[i]))

    plt.legend(legendName)

    i1 = Rs1 * Rs1 + Is1 * Is1
    i2 = Rs2 * Rs2 + Is2 * Is2

    ax2 = plt.subplot(2, 1, 2)  # 两行一列第二个(N=2)

    plt.plot(theta, np.log(i1), theta, np.log(i2))

    plt.xlabel('Scattering Angle(deg)', fontproperties='Times New Roman', fontsize=xySize)
    plt.ylabel('Logarithm of scattering intensity (a.u.)', fontproperties='Times New Roman', fontsize=xySize)
    legend_dict = dict(family='Times New Roman', size=17)
    ax2.tick_params(**tick_dict)

    plt.legend(['$I_1$', '$I_2$'], prop=legend_dict)

    p_name = []

    for pi in p:
        p_name.append(f'$p_{{{pi}}}$ ')
    #     plt.title('The superposition of {}'.format(''.join(p_name)), fontsize=xySize)
    plt.text(70, 17, 'The superposition of {}'.format(''.join(p_name)), fontsize=17)
    # plt.show()
    return fig

if __name__ == '__main__':
    alpha, rm, im, p = eval(input('please input alpha, rm, im,[p1, p2]\nFor example:1000,0.7,0,[0,1]\n'))
    fig = plotData_multi(alpha=alpha, rm=rm, im=im, p=p)
    fig.show()
