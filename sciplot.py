import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def plot(x, y, fig=None, figsize=(15, 6),
         color=None,
         xlabel='Scattering Angle(deg)', ylabel='Logarithm of scattering intensity (a.u.)',
         legend=['$I_1$', '$I_2$']
         ):

    xySize = 17
    if fig == None:
        fig = plt.figure(figsize=figsize)
    ax = plt.subplot(111)
    plt.plot(x, y, color=color)
    plt.xlim(0, 10)
    plt.ylim(0, 1)
    tick_dict = dict(direction='in', top=1, right=1, length=4, width=0.7, labelsize=15)
    plt.xlabel(xlabel, fontproperties='Times New Roman', fontsize=xySize)
    plt.ylabel(ylabel, fontproperties='Times New Roman', fontsize=xySize)
    legend_dict = dict(family='Times New Roman', size=17)
    ax.tick_params(**tick_dict)
    plt.legend(legend, prop=legend_dict)

    return fig