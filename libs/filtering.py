from scipy.special import wofz
import numpy as np
from matplotlib import pylab
import matplotlib.pyplot as plt
from scipy.signal import deconvolve

# for smooth by using a window
def G(x, alpha):
    """ Return Gaussian line shape at x with HWHM alpha """
    return np.sqrt(np.log(2) / np.pi) / alpha\
                             * np.exp(-(x / alpha)**2 * np.log(2))

def L(x, gamma):
    """ Return Lorentzian line shape at x with HWHM gamma """
    return gamma / np.pi / (x**2 + gamma**2)

def V(x, alpha, gamma):
    """
    Return the Voigt line shape at x with Lorentzian component HWHM gamma
    and Gaussian component HWHM alpha.

    """
    sigma = alpha / np.sqrt(2 * np.log(2))

    return np.real(wofz((x + 1j*gamma)/sigma/np.sqrt(2))) / sigma\
                                                           /np.sqrt(2*np.pi)


def y_in_region(x, y, region=None):
    '''
    function return y=0 for that points, which are placed outside the region
    :param x: x - values of vector
    :param y: y - values of vector
    :param region:  [a,b] -
    :return:
    '''
    if region == None:
        return y
    else:
        if len(region) < 2:

            return y
        else:
            region.sort()
            a = region[0]
            b = region[1]
            #  set elements outside the region zeroed out
            y[x <= a] = 0
            y[x >= b] = 0

            return y

def smooth_by_window (y, window_len=11, window='gauss', alpha=0.1, gamma = 0.1, blur_or_sharp = 'blur'):

    if y.ndim != 1:
        raise (ValueError, "smooth only accepts 1 dimension arrays.")

    if y.size < window_len:
        raise (ValueError, "Input vector needs to be bigger than window size.")

    if window_len<3:
        return y

    if not window in ['gauss', 'lorentzian', 'voigt']:
        raise (ValueError, "Window is on of 'gauss', 'lorentzian', 'voigt'")

    if not blur_or_sharp in ['blur', 'sharp']:
        raise (ValueError, "You select understanding procedure of convolution. It must be only 'blur' or 'sharp'")


    s=np.r_[y[window_len-1:0:-1],y,y[-1:-window_len:-1]]
    # s = y
    w= np.linspace(-1,1, window_len)
    if window == 'gauss':
        w = G(w, alpha)
    if window == 'lorentzian':
        w = L(w, gamma)
    if window == 'voigt':
        w = V(w, alpha, gamma)
    #  normalize window to the w.max = 1:
    w = w/w.max()


    if blur_or_sharp in 'sharp':
        #  reflect window y-values from the y=1 line
        # we create hole in center of the window region:
        w = 1 - w
        y = np.convolve(w/w.sum(),s,mode='valid' )
        # y = np.array(deconvolve(s,w/w.sum()))[0] # quotient
        # y = np.array(deconvolve(s,w/w.sum()))[0] # remainder

    else:
        y = np.convolve(w/w.sum(),s,mode='valid' )


    if (window_len % 2 == 0): #even
        return y[(window_len/2-1):-(window_len/2)]
    else: #odd
        return y[(window_len/2):-(window_len/2)]




if __name__ == "__main__":
    # if this file run by itself:
    alpha, gamma = 0.1, 0.1

    #generate a source step-function:
    x = np.linspace(1,4,100)
    y = np.linspace(2,4,100)
    region = [2,3]
    y = y_in_region(x,y,region)

    plt.plot(y,'.-', c='k', label='step func')
    plt.ylim([-0.5, 3.5])
    plt.show()

    windows = ['gauss', 'lorentzian', 'voigt']
    z = smooth_by_window(y,window='voigt', window_len=21)

    for w in windows:
        print(w)
        z = smooth_by_window(y,window=w)

        plt.plot(z, label=w)
        plt.draw()
    plt.legend()

