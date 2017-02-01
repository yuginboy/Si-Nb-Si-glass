import sys
import os
from io import StringIO
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
import scipy as sp
from scipy.interpolate import interp1d
class OutPlotVars:
    def __init__(self):
        self.fig = []
        self.ax = []


def plotData(x = np.r_[0:50], y = np.cos(np.r_[0:50]/6*np.pi), error = np.random.rand(50) * 0.5, numOfIter = 1,
             y_median = np.sin(np.r_[0:50]/6*np.pi), y_max = np.cos(np.r_[0:50]/6*np.pi)+1.5,  y_min = np.cos(np.r_[0:50]/6*np.pi)-1.5,
             out_dir = '/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/Version_45-deg_v03_001/calc/set_of_residuals',
             window_title = 'test',
             title_txt = 'Differences between theoretical and experimental data', labelStartName = 'RD',
             xlabeltxt = 'Concentration $x$ of Si ($Si_xNb_{1-x}$)', ylabeltxt = 'Residuals (%)', case='rd'):

    pylab.ion()  # Force interactive
    plt.close('all')
    ### for 'Qt4Agg' backend maximize figure
    plt.switch_backend('QT5Agg')

    fig = plt.figure()
    # gs1 = gridspec.GridSpec(1, 2)
    # fig.show()
    # fig.set_tight_layout(True)
    figManager = plt.get_current_fig_manager()
    DPI = fig.get_dpi()
    fig.set_size_inches(1920.0 / DPI, 1080.0 / DPI)

    gs = gridspec.GridSpec(1,1)

    ax = fig.add_subplot(gs[0,0])
    txt = title_txt
    # txt =  'GaMnAs case %s, ' % case + '$\chi(k)$ when the Number of the treated file is: {0}'.format(numOfIter)
    fig.suptitle(txt, fontsize=22, fontweight='normal')

    # Change the axes border width
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    # plt.subplots_adjust(top=0.85)
    # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
    fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

    # put window to the second monitor
    # figManager.window.setGeometry(1923, 23, 640, 529)
    figManager.window.setGeometry(1920, 20, 1920, 1180)
    figManager.window.setWindowTitle(window_title)
    figManager.window.showMinimized()

    # plt.show()
    ax.plot( x, y, '-o', label = '<$'+labelStartName+'$>' )
    ax.plot( x, y_median, '-o', label = '<$'+labelStartName +'$> median', color = 'darkcyan' )
    ax.plot( x, y_max, label = '<$'+labelStartName+'$> max', color = 'skyblue' )
    ax.plot( x, y_min, label = '<$'+labelStartName+'$> min', color = 'lightblue' )

    fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
    ax.plot(x, y, 'k', color='#1B2ACC')


    ax.fill_between(x, y-error, y+error,
        alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF',
        linewidth=4, linestyle='dashdot', antialiased=True, label = '$\chi(k)$')



    ax.grid(True)

    ax.set_ylabel(ylabeltxt, fontsize=20, fontweight='bold')
    ax.set_xlabel(xlabeltxt, fontsize=20, fontweight='bold')
    # ax.set_ylim(ymin = -0.3, ymax= 0.5)
    ax.legend(shadow=True, fancybox=True, loc='best')
    # plt.draw()
    # save to the PNG file:
    out_file_name = '%s_' % (case) + "%05d.png" %(numOfIter)
    # fig.savefig( os.path.join(out_dir, out_file_name) )

    # create output links on fig and axes:
    out_var = OutPlotVars()
    out_var.fig = fig
    out_var.ax = ax

    return out_var

if __name__ == "__main__":
    plotData()
    print ('plot the data')