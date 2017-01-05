#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
from scipy.special import wofz
from scipy.interpolate import interp1d
from scipy import integrate
from scipy import constants as phys
from libs.dir_and_file_operations import *
import re
import math

def timeForCreatingMonoLayer(P=1e-10):
    nu = P*100/math.sqrt( 2*math.pi*1.6e-27*32*1.38e-23*300 )
    print('nu = {:.2e}'.format(nu))
    t = 1e23**(2/3)/nu
    # t = 3e-4/(P*100) # from wiki t in sec for ML creating with coeff = 1
    print('t = {0:.2} sec, {1:.2} year'.format(t, t/365/86400))
from libs.dir_and_file_operations import *
class Struct:
    '''
    Describe structure for a data
    '''
    def __init__(self):
        self.T = []
        self.R = []
        self.d = 1.1
        self.T_inflection = 30
        self.Tstep = 1
    def interpolate(self):
        self.xx = np.r_[self.T.min(): self.T.max(): self.Tstep]
        f = interp1d(self.T, self.R)
        self.yy = f(self.xx)

    def plot(self, ax):
        ax.plot(self.xx, self.yy, 'o-', label='{0}nm'.format(self.d))
        ax.set_ylabel('$R (Ohm)$', fontsize=20, fontweight='bold')
        ax.set_xlabel('$T (K)$', fontsize=20, fontweight='bold')
        ax.grid(True)
        # ax.fill_between(x, y - error, y + error,
        #                 alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF',
        #                 linewidth=4, linestyle='dashdot', antialiased=True, label='$\chi(k)$')

    def plotLogT(self, ax, T1 = 10, T2 = 300):
        # Plot graph log(1/rho) vs 1/T to define the range with a different behavior of charge currents
        a = self.xx
        # find indeces for elements inside the region [T1, T2]:
        ind = np.where(np.logical_and(a >= T1, a <= T2))
        x = 1/(self.xx[ind]**1)
        # y = np.log(self.yy[ind])
        y = self.yy[ind]**(-1)
        ax.plot(x, y, 'o-', label='{0}nm'.format(self.d))
        # ax.set_ylabel('$ln(1/\\rho)$', fontsize=20, fontweight='bold')
        ax.set_ylabel('$(\sigma)$', fontsize=20, fontweight='bold')
        ax.set_xlabel('$1/T^{1}$', fontsize=20, fontweight='bold')
        ax.grid(True)


class Hall:
    '''
        Search a goodness fit model for resistivity processes
    '''
    def __init__(self):

        self.dataFolderSorce = '/home/yugin/PycharmProjects/Si-Nb-Si-glass/data/Hall_Effect/R(T)'

        files_lsFN = listOfFilesFN_with_selected_ext(self.dataFolderSorce, ext = 'dat')

        # setup variables for plot:
        self.suptitle_txt = 'Resistivity'
        self.ylabel_txt = 'R, (Ohm)'
        self.xlabel_txt = '$T^{1/2}$'


        struct_of_data = {}
        self.setupAxes()

        indx = 0
        for i in files_lsFN:
            tmp_data = np.loadtxt(i, float)
            case_name = re.findall('[\d\.\d]+', os.path.basename(i))

            # create a new instance for each iteration step otherwise struct_of_data has one object for all keys
            data = Struct()
            data.d = float(case_name[0])
            data.T = tmp_data[:, 0]
            data.R = tmp_data[:, 1]
            data.interpolate()
            data.plot(self.ax)
            plt.draw()
            self.ax.legend(shadow=True, fancybox=True, loc='best')
            struct_of_data[case_name[0]] = data

            print('d = ', struct_of_data[case_name[0]].d, ' nm')
            indx = indx+1



        # for i in range(len(struct_of_data)):
        #     print(list(struct_of_data.keys())[i])
        #     print(list(struct_of_data.values())[i])
        #     print(list(struct_of_data.items())[i])

        sortKeys = sorted(struct_of_data, key=lambda key: struct_of_data[key].d)
        for i in sortKeys:
            self.ax.cla()
            # struct_of_data[i].plotLogT(self.ax)
            struct_of_data[i].plot(self.ax)

            self.ax.legend(shadow=True, fancybox=True, loc='best')
            plt.draw()
            # print(list(struct_of_data.items())[i])

        # self.ax.legend(shadow=True, fancybox=True, loc='best')

    def setupAxes(self):
        # create figure with axes:

        pylab.ion()  # Force interactive
        plt.close('all')
        ### for 'Qt4Agg' backend maximize figure
        plt.switch_backend('QT4Agg')

        self.fig = plt.figure()
        # gs1 = gridspec.GridSpec(1, 2)
        # fig.show()
        # fig.set_tight_layout(True)
        self.figManager = plt.get_current_fig_manager()
        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(800.0 / DPI, 600.0 / DPI)

        gs = gridspec.GridSpec(1, 1)

        self.ax = self.fig.add_subplot(gs[0, 0])
        self.ax.grid(True)

        self.fig.suptitle(self.suptitle_txt, fontsize=22, fontweight='normal')

        # Change the axes border width
        for axis in ['top', 'bottom', 'left', 'right']:
            self.ax.spines[axis].set_linewidth(2)
        # plt.subplots_adjust(top=0.85)
        # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
        self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

        # put window to the second monitor
        # figManager.window.setGeometry(1923, 23, 640, 529)
        self.figManager.window.setGeometry(780, 20, 800, 600)
        self.figManager.window.setWindowTitle('Hall fitting')
        self.figManager.window.showMinimized()

        self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)


        # save to the PNG file:
        # out_file_name = '%s_' % (case) + "%05d.png" % (numOfIter)
        # fig.savefig(os.path.join(out_dir, out_file_name))



class HallCoefficient:
    def __init__(self):

        self.baseOutDir = '/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/Hall_Effect'
        # setup variables for plot:
        self.suptitle_txt = 'Hall Coefficient'
        self.ylabel_txt = '$R_H (m^3/C)$'
        self.xlabel_txt = 'd (m)'

        self.setupAxes()
        # Calculation are provides in SI:
        self.Rh_Nb = 8.72e-11 # m^3/C
        self.Rh_Nb_error = math.fabs(9e-11 - self.Rh_Nb)*0.5

        self.Rh_NbSi2 = -7.7e-11 # m^3/C
        self.Rh_NbSi2_error = 1e-12

        self.n_Nb = 1/phys.e/self.Rh_Nb
        self.n_Nb_error = self.n_Nb*self.Rh_Nb_error/self.Rh_Nb

        self.n_NbSi2 = 1/phys.e/self.Rh_NbSi2
        self.n_NbSi2_error = self.n_NbSi2*self.Rh_NbSi2_error/self.Rh_NbSi2

        # critical thickness when Rh = 0 from the graph:
        self.d0 = ((1.87+1.72)*0.5)*1e-9
        self.d0_error = ((1.87-1.72)*0.5)*1e-9

        self.p = self.n_Nb
        self.p_error = self.n_Nb_error
        self.n = math.fabs(self.n_NbSi2)
        self.n_error = self.n_NbSi2_error

        self.x = 0.5*self.d0*self.p/(self.p+self.n)
        self.x_error = self.x*math.sqrt((self.d0_error/self.d0)**2 + (2*self.n_error/(self.p + self.n))**2 +
                                        ( self.p_error*(self.n-self.p)/self.p/(self.p+self.n) )**2)

    def printValues(self):
        self.p_txt = 'p = {:.3f}'.format(self.p/1e28) + ' +/- {:.3f} (*10^28)1/m^3'.format(self.p_error/1e28)
        print(self.p_txt)
        self.n_txt = 'n = {:.3f}'.format(self.n/1e28) + ' +/- {:.3f} (*10^28)1/m^3'.format(self.n_error/1e28)
        print(self.n_txt)

        self.d0_txt = 'do = {:.3f}'.format(self.d0*1e9) + ' +/- {:.3f} nm'.format(self.d0_error*1e9)
        print(self.d0_txt)
        self.x_txt = 'x = {:.3f}'.format(self.x*1e9) + ' +/- {:.3f} nm'.format(self.x_error*1e9)
        print(self.x_txt)

    def calcValue(self):
        # create array of thickness values:
        self.d = np.r_[0.9: 10: 0.5]*1e-9
        self.Rh = np.zeros(len(self.d))
        self.Rh_error = np.zeros(len(self.d))
        out_array = np.zeros((len(self.d),3))
        ind = 0
        for h in self.d:
            self.Rh[ind] = calc_Rh(n = self.n, p = self.p, d = h, x = self.x)
            self.Rh_error[ind] = calc_Rh_error(n = self.n, sigma_n = self.n_error, p = self.p, sigma_p = self.p_error,
                                          d = h, sigma_d = 2e-10 , x = self.x, sigma_x = self.x_error)
            ind = ind + 1

        out_array[:, 0] = self.d[:]
        out_array[:, 1] = self.Rh[:]
        out_array[:, 2] = self.Rh_error[:]

        self.plot(self.ax)

        outDirPath = create_out_data_folder(self.baseOutDir, first_part_of_folder_name='Rh(d)')
        if not (os.path.isdir(outDirPath)):
            os.makedirs(outDirPath, exist_ok=True)
        out_file_name = 'Rh(d).png'
        self.fig.savefig(os.path.join(outDirPath, out_file_name))
        # save results to the *.dat file:
        headerTxt = self.p_txt +'\n' + self.n_txt +'\n' +self.d0_txt +'\n' +self.x_txt +'\n' +'d (m)\tRh (m^3/C)\tstd'
        np.savetxt(os.path.join(outDirPath, 'Rh_result.dat'), out_array, fmt='%1.6e', delimiter='\t', header=headerTxt)

    def setupAxes(self):
        # create figure with axes:

        pylab.ion()  # Force interactive
        plt.close('all')
        ### for 'Qt4Agg' backend maximize figure
        plt.switch_backend('QT4Agg')

        self.fig = plt.figure()
        # gs1 = gridspec.GridSpec(1, 2)
        # fig.show()
        # fig.set_tight_layout(True)
        self.figManager = plt.get_current_fig_manager()
        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(800.0 / DPI, 600.0 / DPI)

        gs = gridspec.GridSpec(1, 1)

        self.ax = self.fig.add_subplot(gs[0, 0])
        self.ax.grid(True)

        self.fig.suptitle(self.suptitle_txt, fontsize=22, fontweight='normal')

        # Change the axes border width
        for axis in ['top', 'bottom', 'left', 'right']:
            self.ax.spines[axis].set_linewidth(2)
        # plt.subplots_adjust(top=0.85)
        # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
        self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

        # put window to the second monitor
        # figManager.window.setGeometry(1923, 23, 640, 529)
        self.figManager.window.setGeometry(780, 20, 800, 600)
        self.figManager.window.setWindowTitle('Hall Coefficient')
        self.figManager.window.showMinimized()

        self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)


        # save to the PNG file:
        # out_file_name = '%s_' % (case) + "%05d.png" % (numOfIter)
        # fig.savefig(os.path.join(out_dir, out_file_name))

    def plot(self, ax):
        ax.plot(self.d*1e9, self.Rh, 'o-', color='#1B2ACC', label='{0:3f}nm'.format(self.x*1e9))
        # ax.plot(x, y_median, '-o', label='<$' + labelStartName + '$> median', color='darkcyan')
        # ax.plot(x, y_max, label='<$' + labelStartName + '$> max', color='skyblue')
        # ax.plot(x, y_min, label='<$' + labelStartName + '$> min', color='lightblue')

        self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
        # ax.plot(x, y, 'k', color='#1B2ACC')

        ax.fill_between(self.d*1e9, self.Rh - self.Rh_error, self.Rh + self.Rh_error,
                        alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF',
                        linewidth=4, linestyle='dashdot', antialiased=True, label='$\chi(k)$')
        ax.grid(True)
        ax.set_ylabel('$R_H (m^3/C)$', fontsize=20, fontweight='bold')
        ax.set_xlabel('$d (nm)$', fontsize=20, fontweight='bold')

def calc_Rh(n = 8.11e28, p = 7.16e28, d = 1e-9, x = 0.42e-9):
    I = (p*d - 2*x*(p+n))
    II = (p*d - 2*x*(p-n))
    IIsq = II**2

    Rh = d*I/IIsq/phys.e
    return Rh

def calc_Rh_error(n = 8.11e28, sigma_n = 0.11e28, p = 7.16e28, sigma_p = 0.11e28, d = 1e-9, sigma_d = 1e-11 , x = 0.42e-9, sigma_x = 2e-11):
    I = (p*d - 2*x*(p+n))
    II = (p*d - 2*x*(p-n))
    IdivII = I/II
    IIsq = II**2

    dRp = ( d*(d-2*x)/phys.e/IIsq ) * ( 1 - 2*IdivII)
    dRn = ( d*2*x/phys.e/IIsq ) * ( 1 + 2*IdivII)
    dRx = (d * 2 / phys.e / IIsq) * (p + n - 2 * (p - n) * IdivII)
    dRd = (d / phys.e / IIsq) * ( I/d + p*(1-2*IdivII) )


    return math.sqrt( (dRp*sigma_p)**2 + (dRn*sigma_n)**2 + (dRx*sigma_x)**2 + (dRd*sigma_d)**2)





if __name__ == "__main__":
    print ('-> you run ',  __file__, ' file in a main mode' )
    # a = HallCoefficient()
    # a.printValues()
    # print(calc_Rh_error())
    # a.calcValue()
    a = Hall()
    print('-> script ',  __file__, ' had been finished' )

