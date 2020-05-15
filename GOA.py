import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def generateData(alpha,rm,p,N_ta = 2**13-1):
    '''
    生成p1——p2阶分波叠加分布，p1 <0绘制总光强
    '''
    origin_path = os.getcwd()
    if rm > 1:
        os.chdir("miedebye/GOA/m_gt_1")
    if rm < 1:
        os.chdir("miedebye/GOA/m_lt_1")
    exeName = "a.exe"
    txtName = 'Parameter_in.txt'

    Ta_min, Ta_max = 0,180
    with open(txtName,'w') as f1:
        f1.write(f'{alpha}\n'
                 f'{rm:.6f}\t{0.0}\n'
                 f'{N_ta}\t{Ta_min:.2f}\t{Ta_max:.2f}\n'
                 f'{p}\t')

    os.system(exeName)
    dataName = f"GOA,p={p},m={rm:.6f},a={alpha:.2f}.txt"
    data = pd.read_csv(dataName,sep ='\t',encoding='gbk',delimiter='\s+')
    os.remove(dataName)
    os.chdir(origin_path)
    return data

def superposition_intensity(alpha=2000, rm=1.7, p=[0, 1], N_ta=2 ** 13 - 1):
    """Return tuple(theta, i1, i2)"""

    Rs1, Is1, Rs2, Is2 = 0, 0, 0, 0
    N = len(p)
    for i in range(N):
        data = generateData(alpha, rm, p=p[i], N_ta=N_ta)
        theta = data['ScatteringAngle']
        theta = theta.to_numpy()
        #    i1, i2 = data['I1'], data['I2']
        #    i1,i2 = i1.to_numpy(), i2.to_numpy()

        rs1, is1, rs2, is2 = data['i1_re'], data['i1_im'], data['i2_re'], data['i2_im']
        rs1, is1, rs2, is2 = rs1.to_numpy(), is1.to_numpy(), rs2.to_numpy(), is2.to_numpy()
        Rs1 += rs1
        Is1 += is1
        Rs2 += rs2
        Is2 += is2

    i1 = Rs1 * Rs1 + Is1 * Is1
    i2 = Rs2 * Rs2 + Is2 * Is2
    return theta,i1, i2


def plot_goa(alpha=2000, rm=1.7, p=[0, 1], N_ta=2 ** 13 - 1, figsize=(15, 6)):
    theta, i1, i2 = superposition_intensity(alpha, rm, p, N_ta)

    fig = plt.figure(figsize=figsize)
    xySize = 17
    tick_dict = dict(direction='in', top=1, right=1, length=4, width=0.7, labelsize=15)
    ax = plt.subplot(1, 1, 1)
    x = theta[:]
    # y1, y2 = np.log(i1)[:],np.log(i2)[:]
    # x = theta
    # y1, y2 = np.log(i1)[:],np.log(i2)[:]
    plt.semilogy(x, i1, x, i2)
    plt.xlabel('Scattering Angle(deg)', fontproperties='Times New Roman', fontsize=xySize)
    plt.ylabel('Scattering intensity (a.u.)', fontproperties='Times New Roman', fontsize=xySize)
    legend_dict = dict(family='Times New Roman', size=17)
    ax.tick_params(**tick_dict)

    plt.legend(['$I_1$', '$I_2$'], prop=legend_dict)
    p_name = []

    for pi in p:
        p_name.append(f'$p_{{{pi}}}$ ')
    plt.text(70, max(i1.max(), i2.max())**(3/4), f'The superposition of {p_name[0]}and {p_name[1]}', fontsize=17)
    fig.set_tight_layout(tight='rect')
    return fig


def plot_multi(alpha=2000, rm=1.7, p=[0, 1], N_ta=2 ** 13 - 1, figsize=(15, 6)):
    '''N表示分波个数'''
    Rs1, Is1, Rs2, Is2 = 0, 0, 0, 0

    N = len(p)
    fig = plt.figure(figsize=figsize)
    ax1 = plt.subplot(2, 1, 1)  # 画在一起
    xySize = 17
    tick_dict = dict(direction='in', top=1, right=1, length=4, width=0.7, labelsize=15)
    ax1.tick_params(**tick_dict)
    for i in range(N):
        data = generateData(alpha, rm, p=p[i], N_ta=N_ta)

        theta = data['ScatteringAngle']
        theta = theta.to_numpy()

        rs1, is1, rs2, is2 = data['i1_re'], data['i1_im'], data['i2_re'], data['i2_im']
        rs1, is1, rs2, is2 = rs1.to_numpy(), is1.to_numpy(), rs2.to_numpy(), is2.to_numpy()
        Rs1 += rs1
        Is1 += is1
        Rs2 += rs2
        Is2 += is2
        x = theta[:]

        plt.plot(x, np.log(rs1 * rs1 + is1 * is1)[:], x, np.log(rs2 * rs2 + is2 * is2)[:])
        plt.ylabel('Logarithm of scattering amplitude (a.u.)', fontproperties='Times New Roman', fontsize=xySize)

    legendName = []
    for i in range(N):
        legendName.append('$A_1$ of $p_{}$'.format(p[i]))
        legendName.append('$A_2$ of $p_{}$'.format(p[i]))

    plt.legend(legendName)

    i1 = Rs1 * Rs1 + Is1 * Is1
    i2 = Rs2 * Rs2 + Is2 * Is2

    ax2 = plt.subplot(2, 1, 2)  # 两行一列第二个(N=2)
    y1, y2 = np.log(i1)[:], np.log(i2)[:]
    plt.plot(x, y1, x, y2)

    plt.xlabel('Scattering Angle(deg)', fontproperties='Times New Roman', fontsize=xySize)
    plt.ylabel('Logarithm of scattering intensity (a.u.)', fontproperties='Times New Roman', fontsize=xySize)
    legend_dict = dict(family='Times New Roman', size=17)
    ax2.tick_params(**tick_dict)

    plt.legend(['$I_1$', '$I_2$'], prop=legend_dict)
    fig.set_tight_layout(tight='rect')
    p_name = []

    for pi in p:
        p_name.append(f'$p_{{{pi}}}$ ')
    #     plt.title('The superposition of {}'.format(''.join(p_name)), fontsize=xySize)
    plt.text(x.max()/3, max(y1.max(), y2.max())*3/4, f'The superposition of {p_name[0]}and {p_name[1]}', fontsize=17)
    # plt.show()
    return fig

if __name__ == "__main__":
    plot_goa(alpha=2000, rm=1.7, p=[0, 1], N_ta=2 ** 13 - 1, figsize=(15, 6))