import matplotlib.pyplot as plt
from numpy import arange
from numpy import meshgrid
from numpy import log, pi, savetxt
from scipy import special
import sys


def WHH (alpha = 0.888):
    delta = 0.001
    xrange = arange(0.0001, 1.0, delta)
    yrange = arange(0.0001, 1.0, delta)
    t, h = meshgrid(xrange,yrange)
    # F is one side of the equation, G is the other
    # alpha = 0.888

    arg1 = (0.5*( 1+((1+alpha*1j)*4*h/pi/pi/t) ))
    arg2 = (0.5*( 1+((1-alpha*1j)*4*h/pi/pi/t) ))

    F = 0.5*( special.digamma(arg1) + special.digamma(arg2) ) - special.digamma(0.5)
    # F = special.digamma(0.5*(1+h/t)) - special.digamma(0.5)
    G = log(t)

    plt.figure('WHH', dpi = 96)   #figsize=(8,8),

    cp = plt.contour(t, h, (F + G), [0])
    # get data points from the contour plot:
    p = cp.collections[0].get_paths()[0]
    v = p.vertices
    x = v[:, 0]
    y = v[:, 1]
    ax = plt.gca()
    ax.clear()
    plt.ylabel('h')
    plt.xlabel('t (=T/Tc)')
    plt.grid(True)
    txt = '$\\alpha = ${0:1.4g}'.format(alpha)
    ax.set_title(txt, fontsize=22, fontweight='normal')
    plt.plot(x, y, label=txt)
    ax.legend(shadow=True, fancybox=True, loc='best')
    plt.draw()
    plt.show()
    headerTxt = 'x\ty'
    savetxt('data_alpha={0:1.4g}'.format(alpha)+'.txt', v[:, 0:2], fmt='%1.6e', delimiter='\t', header=headerTxt)
if __name__ == "__main__":
    print ('-> you run ',  __file__, ' file in a main mode')
    if len(sys.argv) > 1:
        for i in range(len(sys.argv[1:])):
            WHH(float(sys.argv[i+1]))
    else:
         print('--> please run in terminal the next command: psi_conduct 0.888 1.307 \n instead 0.888 you can put your values.')
    print('-> program ',  __file__, ' have been finished')