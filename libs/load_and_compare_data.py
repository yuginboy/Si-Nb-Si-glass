"Main file for run this package"
import pandas as pd
import sys
import os
from io import StringIO
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
import scipy as sp
from scipy.interpolate import interp1d
import re
from libs.backgrounds import shirley_base, shirley_new
from libs.estimations import std_residual, y_in_region, get_integral_in_region
from libs.filtering import smooth_by_window
from operator import itemgetter, attrgetter

from libs.dir_and_file_operations import *
from libs.plot_data import plotData
# for parallel calculation:
import time
from joblib import Parallel, delayed
import multiprocessing



def defLabelFromFileName(txt):
    # set the values for graphs label name like: '0 min' instead of '00'
    if '00' in txt:
        return '0 min'
    if '08' in txt:
        return '8 min'
    if '14' in txt:
        return '14 min'
    if '17' in txt:
        return '17 min'
    if '24' in txt:
        return '24 min'

def etchTimeFromFileName(txt):
    # set the values for graphs label name like: '0' instead of '00'
    if '00' in txt:
        return 0
    if '08' in txt:
        return 8
    if '14' in txt:
        return 14
    if '17' in txt:
        return 17
    if '24' in txt:
        return 24


def importExperimentDataNb(dataPath):
    # Import Si2p and Nb3d spectra from 2 files in experiment subfolder
    """

    """
    for file in os.listdir(os.path.join(dataPath, 'experiment')):
        if file.endswith(".dat"):
            if 'Nb' in file:
                # print('Nb:', os.path.join(dataPath, file))
                Nbexp = pd.read_csv(os.path.join(dataPath, 'experiment', file), comment='#', delimiter='\t')

    return Nbexp

def importExperimentDataSi(dataPath):
    # Import Si2p and Nb3d spectra from 2 files in experiment subfolder
    """

    """
    for file in os.listdir(os.path.join(dataPath, 'experiment')):
        if file.endswith(".dat"):

            if 'Si' in file:
                # print('Si:', os.path.join(dataPath, file))
                Siexp = pd.read_csv(os.path.join(dataPath, 'experiment', file), comment='#', delimiter='\t')

    return Siexp

def bg_substraction(x,y):
    return y-shirley_new(x,y)



class WorkWithXPSSpectra:
    '''
    Class wich load SESSA's calculated Nb,Si spectra, load raw experimental spectra, subtract bg,
    interpolate for equal number of energy points, align spectra by maxima-maxima point, calculate integral inside ROI and
    a lot of different things which we can do with XPS spectra by physical and mathematical data processing
    '''
    def __init__(self):
        self.dataPath = '/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/Version_45-deg_v03_002_with_refSpectra'

        # n01: Region of interest for calc STD and residual integral values
        # self.RIO_Si = [105, 96]
        # self.RIO_Nb = [200, 208]

        # n02:  a little bit closer region then n01
        # self.RIO_Si = [105, 97.5]
        # self.RIO_Nb = [201, 207]

        # n03:  measure only biggest peak:
        # self.RIO_Si = [98, 101.3]
        # self.RIO_Nb = [201.5, 204.5]

        # n04:  measure only 1/2 of the biggest peak:
        # self.RIO_Si = [99.3, 101]
        # self.RIO_Nb = [202.85, 204]

        # Select only a top peaks area
        # RIO_Si = [99.4, 99.2]
        # RIO_Nb = [202.8, 202.9]

        self.RIO_Si = [105, 96]
        self.RIO_Nb = [200, 208]

        self.blur_or_sharp = 'as_is' # the one from these values: 'blur', 'sharp', 'as_is'
        self.alpha=0.5
        self.gamma = 0.5
        self.window_len = 200
        self.window_name = 'gauss' # window_name: 'gauss', 'lorentzian', 'voigt'
        # use info about element concentration or not:
        self.useConcentrationOfElem = True
        self.uniqPartNameOfSESSACalcDirs = 'out_'
        # Colors for lines on a graph, length of this value and number of time-point simulations should be the same:
        self.colorsForGraph = ['peru','dodgerblue','brown','red', 'darkviolet']

        pylab.ion()  # Force interactive
        plt.close('all')
        ### for 'Qt4Agg' backend maximize figure
        plt.switch_backend('QT4Agg')

        self.fig = plt.figure()
        # gs1 = gridspec.GridSpec(1, 2)
        # self.fig.show()
        # fig.set_tight_layout(True)
        self.figManager = plt.get_current_fig_manager()
        DPI = self.fig.get_dpi()
        self.fig.set_size_inches(1920.0 / DPI, 1080.0 / DPI )

        self.wantPlotSpectraBeforeAndAfterFiltering = True
        self.wantPlotSpectraExperimentalAndAfterFiltering = True
        self.wantSpectraAndResiduals = True

        # type of residuals to calculate 'integral', 'std':
        self.residualsType = 'integral'

    def loadExperimentalData(self):
        '''
        Load experimental data from subfolder "experiment" (it should exist!)
        :return:
        '''
        self.Nbexp = importExperimentDataNb(self.dataPath)
        self.Siexp = importExperimentDataSi(self.dataPath)

        self.srcNb = np.zeros((len(self.Nbexp['BE (eV)']), 6))
        self.srcNb[:, 0]= self.Nbexp['BE (eV)'].values
        self.srcNb[:, 1] = self.Nbexp['0 min'].values
        self.srcNb[:, 2] = self.Nbexp['8 min'].values
        self.srcNb[:, 3] = self.Nbexp['14 min'].values
        self.srcNb[:, 4] = self.Nbexp['17 min'].values
        self.srcNb[:, 5] = self.Nbexp['24 min'].values

        self.srcSi = np.zeros((len(self.Siexp['BE (eV)']), 6))
        self.srcSi[:, 0] = self.Siexp['BE (eV)'].values
        self.srcSi[:, 1] = self.Siexp['0 min'].values
        self.srcSi[:, 2] = self.Siexp['8 min'].values
        self.srcSi[:, 3] = self.Siexp['14 min'].values
        self.srcSi[:, 4] = self.Siexp['17 min'].values
        self.srcSi[:, 5] = self.Siexp['24 min'].values

        # Subtract background:
        for i in range(1,6):
            self.srcNb[:, i] = bg_substraction(self.srcNb[:, 0], self.srcNb[:, i])
            self.srcSi[:, i] = bg_substraction(self.srcSi[:, 0], self.srcSi[:, i])

    def loadSESSAspectra(self):

        # check if loadExperimentalData was run before:
        if not hasattr(self, 'Nbexp'):
            self.loadExperimentalData()


        # load SESSA calculated spectra:
        self.dirPathList = listdirs(self.dataPath)
        self.dirFullPathList = listdirsFN(self.dataPath)

        # Create new list only with elements which contains substring 'out' = self.uniqPartNameOfSESSACalcDirs
        self.d = [i for i in self.dirPathList if self.uniqPartNameOfSESSACalcDirs in i ]

        # folderName = '/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/Version_45-deg_v03_001/out_Si0.01Ni0.99'
        self.Nbcalc = np.zeros((2048, 5, len(self.d)))
        self.Sicalc = np.zeros((2048, 5, len(self.d)))
        self.srcValuesFromSESSA_Nb  = np.zeros((2048, 5, len(self.d)))
        self.srcValuesFromSESSA_Si  = np.zeros((2048, 5, len(self.d)))
        self.nSiNb = np.zeros((len(self.d),2))

        # set the values for graphs label name like: '0 min' instead of '00'
        self.graphLabelName = []

        i = 0
        j = 0
        # sort the list of folder names:
        neededFolders = list(k for k in self.dirPathList if self.uniqPartNameOfSESSACalcDirs in k)
        parameter = list(int(float(re.findall("\d+\.\d+", k)[0])*100) for k in neededFolders)
        sortedlist = [i[0] for i in sorted(zip(neededFolders, parameter), key=lambda l: l[1], reverse=False)]
        for folderName in sortedlist:
            # check the 'out_' folders only
            if self.uniqPartNameOfSESSACalcDirs in folderName:
                concentration = re.findall("\d+\.\d+", folderName)
                self.nSiNb[j, 0] = concentration[0] #Si
                self.nSiNb[j, 1] = concentration[1] #Nb
                folderFullName = os.path.join(self.dataPath,folderName)
                for file in sorted(file for file in sorted(os.listdir(folderFullName)) if file.startswith('Si') and file.endswith(".dat")):
                    # print('Si:', os.path.join(folderFullName, file))
                    data = pd.read_csv(os.path.join(folderFullName, file), comment='#', header=None, delimiter='\t',
                                       names=('Energy', 'Intensity', 'NaN'))
                    data['Energy'] = 1486.6 - data['Energy']
                    self.Six = data['Energy'].values
                    self.Sicalc[:,i,j] = data['Intensity'].values
                    i += 1

                i = 0
                for file in sorted(file for file in sorted(os.listdir(folderFullName)) if file.startswith('Nb') and file.endswith(".dat")):
                    # print('Nb:', os.path.join(folderFullName, file))
                    data = pd.read_csv(os.path.join(folderFullName, file), comment='#', header=None, delimiter='\t',
                                       names=('Energy', 'Intensity', 'NaN'))
                    data['Energy'] = 1486.6 - data['Energy']
                    self.Nbx = data['Energy'].values
                    self.Nbcalc[:, i, j] = data['Intensity'].values
                    self.graphLabelName.append(defLabelFromFileName(file))

                    i += 1

                    # Nbcalc[:,i,j]=Nby
                    # Sicalc[:,i,j]=Siy

                j += 1
                i = 0

        # interpolate data for Experimental data points
        self.interpSi = np.zeros((len(self.Six), 5))
        self.interpNb = np.zeros((len(self.Nbx), 5))

        for i in range(5):
            f = interp1d(self.srcSi[:, 0], self.srcSi[:, i+1])
            self.interpSi[:, i] = f(self.Six)
            f = interp1d(self.srcNb[:, 0], self.srcNb[:, i+1])
            self.interpNb[:, i] = f(self.Nbx)


        # Normalize experimental data after interpolation:
        maxVal   =  self.interpNb.max()
        self.interpNb =  self.interpNb/maxVal

        maxVal   = self.interpSi.max()
        self.interpSi = self.interpSi/maxVal

        # calculate BE shift between experiment and calculation
        self.calcBE_Si = self.Six[self.Sicalc[:, 1, 0].argmax()]
        self.expBE_Si  = self.Six[self.interpSi[:, 1].argmax()]
        self.deltaBE_Si = self.expBE_Si - self.calcBE_Si
        # self.deltaBE_Si = 0.0
        print('calcBE_Si= {0:.5}, expBE_Si={1:.5}, delta={2:.5}'.format(self.calcBE_Si, self.expBE_Si, self.deltaBE_Si))

        self.calcBE_Nb = self.Nbx[self.Nbcalc[:, 3, 0].argmax()]
        self.expBE_Nb = self.Nbx[self.interpNb[:, 3].argmax()]
        self.deltaBE_Nb = self.expBE_Nb - self.calcBE_Nb - 0.08
        print('calcBE_Nb= {0:.5}, expBE_Nb={1:.5}, delta={2:.5}'.format(self.calcBE_Nb, self.expBE_Nb, self.deltaBE_Nb))

        self.SiXexp = self.Six - self.deltaBE_Si
        self.NbXexp = self.Nbx - self.deltaBE_Nb



        # normalize SESSA data to Intensity eq y=1:
        for i in range(len(self.d)):
            maxVal = self.Nbcalc[:,:,i].max()

            self.Nbcalc[:,:,i] = self.Nbcalc[:,:,i]/maxVal

            maxVal = self.Sicalc[:,:,i].max()
            self.Sicalc[:,:,i] = self.Sicalc[:,:,i]/maxVal

        # Remember all normalized calculation values from SESSA as_is before filtering for subsequent comparing:
        self.srcValuesFromSESSA_Si [:, :, :] = self.Sicalc [:, :, :]
        self.srcValuesFromSESSA_Nb [:, :, :] = self.Nbcalc [:, :, :]


        # apply filter to the SESSA normalized spectra:
        #
        for j in range(len(self.d)):
            for i in range(5):
                if self.blur_or_sharp in ['blur', 'sharp']:
                    self.Nbcalc[:, i, j] = smooth_by_window (self.Nbcalc[:, i, j], window_len=self.window_len, window = self.window_name, alpha=self.alpha, gamma = self.gamma, blur_or_sharp= self.blur_or_sharp)
                    self.Nbcalc[:, i, j] = y_in_region (self.Nbx, self.Nbcalc[:, i, j], region=self.RIO_Nb)

                    self.Sicalc[:, i, j] = smooth_by_window (self.Sicalc[:, i, j], window_len=self.window_len, window = self.window_name, alpha=self.alpha, gamma = self.gamma, blur_or_sharp= self.blur_or_sharp)
                    self.Sicalc[:, i, j] = y_in_region (self.Six, self.Sicalc[:, i, j], region=self.RIO_Si)

                else:
                    self.Nbcalc[:, i, j] = y_in_region(self.Nbx, self.Nbcalc[:, i, j], region=self.RIO_Nb)
                    self.Sicalc[:, i, j] = y_in_region(self.Six, self.Sicalc[:, i, j], region=self.RIO_Si)

        # create OUT data folder:
        ROI_txt = 'Si=[{},{}]_Nb=[{},{}]_'.format(self.RIO_Si[0], self.RIO_Si[1], self.RIO_Nb[0], self.RIO_Nb[1])
        if self.blur_or_sharp in ['blur', 'sharp']:

            if self.window_name in 'gauss':
                self.values_of_current_project = ROI_txt + self.blur_or_sharp + "_{}_alpha={}_window_len={}".\
                    format(self.window_name, self.alpha, self.window_len)

            if self.window_name in 'lorentzian':
                self.values_of_current_project = ROI_txt + self.blur_or_sharp + "_{}_gamma={}_window_len={}".\
                    format(self.window_name, self.gamma, self.window_len)

            if self.window_name in 'voigt':
                self.values_of_current_project = ROI_txt + self.blur_or_sharp + "_{}_alpha={}_gamma={}_window_len={}".\
                    format(self.window_name, self.alpha, self.gamma, self.window_len)
        else:

             self.values_of_current_project = ROI_txt + self.blur_or_sharp


        # create a base out subdirectory with name 'calc':
        self.baseOutDir = createFolder( os.path.join((self.dataPath), 'calc') )
        # create a base out dir for set of calculated residuals:
        self.baseOutDirResiduals = createFolder( os.path.join((self.baseOutDir), 'set_of_residuals') )
        # create unique name for calculated data cases:
        self.name_of_out_folder = 'calc_' + self.values_of_current_project
        # create 0001-type of subdirectory inside unique subdirectory:
        self.out_dir = create_out_data_folder( os.path.join(self.baseOutDir, self.name_of_out_folder) )

        # only for test procedure and chek correct value of energy shift:
        # self.plotSpectraSESSABeforeAndAfterEnergyShifts()

        if self.wantPlotSpectraBeforeAndAfterFiltering:
            # plot if needed:
            self.plotSpectraSESSABeforeAndAfterFiltering()


        # normalize filtered SESSA spectra:
        for i in range(len(self.d)):
            maxVal = self.Nbcalc[:, :, i].max()
            self.Nbcalc[:, :, i] = self.Nbcalc[:, :, i]/maxVal

            maxVal = self.Sicalc[:, :, i].max()
            self.Sicalc[:, :, i] = self.Sicalc[:, :, i]/maxVal

        if self.wantPlotSpectraExperimentalAndAfterFiltering:
            # plot if needed:
            self.plotSpectraExperimentalAndSESSAAfterFiltering()

        # main cycle for calculate residuals:
        self.stdSi = np.zeros((len(self.d), 1))
        self.stdNb = np.zeros((len(self.d), 1))

        for j in range(len(self.d)):

            if self.residualsType in 'integral':
                 # Calculate integrals, take subtraction between modules and then take a sum:
                 #    dd = np.abs( get_integral_in_region(SiXexp,interpSi[:,3],RIO_Si) )
                 #    dd = np.abs( get_integral_in_region(SiXexp,interpSi[:,3],RIO_Si) )
                self.stdSi[j] = np.abs(   np.abs( get_integral_in_region(self.SiXexp, self.interpSi, self.RIO_Si) ) -
                                          np.abs( get_integral_in_region(self.Six, self.Sicalc[:, :, j], self.RIO_Si) )   ).sum()

                self.stdNb[j] = np.abs(   np.abs( get_integral_in_region(self.NbXexp, self.interpNb, self.RIO_Nb) ) -
                                          np.abs( get_integral_in_region(self.Nbx, self.Nbcalc[:, :, j], self.RIO_Nb) )   ).sum()

            elif self.residualsType in 'std':
                # calc std errors between experimental and filtered SESSA spectra:
                self.stdSi[j] = (std_residual(self.SiXexp, self.interpSi, self.Six, self.Sicalc[:, :, j], self.RIO_Si))
                self.stdNb[j] = (std_residual(self.NbXexp, self.interpNb, self.Nbx, self.Nbcalc[:, :, j], self.RIO_Nb))

        # normalized residuals:
        self.residuals_stdSi_in_au = (self.stdSi/self.stdSi.max())*100
        self.residuals_stdNb_in_au = (self.stdNb/self.stdNb.max())*100

        if self.wantSpectraAndResiduals:
            # plot if needed:
            self.plotSpectraAndResiduals()

        # save DATA to the ASCII tables:
        self.saveArrayToASCII()

        # plot main graph:
        self.plotResiduals()

    def plotSpectraSESSABeforeAndAfterEnergyShifts(self):
        # Check data for corrected shift procedure

        self.fig.clf()
        gs = gridspec.GridSpec(1, 2)

        self.axesNb = self.fig.add_subplot(gs[0, 0])
        self.axesNb.invert_xaxis()
        self.axesNb.set_title('Nb')
        self.axesSi = self.fig.add_subplot(gs[0, 1])
        self.axesSi.invert_xaxis()
        self.axesSi.set_title('Si')

        for axis in ['top', 'bottom', 'left', 'right']:
            self.axesSi.spines[axis].set_linewidth(2)
            self.axesNb.spines[axis].set_linewidth(2)
        # plt.subplots_adjust(top=0.85)
        # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
        self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

        # put window to the second monitor
        # figManager.window.setGeometry(1923, 23, 640, 529)
        self.figManager.window.setGeometry(0, 20, 1280, 800)

        plt.show()

        # test again for normalizing calculation spectra after filtering:
        for j in range(len(self.d)):
            self.axesNb.cla()
            self.axesSi.cla()
            for i in range(5):
                # plot source calculated data:
                self.axesNb.plot(self.Nbx, self.srcValuesFromSESSA_Nb[:, i, j], '--',
                                 label=(self.graphLabelName[i] + ' src'), color=self.colorsForGraph[i], linewidth=2.5)
                self.axesSi.plot(self.Six, self.srcValuesFromSESSA_Si[:, i, j], '--',
                                 label=(self.graphLabelName[i] + ' src'), color=self.colorsForGraph[i], linewidth=2.5)


                # plot interpolated experimental data
                self.axesNb.plot(self.NbXexp, self.interpNb[:, i], '-', label=(self.graphLabelName[i] + ' exp'),
                                 color=self.colorsForGraph[i], linewidth=5, alpha=0.5)
                self.axesSi.plot(self.SiXexp, self.interpSi[:, i], '-', label=(self.graphLabelName[i] + ' exp'),
                                 color=self.colorsForGraph[i], linewidth=5, alpha=0.5)

                self.axesNb.legend(shadow=True, fancybox=True, loc='upper left')
                self.axesSi.legend(shadow=True, fancybox=True, loc='upper left')
                plt.draw()
            self.fig.suptitle(
                'The mix ratio now is: $Si_{{{0}}}Nb_{{{1}}}$'.format(self.nSiNb[j, 0], self.nSiNb[j, 1],).replace(
                    '_', ' ').
                replace(' alpha', ', $\\alpha$').replace('gamma', '$\gamma$').replace(' blur', ', blur,'), fontsize=22)
            self.axesSi.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesSi.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesNb.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesNb.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesSi.grid(True)
            self.axesNb.grid(True)

            self.axesSi.axvline(x=self.calcBE_Si, linewidth=2, color='black')
            self.axesNb.axvline(x=self.calcBE_Nb, linewidth=2, color='black')

            self.axesSi.set_title('Si 2p', fontsize=20)
            self.axesNb.set_title('Nb 3d', fontsize=20)
            self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
            plt.draw()
            # save to the PNG file:
            # out_file_name = "norm(src_vs_shifted)__Si_%05.2f--Nb_%05.2f.png" % (self.nSiNb[j, 0], self.nSiNb[j, 1])
            # self.fig.savefig(os.path.join(self.out_dir, out_file_name))

        print(
            '-- > Images with calculated and src spectra after energy shifting procedure was saved')

    def plotSpectraSESSABeforeAndAfterFiltering(self):
        # test calculation spectra before and after filtering(blur or sharp):
        if self.blur_or_sharp in ['as_is']:
            pass
        else: # plot if filter was applied:

            self.fig.clf()
            gs = gridspec.GridSpec(1,2)

            self.axesNb = self.fig.add_subplot(gs[0,0])
            self.axesNb.invert_xaxis()
            self.axesNb.set_title('Nb')
            self.axesSi = self.fig.add_subplot(gs[0,1])
            self.axesSi.invert_xaxis()
            self.axesSi.set_title('Si')

            for axis in ['top','bottom','left','right']:
              self.axesSi.spines[axis].set_linewidth(2)
              self.axesNb.spines[axis].set_linewidth(2)
            # plt.subplots_adjust(top=0.85)
            # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
            self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

            # put window to the second monitor
            # figManager.window.setGeometry(1923, 23, 640, 529)
            self.figManager.window.setGeometry(1920, 20, 1920, 1180)

            plt.show()

            # test calculation spectra after filtering:
            for j in range(len(self.d)):
                self.axesNb.cla()
                self.axesSi.cla()
                for i in range(5):
                    self.axesNb.plot(self.Nbx, self.srcValuesFromSESSA_Nb[:, i, j], '--', label=(self.graphLabelName[i] + ' src'), color = self.colorsForGraph[i], linewidth=2.5)
                    self.axesSi.plot(self.Six, self.srcValuesFromSESSA_Si[:, i, j], '--', label=(self.graphLabelName[i] + ' src'), color = self.colorsForGraph[i], linewidth=2.5)
                    self.axesNb.plot(self.Nbx, self.Nbcalc[:, i, j], label = (self.graphLabelName[i] + ' ' + self.blur_or_sharp), color = self.colorsForGraph[i])
                    self.axesSi.plot(self.Six, self.Sicalc[:, i, j], label = (self.graphLabelName[i] + ' ' + self.blur_or_sharp), color = self.colorsForGraph[i])
                    self.axesNb.legend(shadow=True, fancybox=True, loc='upper left')
                    self.axesSi.legend(shadow=True, fancybox=True, loc='upper left')
                    plt.draw()
                self.fig.suptitle('The mix ratio now is: $Si_{{{0}}}Nb_{{{1}}}$\n{2}\n'.format(self.nSiNb[j,0], self.nSiNb[j,1], self.values_of_current_project).replace('_',' ').
                     replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur',', blur,'), fontsize=22)
                self.axesSi.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
                self.axesSi.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
                self.axesNb.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
                self.axesNb.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
                self.axesSi.grid(True)
                self.axesNb.grid(True)
                self.axesSi.set_title('Si 2p', fontsize=20)
                self.axesNb.set_title('Nb 3d', fontsize=20)
                self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
                plt.draw()
                # save to the PNG file:
                out_file_name = "src_vs_filtered__Si_%05.2f--Nb_%05.2f.png" %(self.nSiNb[j,0], self.nSiNb[j,1])
                self.fig.savefig( os.path.join(self.out_dir, out_file_name) )

            print('-- > Images with a comparison of calculated src spectra and calculated src spectra after filtering was saved')

    def plotSpectraExperimentalAndSESSAAfterFiltering(self):
        self.fig.clf()
        gs = gridspec.GridSpec(1,2)

        self.axesNb = self.fig.add_subplot(gs[0,0])
        self.axesNb.invert_xaxis()
        self.axesNb.set_title('Nb')
        self.axesSi = self.fig.add_subplot(gs[0,1])
        self.axesSi.invert_xaxis()
        self.axesSi.set_title('Si')

        for axis in ['top','bottom','left','right']:
          self.axesSi.spines[axis].set_linewidth(2)
          self.axesNb.spines[axis].set_linewidth(2)
        # plt.subplots_adjust(top=0.85)
        # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
        self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

        # put window to the second monitor
        # figManager.window.setGeometry(1923, 23, 640, 529)
        self.figManager.window.setGeometry(1920, 20, 1920, 1180)

        plt.show()

        # test again for normalizing calculation spectra after filtering:
        for j in range(len(self.d)):
            self.axesNb.cla()
            self.axesSi.cla()
            for i in range(5):
                # plot source calculated data:
                self.axesNb.plot(self.Nbx, self.srcValuesFromSESSA_Nb[:, i, j], '--', label=(self.graphLabelName[i] + ' src'), color = self.colorsForGraph[i], linewidth=2.5)
                self.axesSi.plot(self.Six, self.srcValuesFromSESSA_Si[:, i, j], '--', label=(self.graphLabelName[i] + ' src'), color = self.colorsForGraph[i], linewidth=2.5)

                # plot filtered calculated data:
                self.axesNb.plot(self.Nbx, self.Nbcalc[:, i, j], label = (self.graphLabelName[i] + ' ' + self.blur_or_sharp), color = self.colorsForGraph[i])
                self.axesSi.plot(self.Six, self.Sicalc[:, i, j], label = (self.graphLabelName[i] + ' ' + self.blur_or_sharp), color = self.colorsForGraph[i])

                # plot interpolated experimental data
                self.axesNb.plot(self.NbXexp, self.interpNb[:,i], '-', label=(self.graphLabelName[i] + ' exp'), color = self.colorsForGraph[i], linewidth=5, alpha = 0.5)
                self.axesSi.plot(self.SiXexp, self.interpSi[:,i], '-', label=(self.graphLabelName[i] + ' exp'), color = self.colorsForGraph[i], linewidth=5, alpha = 0.5)

                # # fill integrated area of interpolated experimental data
                self.axesNb.fill_between(self.NbXexp, y_in_region(self.NbXexp, self.interpNb[:, i], self.RIO_Nb), interpolate=True, color = self.colorsForGraph[i], alpha = 0.1)
                self.axesSi.fill_between(self.SiXexp, y_in_region(self.SiXexp, self.interpSi[:, i], self.RIO_Si), interpolate=True, color = self.colorsForGraph[i], alpha = 0.1)

                # fill integrated area of filtered calculated data
                self.axesNb.fill_between(self.Nbx, y_in_region(self.Nbx, self.Nbcalc[:, i, j], self.RIO_Nb), interpolate=True, color = self.colorsForGraph[i], alpha = 0.1)
                self.axesSi.fill_between(self.Six, y_in_region(self.Six, self.Sicalc[:, i, j], self.RIO_Si), interpolate=True, color = self.colorsForGraph[i], alpha = 0.1)

                self.axesNb.legend(shadow=True, fancybox=True, loc='upper left')
                self.axesSi.legend(shadow=True, fancybox=True, loc='upper left')
                plt.draw()
            self.fig.suptitle('The mix ratio now is: $Si_{{{0}}}Nb_{{{1}}}$\n{2}\n'.format(self.nSiNb[j,0], self.nSiNb[j,1], self.values_of_current_project).replace('_',' ').
                     replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur',', blur,'), fontsize=22)
            self.axesSi.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesSi.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesNb.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesNb.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesSi.grid(True)
            self.axesNb.grid(True)
            self.axesSi.set_title('Si 2p', fontsize=20)
            self.axesNb.set_title('Nb 3d', fontsize=20)
            self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
            plt.draw()
            # save to the PNG file:
            out_file_name = "norm(src_vs_filtered)__Si_%05.2f--Nb_%05.2f.png" %(self.nSiNb[j,0], self.nSiNb[j,1])
            self.fig.savefig( os.path.join(self.out_dir, out_file_name) )

        print('-- > Images with a comparison of calculated src spectra, normalized calculated spectra after filtering and raw experimental spectra was saved')

    def plotSpectraAndResiduals(self):
        self.fig.clf()
        gs = gridspec.GridSpec(3,2)

        self.axesNb = self.fig.add_subplot(gs[:-1,0])
        self.axesNb.invert_xaxis()
        self.axesNb.set_title('Nb')
        self.axesSi = self.fig.add_subplot(gs[:-1,1])
        self.axesSi.invert_xaxis()
        self.axesSi.set_title('Si')

        # for concentration and std
        self.axesNb_std = self.fig.add_subplot(gs[2,0])
        self.axesNb_std.set_title('std(Nb)')
        self.axesSi_std = self.fig.add_subplot(gs[2,1])
        self.axesSi_std.set_title('std(Si)')

        for axis in ['top','bottom','left','right']:
          self.axesSi.spines[axis].set_linewidth(2)
          self.axesNb.spines[axis].set_linewidth(2)
        # plt.subplots_adjust(top=0.85)
        # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
        self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

        # put window to the second monitor
        # figManager.window.setGeometry(1923, 23, 640, 529)
        self.figManager.window.setGeometry(1920, 20, 1920, 1180)

        plt.show()

        for j in range(len(self.d)):
            self.axesNb.cla()
            self.axesSi.cla()
            self.axesNb_std.cla()
            self.axesSi_std.cla()
            for i in range(5):
                # labelName =
                # plot experimental values:
                self.axesNb.plot(self.NbXexp, self.interpNb[:, i], '-', label=(self.graphLabelName[i] + ' exp'), color = self.colorsForGraph[i], linewidth=5, alpha = 0.5)
                # check the RIO_Nb:
                # axesNb.plot(NbXexp, y_in_region(NbXexp,interpNb[:,i],RIO_Nb), '-', label=(graphLabelName[i] + ' exp'), color = colorsForGraph[i], linewidth=5, alpha = 0.5)

                self.axesSi.plot(self.SiXexp, self.interpSi[:, i], '-', label=(self.graphLabelName[i] + ' exp'), color = self.colorsForGraph[i], linewidth=5, alpha = 0.5)
                # check the RIO_Si:
                # axesSi.plot(SiXexp,y_in_region(SiXexp, interpSi[:,i],RIO_Si), '-', label=(graphLabelName[i] + ' exp'), color = colorsForGraph[i], linewidth=5, alpha = 0.5)

                # axesNb.plot(Nbx, shirley_base(Nbx, interpNb[:,i]), label=graphLabelName[i])
                # axesNb.plot(Nbx, shirley_new(Nbx, interpNb[:,i], numpoints=100), label=graphLabelName[i])

                # plot calculated values:
                self.axesNb.plot(self.Nbx, self.Nbcalc[:, i, j], label=self.graphLabelName[i], color = self.colorsForGraph[i])
                self.axesSi.plot(self.Six, self.Sicalc[:, i, j], label=self.graphLabelName[i], color = self.colorsForGraph[i])

                plt.draw()
            # txtMix =  'The mix ratio now is: $Si_{%d}Nb_{%d}$' % (nSiNb[j,0], nSiNb[j,1])


            self.axesSi_std.plot(self.nSiNb[0: j+1, 0], self.residuals_stdSi_in_au[0: j+1], 'o', color='b')
            self.axesSi_std.plot(self.nSiNb[j, 0], self.residuals_stdSi_in_au[j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None',
                            markeredgewidth=3)
            self.axesSi_std.grid(True)
            self.axesSi_std.set_xlabel('part of Si', fontsize=14, fontweight='bold')
            self.axesSi_std.set_xlim([0, 1])
            self.axesSi_std.set_title('Residuals (Si)')

            self.axesNb_std.plot(self.nSiNb[0: j+1,1], self.residuals_stdNb_in_au[0:j+1], 'o', color='r')
            self.axesNb_std.plot(self.nSiNb[j, 1], self.residuals_stdNb_in_au[j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None',
                            markeredgewidth=3)
            self.axesNb_std.grid(True)
            self.axesNb_std.set_xlabel('part of Nb', fontsize=14, fontweight='bold')
            self.axesNb_std.set_xlim([0, 1])
            self.axesNb_std.set_title('Residuals (Nb)')

            txtMix =  'The mix ratio now is: $Si_{{{0}}}Nb_{{{1}}}$ \n'.format(self.nSiNb[j, 0], self.nSiNb[j, 1])

            # print ( 'The mix ratio now is: Si{0} Nb{1} \n'.format(self.nSiNb[j,0], self.nSiNb[j,1]) )

            self.fig.suptitle('The mix ratio now is: $Si_{{{0}}}Nb_{{{1}}}$\n{2}'.format(self.nSiNb[j,0], self.nSiNb[j,1], self.values_of_current_project).replace('_',' ').
                     replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur',', blur,'), fontsize=22)
            self.axesSi.set_title('Si 2p', fontsize=20)
            self.axesSi.legend(shadow=True, fancybox=True, loc='upper left')
            self.axesSi.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesSi.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesSi.set_ylim([0, 1])
            self.axesSi.set_xlim([105, 96])
            self.axesSi.tick_params(axis='both', which='major', labelsize=14)
            self.axesSi.tick_params(axis='both', which='minor', labelsize=12)
            self.axesSi.grid(True)
            self.axesSi.axvline(x=self.calcBE_Si, linewidth=2, color='black')

            self.axesNb.set_title('Nb 3d', fontsize=20)
            self.axesNb.legend(shadow=True, fancybox=True, loc='upper left')
            self.axesNb.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesNb.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesNb.set_ylim([0, 1])
            self.axesNb.set_xlim([208, 200])
            self.axesNb.tick_params(axis='both', which='major', labelsize=14)
            self.axesNb.tick_params(axis='both', which='minor', labelsize=12)
            self.axesNb.grid(True)
            self.axesNb.axvline(x=self.calcBE_Nb, linewidth=2, color='black')

            self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
            plt.draw()

            # fig.set_tight_layout(True)

            # save to the PNG file:
            out_file_name = "Si_%05.2f--Nb_%05.2f.png" %(self.nSiNb[j,0], self.nSiNb[j,1])
            self.fig.savefig( os.path.join(self.out_dir, out_file_name) )

        print('-> plotSpectraAndResiduals method was finished')


    def plotResiduals(self):
        # figManager.window.showMaximized()
        plt.clf()
        self.result_axes = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        # fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
        self.fig.suptitle('Differences between theoretical and experimental data\n{}'.format(self.values_of_current_project).replace('_',' ').
                     replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur',', blur,'), fontsize=22)

        if self.residualsType in 'integral':
            labelNameTxt1 = '$ RD(\mathbf{Si}) = \left \|{ \left \|{ \int{I_{exp}^{Si}(E)dE} } \\right \| - \left \|{ \int{I_{theor}^{Si}(E)dE} } \\right \| } \\right \| $'
            labelNameTxt2 = '$ RD(\mathbf{Nb}) = \left \|{ \left \|{ \int{I_{exp}^{Nb}(E)dE} } \\right \| - \left \|{ \int{I_{theor}^{Nb}(E)dE} } \\right \| } \\right \| $'
        elif self.residualsType in 'std':
            labelNameTxt1 = '$ RD(\mathbf{Si}) = STD $'
            labelNameTxt2 = '$ RD(\mathbf{Nb}) = STD $'

        self.result_axes.plot(self.nSiNb[:, 0],self.residuals_stdSi_in_au , 'o', markersize=10, color='b', alpha = 0.5,
                         label=labelNameTxt1)
        self.result_axes.plot(self.nSiNb[:, 0], self.residuals_stdNb_in_au, 'o', markersize=10, color='r', alpha = 0.5,
                         label=labelNameTxt2)
        self.result_axes.plot(self.nSiNb[:, 0], (self.residuals_stdSi_in_au + self.residuals_stdNb_in_au)/2, 'o',markersize=14, color='black', label='$\\frac{RD(\mathbf{Nb})+ RD(\mathbf{Si})}{2}$')

        self.result_axes.legend(shadow=True, fancybox=True, loc='best')
        self.result_axes.set_ylabel('Residuals (%)', fontsize=16, fontweight='bold')
        self.result_axes.set_xlabel('Concentration $x$ of Si ($Si_xNb_{1-x}$)', fontsize=16, fontweight='bold')
        self.result_axes.set_xlim([0, 1])
        # result_axes.set_xlim([105, 96])
        self.result_axes.tick_params(axis='both', which='major', labelsize=14)
        self.result_axes.tick_params(axis='both', which='minor', labelsize=12)
        self.result_axes.grid(True)
        plt.draw()

        # save to the PNG file:

        out_file_name = 'result_' + self.values_of_current_project
        self.fig.savefig( os.path.join(self.out_dir, out_file_name  + '.png') )
        self.fig.show()

        self.out_array = np.zeros((len(self.residuals_stdSi_in_au), 1+3))
        self.out_array[:, 0] = self.nSiNb[:, 0]

        self.out_array[:, 1] = self.residuals_stdSi_in_au.T
        self.out_array[:, 2] = self.residuals_stdNb_in_au.T
        self.out_array[:, 3] = (self.residuals_stdSi_in_au.T + self.residuals_stdNb_in_au.T)/2

        headerTxt = 'x\tRD(Si)\tRD(Nb)\t<RD>'
        np.savetxt(os.path.join(self.baseOutDirResiduals, 'residual_' + out_file_name +'.txt'), self.out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
        print('-> program was finished')

    def plotMeanOfResiduals(self):

        # load list of result_*.txt files from dir baseOutDirResiduals:
        filesFullPathName = listOfFilesFN_with_selected_ext(self.baseOutDirResiduals, ext = 'txt')
        if len(filesFullPathName)>0:

            i = 0
            numOfColumns = len(filesFullPathName)
            # load the first file to understand size of array:
            data = np.loadtxt(filesFullPathName[0], float)
            x = data[:, 0]
            numOfRows = len(x)
            RD = np.zeros((numOfRows, numOfColumns))
            RD_Si = np.zeros((numOfRows, numOfColumns))
            RD_Nb = np.zeros((numOfRows, numOfColumns))
            RD_std = np.zeros((numOfRows))
            RD_mean = np.zeros((numOfRows))

            RD_median = np.zeros((numOfRows))
            RD_max = np.zeros((numOfRows))
            RD_min = np.zeros((numOfRows))

            for f in filesFullPathName:
                # load data from the result_*.txt file:
                data = np.loadtxt(f, float)
                data = data[np.argsort(data[:,0])] # sort array by first column
                # help:
                # data[data[:,0].argsort()]
                # data[:,n] -- get entire column of index n
                # argsort() -- get the indices that would sort it
                # data[data[:,n].argsort()] -- get data array sorted by n-th column

                # select RD values eq x :
                if len(data[:, 0]) == numOfRows:
                    RD[:,i] = data[:,3]
                    RD_Si[:,i] = data[:,1]
                    RD_Nb[:,i] = data[:,2]
                else:
                    print('you have unexpected numbers of rows in your output files')
                    print('input file name is: ', f)

                i+=1

            x = data[:, 0]
            RD_std = np.std(RD[:,:],axis=1)
            RD_mean = np.mean(RD[:,:],axis=1)
            RD_median = np.median(RD[:,:],axis=1)
            RD_max    = np.amax(RD[:,:],axis=1)
            RD_min    = np.amin(RD[:,:],axis=1)


            self.RD_out_array = np.zeros((numOfRows, 3+3))
            self.RD_out_array[:, 0] = x
            self.RD_out_array[:, 1] = RD_mean
            self.RD_out_array[:, 2] = RD_std
            self.RD_out_array[:, 3] = RD_median
            self.RD_out_array[:, 4] = RD_max
            self.RD_out_array[:, 5] = RD_min

            # RD(Si):
            RD_Si_std    = np.std   (RD_Si[:,:],axis=1)
            RD_Si_mean   = np.mean  (RD_Si[:,:],axis=1)
            RD_Si_median = np.median(RD_Si[:,:],axis=1)
            RD_Si_max    = np.amax  (RD_Si[:,:],axis=1)
            RD_Si_min    = np.amin  (RD_Si[:,:],axis=1)


            self.RD_Si_out_array = np.zeros((numOfRows, 3+3))
            self.RD_Si_out_array[:, 0] = x
            self.RD_Si_out_array[:, 1] = RD_Si_mean
            self.RD_Si_out_array[:, 2] = RD_Si_std
            self.RD_Si_out_array[:, 3] = RD_Si_median
            self.RD_Si_out_array[:, 4] = RD_Si_max
            self.RD_Si_out_array[:, 5] = RD_Si_min

            # RD(Nb):
            RD_Nb_std    = np.std   (RD_Nb[:,:],axis=1)
            RD_Nb_mean   = np.mean  (RD_Nb[:,:],axis=1)
            RD_Nb_median = np.median(RD_Nb[:,:],axis=1)
            RD_Nb_max    = np.amax  (RD_Nb[:,:],axis=1)
            RD_Nb_min    = np.amin  (RD_Nb[:,:],axis=1)


            self.RD_Nb_out_array = np.zeros((numOfRows, 3+3))
            self.RD_Nb_out_array[:, 0] = x
            self.RD_Nb_out_array[:, 1] = RD_Nb_mean
            self.RD_Nb_out_array[:, 2] = RD_Nb_std
            self.RD_Nb_out_array[:, 3] = RD_Nb_median
            self.RD_Nb_out_array[:, 4] = RD_Nb_max
            self.RD_Nb_out_array[:, 5] = RD_Nb_min

            outDirPath = create_out_data_folder(self.baseOutDirResiduals, first_part_of_folder_name = 'RD_rslt')
            if  not (os.path.isdir(outDirPath)):
                        os.makedirs(outDirPath, exist_ok=True)

            # save RD results to the *.dat file:
            out_array = self.RD_out_array
            case_of_calc = 'rd'
            headerTxt = 'k\t<RD>\tstd\tRD_median\tRD_max\tRD_min'
            np.savetxt(os.path.join(outDirPath, 'RD_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y = RD_mean,
                     error = RD_std,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     case = case_of_calc,
                     labelStartName = 'RD',
                     y_median= RD_median,
                     y_max=RD_max,
                     y_min=RD_min)

            # save RD(Si) results to the *.dat file:
            out_array = self.RD_Si_out_array
            case_of_calc = 'rd(Si)'
            headerTxt = 'k\t<RD(Si)>\tstd\tRD(Si)_median\tRD(Si)_max\tRD(Si)_min'
            np.savetxt(os.path.join(outDirPath, 'RD(Si)_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y = RD_Si_mean,
                     error = RD_Si_std,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     case = case_of_calc,
                     labelStartName = 'RD(Si)',
                     y_median= RD_Si_median,
                     y_max=RD_Si_max,
                     y_min=RD_Si_min)

            # save RD(Nb) results to the *.dat file:
            out_array = self.RD_Nb_out_array
            case_of_calc = 'rd(Nb)'
            headerTxt = 'k\t<RD(Nb)>\tstd\tRD(Nb)_median\tRD(Nb)_max\tRD(Nb)_min'
            np.savetxt(os.path.join(outDirPath, 'RD(Nb)_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y = RD_Nb_mean,
                     error = RD_Nb_std,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     case = case_of_calc,
                     labelStartName = 'RD(Nb)',
                     y_median= RD_Nb_median,
                     y_max=RD_Nb_max,
                     y_min=RD_Nb_min)


            print('-> <RD>, <RD(Si)>, <RD(Nb)> was calculated')

    def saveArrayToASCII(self):
        '''
        export data to the ASCII tables
        :return:
        '''

        self.Nb_out_array = np.zeros((len(self.Nbx), 5 + 1))
        self.Nb_out_array[:, 0] = self.Nbx

        self.Nbexp_out_array = np.zeros((len(self.NbXexp), 5 + 1))
        self.Nbexp_out_array[:, 0] = self.NbXexp
        self.Siexp_out_array = np.zeros((len(self.SiXexp), 5 + 1))
        self.Siexp_out_array[:, 0] = self.SiXexp

        self.Si_out_array = np.zeros((len(self.Six), 5 + 1))
        self.Si_out_array[:, 0] = self.Six

        # save Experimental Data:
        headerTxt='BE(eV)\t'
        for i in range(5):
            headerTxt = headerTxt + self.graphLabelName[i] + '\t'
            self.Nbexp_out_array[:, i + 1] = self.interpNb[:, i]
            self.Siexp_out_array[:, i + 1] = self.interpSi[:, i]
        headerTxt = headerTxt+'\n'
        # save to the DAT file:
        startTxt = 'Nb_experimental'
        out_array = self.Nbexp_out_array
        out_file_name = startTxt + ".dat"
        np.savetxt(os.path.join(self.out_dir, out_file_name), out_array, fmt='%1.6e', delimiter='\t',
                   header=headerTxt)
        startTxt = 'Si_experimental'
        out_array = self.Siexp_out_array
        out_file_name = startTxt + ".dat"
        np.savetxt(os.path.join(self.out_dir, out_file_name), out_array, fmt='%1.6e', delimiter='\t',
                   header=headerTxt)

        # save Theoretical Data:
        for j in range(len(self.d)):
            headerTxt='BE(eV)\t'
            for i in range(5):
                headerTxt = headerTxt + self.graphLabelName[i] + '\t'

                self.Nb_out_array[:, i + 1] = self.Nbcalc[:, i, j]
                self.Si_out_array[:, i + 1] = self.Sicalc[:, i, j]


            headerTxt = headerTxt+'\n'

            # save to the DAT file:
            startTxt = 'Nb_theor_'
            out_array = self.Nb_out_array
            out_file_name = startTxt + "Si_%05.2f--Nb_%05.2f.dat" % (self.nSiNb[j, 0], self.nSiNb[j, 1])
            np.savetxt(os.path.join(self.out_dir, out_file_name), out_array, fmt='%1.6e', delimiter='\t',
                       header=headerTxt)
            startTxt = 'Si_theor_'
            out_array = self.Si_out_array
            out_file_name = startTxt + "Si_%05.2f--Nb_%05.2f.dat" % (self.nSiNb[j, 0], self.nSiNb[j, 1])
            np.savetxt(os.path.join(self.out_dir, out_file_name), out_array, fmt='%1.6e', delimiter='\t',
                       header=headerTxt)
        print('-> Experimental and Theoretical Data has been saved')

if __name__ == "__main__":
    print ('-> you run ',  __file__, ' file in a main mode' )
    a = WorkWithXPSSpectra()
    a.loadSESSAspectra()
    a.plotMeanOfResiduals()


