import numpy as np
from numpy.fft import fft,fftshift


def space2fre(x, y):
    """ Transform space domain (x, y) to the frequency domain (frequency, amplitude)
    """
    x, y = x.reshape(-1, 1)[...,-1], y.reshape(-1, 1)[...,-1]
    x_max = x.max()
    x_min = x.min()
    N = len(x)
    delta_x = (x_max - x_min) / (N - 1)
    f_max = 1 / (2 * delta_x)
    delta_f = 2 * f_max / (N - 1)
    if N%2==0:
        fre_x = np.linspace(-f_max, f_max, N)-delta_f/2
    else:
        fre_x = np.linspace(-f_max, f_max, N)
    fre_y_shift = fftshift(fft(y))
    magnitude_energy = np.abs(fre_y_shift) / (N - 1)
    amplitude_y = magnitude_energy * 2 #  则表示原来振幅
    idx = np.argwhere(fre_x>=0)
    return fre_x[idx].reshape(-1, 1), amplitude_y[idx].reshape(-1, 1)
