'''
Load and compare only experimental spectra with a one (single) calculated SESSA model
'''
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

from libs.dir_and_file_operations import *
from libs.plot_data import plotData

from libs.load_and_compare_data import WorkWithXPSSpectra, defLabelFromFileName, etchTimeFromFileName

class CompareTwoModels (WorkWithXPSSpectra):
    def __init__(self):
        super(CompareTwoModels, self).__init__()
        self.wantSpectraAndRatios = True
        self.dataPath = "/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/together_refSpectra/"


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

        i = 0
        j = 0
        # set the values for graphs label name like: '0 min' instead of '00'
        self.graphLabelName = []
        etchTime = []
        self.uniqParameter = []  # sort the list of folder names:
        neededFolders = list(k for k in self.dirPathList if self.uniqPartNameOfSESSACalcDirs in k)
        parameter = list(int(float(re.findall("\d+", k)[0]) * 100) for k in neededFolders)
        sortedlist = [i[0] for i in sorted(zip(neededFolders, parameter), key=lambda l: l[1], reverse=False)]
        for folderName in sortedlist:
            # check the 'out_' folders only
            if self.uniqPartNameOfSESSACalcDirs in folderName:
                # tmpParameter = re.findall("\d+\.\d+", folderName)
                # str within {*}
                # tmpParameter = re.findall("\{(\w+)\}", folderName)
                tmpParameter = folderName[folderName.find("{")+1:folderName.find("}")]
                self.uniqParameter.append(tmpParameter) #Si
                folderFullName = os.path.join(self.dataPath, folderName)
                for file in sorted(file for file in sorted(os.listdir(folderFullName)) if
                                   file.startswith('Si') and file.endswith(".dat")):
                    # print('Si:', os.path.join(folderFullName, file))
                    data = pd.read_csv(os.path.join(folderFullName, file), comment='#', header=None, delimiter='\t',
                                       names=('Energy', 'Intensity', 'NaN'))
                    data['Energy'] = 1486.6 - data['Energy']
                    self.Six = data['Energy'].values
                    self.Sicalc[:, i, j] = data['Intensity'].values
                    i += 1
                i = 0
                for file in sorted(file for file in sorted(os.listdir(folderFullName)) if
                                   file.startswith('Nb') and file.endswith(".dat")):
                    # print('Nb:', os.path.join(folderFullName, file))
                    data = pd.read_csv(os.path.join(folderFullName, file), comment='#', header=None, delimiter='\t',
                                       names=('Energy', 'Intensity', 'NaN'))
                    data['Energy'] = 1486.6 - data['Energy']
                    self.Nbx = data['Energy'].values
                    self.Nbcalc[:, i, j] = data['Intensity'].values
                    self.graphLabelName.append(defLabelFromFileName(file))
                    etchTime.append(etchTimeFromFileName(file))

                    i += 1

                j += 1
                i = 0
        # number of cases (folders):
        self.numOfCases = np.r_[1: len(self.d)+1: 1]
        u, idx = np.unique(etchTime, return_index=True)
        self.etchTime = u[np.argsort(idx)]

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
        self.expBE_Si = self.Six[self.interpSi[:, 1].argmax()]
        self.deltaBE_Si = self.expBE_Si - self.calcBE_Si
        # self.deltaBE_Si = 0.0
        print(
         'calcBE_Si= {0:.5}, expBE_Si={1:.5}, delta={2:.5}'.format(self.calcBE_Si, self.expBE_Si, self.deltaBE_Si))

        self.calcBE_Nb = self.Nbx[self.Nbcalc[:, 3, 0].argmax()]
        self.expBE_Nb = self.Nbx[self.interpNb[:, 3].argmax()]
        self.deltaBE_Nb = self.expBE_Nb - self.calcBE_Nb - 0.08
        print(
         'calcBE_Nb= {0:.5}, expBE_Nb={1:.5}, delta={2:.5}'.format(self.calcBE_Nb, self.expBE_Nb, self.deltaBE_Nb))

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
                    self.Nbcalc[:, i, j] = smooth_by_window(self.Nbcalc[:, i, j], window_len=self.window_len,
                                                             window = self.window_name, alpha=self.alpha,
                                                             gamma = self.gamma, blur_or_sharp=self.blur_or_sharp)
                    self.Nbcalc[:, i, j] = y_in_region (self.Nbx, self.Nbcalc[:, i, j], region=self.RIO_Nb)

                    self.Sicalc[:, i, j] = smooth_by_window(self.Sicalc[:, i, j], window_len=self.window_len,
                                                             window = self.window_name, alpha=self.alpha,
                                                             gamma = self.gamma, blur_or_sharp=self.blur_or_sharp)
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
        # create a base out dir for set of calculated ratios:
        self.baseOutDirRatios = createFolder( os.path.join((self.baseOutDir), 'set_of_ratios') )
        # create unique name for calculated data cases:
        self.name_of_out_folder = 'calc_' + self.values_of_current_project
        # create 0001-type of subdirectory inside unique subdirectory:
        self.out_dir = create_out_data_folder( os.path.join(self.baseOutDir, self.name_of_out_folder) )

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

        # calculate the ratio between max Intensity and Area for spectra theor and experiment:
        self.ratioMaxIntensityNb = np.zeros((5, len(self.d))) # 5 curves and d cases
        self.ratioMaxIntensitySi = np.zeros((5, len(self.d)))

        #  SubMax - ratio between max of current time cases Exper and Theor curves
        self.ratioSubMaxIntensityNb = np.zeros((5, len(self.d))) # 5 curves and d cases
        self.ratioSubMaxIntensitySi = np.zeros((5, len(self.d)))

        self.ratioMaxAreaNb = np.zeros((5, len(self.d))) # 5 curves and d cases
        self.ratioMaxAreaSi = np.zeros((5, len(self.d)))

        #  SubMax - ratio between max of current time cases Exper and Theor curves
        self.ratioSubAreaNb = np.zeros((5, len(self.d))) # 5 curves and d cases
        self.ratioSubAreaSi = np.zeros((5, len(self.d)))

        self.areaNbExper = np.zeros((5))
        self.areaNbTheor = np.zeros((5, len(self.d)))

        self.areaSiExper = np.zeros((5))
        self.areaSiTheor = np.zeros((5, len(self.d)))

        # Calculate area values:
        self.areaNbExper[:] = np.abs( get_integral_in_region(self.NbXexp, self.interpNb, self.RIO_Nb) )
        self.areaSiExper[:] = np.abs( get_integral_in_region(self.SiXexp, self.interpSi, self.RIO_Si) )

        for j in range(len(self.d)):

                 self.areaNbTheor[:, j] = np.abs( get_integral_in_region(self.Nbx, self.Nbcalc[:, :, j], self.RIO_Nb) )
                 self.areaSiTheor[:, j] = np.abs( get_integral_in_region(self.Six, self.Sicalc[:, :, j], self.RIO_Si) )

        # Calculate Ratio values:
        for j in range(len(self.d)):
            self.ratioMaxAreaNb[:, j] = self.areaNbTheor[:, j] / self.areaNbExper[:].max()
            self.ratioMaxAreaSi[:, j] = self.areaSiTheor[:, j] / self.areaSiExper[:].max()

            self.ratioSubAreaNb[:, j] = self.areaNbTheor[:, j] / self.areaNbExper[:]
            self.ratioSubAreaSi[:, j] = self.areaSiTheor[:, j] / self.areaSiExper[:]
            for i in range(5): # time cases
                self.ratioMaxIntensityNb[i, j] = self.Nbcalc[:, i, j].max() / 1.0
                self.ratioMaxIntensitySi[i, j] = self.Sicalc[:, i, j].max() / 1.0

                self.ratioSubMaxIntensityNb[i, j] = self.Nbcalc[:, i, j].max() / self.interpNb[:, i].max()
                self.ratioSubMaxIntensitySi[i, j] = self.Sicalc[:, i, j].max() / self.interpSi[:, i].max()

        if self.wantSpectraAndRatios:
            # plot if needed:
            self.plotSpectraAndRatios()

        if self.wantSpectraAndResiduals:
            # plot if needed:
            self.plotSpectraAndResiduals()

        # plot main graph:
        self.plotResiduals()

    def plotSpectraSESSABeforeAndAfterFiltering(self):
        # test calculation spectra before and after filtering(blur or sharp):
        if self.blur_or_sharp in ['as_is']:
            pass
        else: # plot if filter was applied:

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
                self.fig.suptitle('The parameter value is: ${0}$, case # {1}\n{2}'.format(self.uniqParameter[j], j,
                     self.values_of_current_project).replace('_', ' ').
                     replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur', ', blur,'), fontsize=22)
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
                out_file_name = "src_vs_filtered__p={0}_{{{1}}}.png".format(j, self.uniqParameter[j])
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

        for axis in ['top', 'bottom', 'left', 'right']:
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
            self.fig.suptitle('The parameter value is: ${0}$, case # {1}\n{2}'.format(self.uniqParameter[j], j,
                     self.values_of_current_project).replace('_', ' ').
                     replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur', ', blur,'), fontsize=22)
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
            out_file_name = "norm(src_vs_filtered)__p={0}_{{{1}}}.png".format(j, self.uniqParameter[j])
            self.fig.savefig( os.path.join(self.out_dir, out_file_name) )

        print('-- > Images with a comparison of calculated src spectra, normalized calculated spectra after filtering and raw experimental spectra was saved')

    def plotSpectraAndRatios(self):
        self.fig.clf()
        gs = gridspec.GridSpec(3, 4)

        self.axesNb = self.fig.add_subplot(gs[0, 0:2])
        self.axesNb.invert_xaxis()
        self.axesNb.set_title('Nb')
        self.axesSi = self.fig.add_subplot(gs[0, 2:])
        self.axesSi.invert_xaxis()
        self.axesSi.set_title('Si')

        # for concentration and std
        self.axesNb_0 = self.fig.add_subplot(gs[1, 0])
        self.axesNb_0.set_title('$I_{MAX}^{Nb}$')
        self.axesNb_1 = self.fig.add_subplot(gs[1, 1])
        self.axesNb_1.set_title('$I_{subMAX}^{Nb}$')
        self.axesNb_2 = self.fig.add_subplot(gs[2, 0])
        self.axesNb_2.set_title('$S_{MAX}^{Nb}$')
        self.axesNb_3 = self.fig.add_subplot(gs[2, 1])
        self.axesNb_3.set_title('$S_{subMAX}^{Nb}$')



        self.axesSi_0 = self.fig.add_subplot(gs[1, 2])
        self.axesSi_0.set_title('$I_{MAX}^{Si}$')
        self.axesSi_1 = self.fig.add_subplot(gs[1, 3])
        self.axesSi_1.set_title('$I_{subMAX}^{Si}$')
        self.axesSi_2 = self.fig.add_subplot(gs[2, 2])
        self.axesSi_2.set_title('$S_{MAX}^{Si}$')
        self.axesSi_3 = self.fig.add_subplot(gs[2, 3])
        self.axesSi_3.set_title('$S_{subMAX}^{Si}$')

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


            # on std axes we want to plot cases line together:
            # self.axesNb_std.cla()
            # self.axesSi_std.cla()
            for i in range(5):
                self.axesNb_0.cla()
                self.axesNb_1.cla()
                self.axesNb_2.cla()
                self.axesNb_3.cla()
                self.axesSi_0.cla()
                self.axesSi_1.cla()
                self.axesSi_2.cla()
                self.axesSi_3.cla()
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
                self.axesNb.plot(self.Nbx, self.Nbcalc[:, i, j], label=self.graphLabelName[i], color=self.colorsForGraph[i])
                self.axesSi.plot(self.Six, self.Sicalc[:, i, j], label=self.graphLabelName[i], color=self.colorsForGraph[i])

                # -------------------------------
                # Plot subplots with ratio values:
                self.axesSi_0.plot(self.etchTime[0: i+1], self.ratioMaxIntensitySi[0: i+1, j], 'o', color='b')
                self.axesSi_0.plot(self.etchTime[i], self.ratioMaxIntensitySi[i, j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None', markeredgewidth=3)
                self.axesSi_0.grid(True)
                self.axesSi_0.set_xlabel('etching time (min)', fontsize=14, fontweight='bold')
                self.axesSi_0.set_xlim([0, 25])
                self.axesSi_0.set_title('ratio $I_{MAX}^{Si}$')

                self.axesNb_0.plot(self.etchTime[0: i+1], self.ratioMaxIntensityNb[0: i+1, j], 'o', color='r')
                self.axesNb_0.plot(self.etchTime[i], self.ratioMaxIntensityNb[i, j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None', markeredgewidth=3)
                self.axesNb_0.grid(True)
                self.axesNb_0.set_xlabel('etching time (min)', fontsize=14, fontweight='bold')
                self.axesNb_0.set_xlim([0, 25])
                self.axesNb_0.set_title('ratio $I_{MAX}^{Nb}$')

                self.axesSi_1.plot(self.etchTime[0: i+1], self.ratioSubMaxIntensitySi[0: i+1, j], 'o', color='b')
                self.axesSi_1.plot(self.etchTime[i], self.ratioSubMaxIntensitySi[i, j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None',markeredgewidth=3)
                self.axesSi_1.grid(True)
                self.axesSi_1.set_xlabel('etching time (min)', fontsize=14, fontweight='bold')
                self.axesSi_1.set_xlim([0, 25])
                self.axesSi_1.set_title('ratio $I_{subMAX}^{Si}$')

                self.axesNb_1.plot(self.etchTime[0: i+1], self.ratioSubMaxIntensityNb[0: i+1, j], 'o', color='r')
                self.axesNb_1.plot(self.etchTime[i], self.ratioSubMaxIntensityNb[i, j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None', markeredgewidth=3)
                self.axesNb_1.grid(True)
                self.axesNb_1.set_xlabel('etching time (min)', fontsize=14, fontweight='bold')
                self.axesNb_1.set_xlim([0, 25])
                self.axesNb_1.set_title('ratio $I_{subMAX}^{Nb}$')

                self.axesSi_2.plot(self.etchTime[0: i+1], self.ratioMaxAreaSi[0: i+1, j], 'o', color='b')
                self.axesSi_2.plot(self.etchTime[i], self.ratioMaxAreaSi[i, j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None',markeredgewidth=3)
                self.axesSi_2.grid(True)
                self.axesSi_2.set_xlabel('etching time (min)', fontsize=14, fontweight='bold')
                self.axesSi_2.set_xlim([0, 25])
                self.axesSi_2.set_title('ratio $S_{MAX}^{Si}$')

                self.axesNb_2.plot(self.etchTime[0: i+1], self.ratioMaxAreaNb[0: i+1, j], 'o', color='r')
                self.axesNb_2.plot(self.etchTime[i], self.ratioMaxAreaNb[i, j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None', markeredgewidth=3)
                self.axesNb_2.grid(True)
                self.axesNb_2.set_xlabel('etching time (min)', fontsize=14, fontweight='bold')
                self.axesNb_2.set_xlim([0, 25])
                self.axesNb_2.set_title('ratio $S_{MAX}^{Nb}$')

                self.axesSi_3.plot(self.etchTime[0: i+1], self.ratioSubAreaSi[0: i+1, j], 'o', color='b')
                self.axesSi_3.plot(self.etchTime[i], self.ratioSubAreaSi[i, j], 'o', markeredgecolor='red', markersize=20, markerfacecolor ='None', markeredgewidth=3)
                self.axesSi_3.grid(True)
                self.axesSi_3.set_xlabel('etching time (min)', fontsize=14, fontweight='bold')
                self.axesSi_3.set_xlim([0, 25])
                self.axesSi_3.set_title('ratio $S_{subMAX}^{Si}$')

                self.axesNb_3.plot(self.etchTime[0: i+1], self.ratioSubAreaNb[0: i+1, j], 'o', color='r')
                self.axesNb_3.plot(self.etchTime[i], self.ratioSubAreaNb[i, j], 'o', markeredgecolor='red', markersize=20, markerfacecolor ='None', markeredgewidth=3)
                self.axesNb_3.grid(True)
                self.axesNb_3.set_xlabel('etching time (min)', fontsize=14, fontweight='bold')
                self.axesNb_3.set_xlim([0, 25])
                self.axesNb_3.set_title('ratio $S_{subMAX}^{Nb}$')


                plt.draw()


            txtMix =  'The parameter now is: ${}$ \n'.format(self.uniqParameter[j])

            # print ( 'The mix ratio now is: Si{0} Nb{1} \n'.format(self.nSiNb[j,0], self.nSiNb[j,1]) )

            self.fig.suptitle('The parameter now is: ${0}$, case #{1}\n{2}'.format(self.uniqParameter[j], j, self.values_of_current_project).replace('_', ' ').
                     replace(' alpha', ', $\\alpha$').replace('gamma', '$\gamma$').replace(' blur', ', blur,'), fontsize=22)
            self.axesSi.set_title('Si 2p', fontsize=20)
            self.axesSi.legend(shadow=True, fancybox=True, loc='upper left')
            self.axesSi.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesSi.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesSi.set_ylim([0, 1])
            self.axesSi.set_xlim([105, 96])
            self.axesSi.tick_params(axis='both', which='major', labelsize=14)
            self.axesSi.tick_params(axis='both', which='minor', labelsize=12)
            self.axesSi.grid(True)

            self.axesNb.set_title('Nb 3d', fontsize=20)
            self.axesNb.legend(shadow=True, fancybox=True, loc='upper left')
            self.axesNb.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesNb.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesNb.set_ylim([0, 1])
            self.axesNb.set_xlim([208, 200])
            self.axesNb.tick_params(axis='both', which='major', labelsize=14)
            self.axesNb.tick_params(axis='both', which='minor', labelsize=12)
            self.axesNb.grid(True)

            self.axesSi.axvline(x=self.calcBE_Si, linewidth=2, color='black')
            self.axesNb.axvline(x=self.calcBE_Nb, linewidth=2, color='black')


            self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
            plt.draw()

            # fig.set_tight_layout(True)

            # save to the PNG file:
            out_file_name = "10_plots_p={0}_{{{1}}}.png".format(j, self.uniqParameter[j])
            self.fig.savefig( os.path.join(self.out_dir, out_file_name) )

            # save output txt file for each cases:
            self.out_array = np.zeros((len(self.etchTime), 1+8))
            self.out_array[:, 0] = self.etchTime[:]

            self.out_array[:, 1] = self.ratioMaxIntensitySi[:, j]
            self.out_array[:, 2] = self.ratioMaxIntensityNb[:, j]

            self.out_array[:, 3] = self.ratioSubMaxIntensitySi[:, j]
            self.out_array[:, 4] = self.ratioSubMaxIntensityNb[:, j]

            self.out_array[:, 5] = self.ratioMaxAreaSi[:, j]
            self.out_array[:, 6] = self.ratioMaxAreaNb[:, j]

            self.out_array[:, 7] = self.ratioSubAreaSi[:, j]
            self.out_array[:, 8] = self.ratioSubAreaNb[:, j]

            out_file_name = 'result_' + self.values_of_current_project + '_p={{{0}}}'.format(self.uniqParameter[j])
            headerTxt = 'time(min)\tImax(Si)\tImax(Nb)\tIsub(Si)\tIsub(Nb)\tSmax(Si)\tSmax(Nb)\tSsub(Si)\tSsub(Nb)'
            np.savetxt(os.path.join(self.baseOutDirRatios, 'ratios_' + out_file_name +'.txt'),
                       self.out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)


        print('-> plotSpectraAndResiduals method was finished')
    def plotSpectraAndResiduals(self):
        self.fig.clf()
        gs = gridspec.GridSpec(3, 2)

        self.axesNb = self.fig.add_subplot(gs[:-1, 0])
        self.axesNb.invert_xaxis()
        self.axesNb.set_title('Nb')
        self.axesSi = self.fig.add_subplot(gs[:-1, 1])
        self.axesSi.invert_xaxis()
        self.axesSi.set_title('Si')

        # for concentration and std
        self.axesNb_std = self.fig.add_subplot(gs[2, 0])
        self.axesNb_std.set_title('std(Nb)')
        self.axesSi_std = self.fig.add_subplot(gs[2, 1])
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


            self.axesSi_std.plot(self.numOfCases[0: j+1], self.residuals_stdSi_in_au[0: j+1], 'o', color='b')
            self.axesSi_std.plot(self.numOfCases[j], self.residuals_stdSi_in_au[j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None',
                            markeredgewidth=3)
            self.axesSi_std.grid(True)
            self.axesSi_std.set_xlabel('case number', fontsize=14, fontweight='bold')
            self.axesSi_std.set_xlim([-1, len(self.d)+1])
            self.axesSi_std.set_title('Residuals (Si)')

            self.axesNb_std.plot(self.numOfCases[0: j+1], self.residuals_stdNb_in_au[0:j+1], 'o', color='r')
            self.axesNb_std.plot(self.numOfCases[j], self.residuals_stdNb_in_au[j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None',
                            markeredgewidth=3)
            self.axesNb_std.grid(True)
            self.axesNb_std.set_xlabel('case number', fontsize=14, fontweight='bold')
            self.axesNb_std.set_xlim([-1, len(self.d)+1])
            self.axesNb_std.set_title('Residuals (Nb)')

            self.fig.suptitle('The parameter now is: ${0}$, case #{1}\n{2}'.format(self.uniqParameter[j], j, self.values_of_current_project).replace('_', ' ').
                     replace(' alpha', ', $\\alpha$').replace('gamma', '$\gamma$').replace(' blur', ', blur,'), fontsize=22)
            self.axesSi.set_title('Si 2p', fontsize=20)
            self.axesSi.legend(shadow=True, fancybox=True, loc='upper left')
            self.axesSi.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesSi.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesSi.set_ylim([0, 1])
            self.axesSi.set_xlim([105, 96])
            self.axesSi.tick_params(axis='both', which='major', labelsize=14)
            self.axesSi.tick_params(axis='both', which='minor', labelsize=12)
            self.axesSi.grid(True)

            self.axesNb.set_title('Nb 3d', fontsize=20)
            self.axesNb.legend(shadow=True, fancybox=True, loc='upper left')
            self.axesNb.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.axesNb.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.axesNb.set_ylim([0, 1])
            self.axesNb.set_xlim([208, 200])
            self.axesNb.tick_params(axis='both', which='major', labelsize=14)
            self.axesNb.tick_params(axis='both', which='minor', labelsize=12)
            self.axesNb.grid(True)

            self.axesSi.axvline(x=self.calcBE_Si, linewidth=2, color='black')
            self.axesNb.axvline(x=self.calcBE_Nb, linewidth=2, color='black')

            self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
            plt.draw()

            # fig.set_tight_layout(True)

            # save to the PNG file:
            out_file_name = "3_plots_p={0}_{{{1}}}.png".format(j, self.uniqParameter[j])
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

        self.result_axes.plot(self.numOfCases[:], self.residuals_stdSi_in_au , 'o', markersize=10, color='b', alpha = 0.5,
                         label=labelNameTxt1)
        self.result_axes.plot(self.numOfCases[:], self.residuals_stdNb_in_au, 'o', markersize=10, color='r', alpha = 0.5,
                         label=labelNameTxt2)
        self.result_axes.plot(self.numOfCases[:], (self.residuals_stdSi_in_au + self.residuals_stdNb_in_au)/2, 'o',markersize=14, color='black', label='$\\frac{RD(\mathbf{Nb})+ RD(\mathbf{Si})}{2}$')

        self.result_axes.legend(shadow=True, fancybox=True, loc='best')
        self.result_axes.set_ylabel('Residuals (%)', fontsize=16, fontweight='bold')
        self.result_axes.set_xlabel('case number)', fontsize=16, fontweight='bold')
        self.result_axes.set_xlim([-1, len(self.d)+1])
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
        self.out_array[:, 0] = self.numOfCases[:].T

        self.out_array[:, 1] = self.residuals_stdSi_in_au.T
        self.out_array[:, 2] = self.residuals_stdNb_in_au.T
        self.out_array[:, 3] = (self.residuals_stdSi_in_au.T + self.residuals_stdNb_in_au.T)/2

        headerTxt = 'x\tRD(Si)\tRD(Nb)\t<RD>'
        np.savetxt(os.path.join(self.baseOutDirResiduals, 'residual_' + out_file_name +'.txt'), self.out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
        print('-> program was finished')

    def plotMeanOfRatios(self):

        # load list of result_*.txt files from dir baseOutDirResiduals:
        filesFullPathName = listOfFilesFN_with_selected_ext(self.baseOutDirRatios, ext = 'txt')
        if len(filesFullPathName)>0:

            i = 0
            numOfColumns = len(filesFullPathName)
            # load the first file to understand size of array:
            data = np.loadtxt(filesFullPathName[0], float)
            x = data[:, 0]
            numOfRows = len(x)

            Imax_Si = np.zeros((numOfRows, numOfColumns))
            Isub_Si = np.zeros((numOfRows, numOfColumns))
            Smax_Si = np.zeros((numOfRows, numOfColumns))
            Ssub_Si = np.zeros((numOfRows, numOfColumns))
            Imax_Nb = np.zeros((numOfRows, numOfColumns))
            Isub_Nb = np.zeros((numOfRows, numOfColumns))
            Smax_Nb = np.zeros((numOfRows, numOfColumns))
            Ssub_Nb = np.zeros((numOfRows, numOfColumns))

            Imax_Si_mean = np.zeros((numOfRows))
            Isub_Si_mean = np.zeros((numOfRows))
            Smax_Si_mean = np.zeros((numOfRows))
            Ssub_Si_mean = np.zeros((numOfRows))
            Imax_Nb_mean = np.zeros((numOfRows))
            Isub_Nb_mean = np.zeros((numOfRows))
            Smax_Nb_mean = np.zeros((numOfRows))
            Ssub_Nb_mean = np.zeros((numOfRows))

            Imax_Si_median = np.zeros((numOfRows))
            Isub_Si_median = np.zeros((numOfRows))
            Smax_Si_median = np.zeros((numOfRows))
            Ssub_Si_median = np.zeros((numOfRows))
            Imax_Nb_median = np.zeros((numOfRows))
            Isub_Nb_median = np.zeros((numOfRows))
            Smax_Nb_median = np.zeros((numOfRows))
            Ssub_Nb_median = np.zeros((numOfRows))

            Imax_Si_std = np.zeros((numOfRows))
            Isub_Si_std = np.zeros((numOfRows))
            Smax_Si_std = np.zeros((numOfRows))
            Ssub_Si_std = np.zeros((numOfRows))
            Imax_Nb_std = np.zeros((numOfRows))
            Isub_Nb_std = np.zeros((numOfRows))
            Smax_Nb_std = np.zeros((numOfRows))
            Ssub_Nb_std = np.zeros((numOfRows))

            Imax_Si_max = np.zeros((numOfRows))
            Isub_Si_max = np.zeros((numOfRows))
            Smax_Si_max = np.zeros((numOfRows))
            Ssub_Si_max = np.zeros((numOfRows))
            Imax_Nb_max = np.zeros((numOfRows))
            Isub_Nb_max = np.zeros((numOfRows))
            Smax_Nb_max = np.zeros((numOfRows))
            Ssub_Nb_max = np.zeros((numOfRows))

            Imax_Si_min = np.zeros((numOfRows))
            Isub_Si_min = np.zeros((numOfRows))
            Smax_Si_min = np.zeros((numOfRows))
            Ssub_Si_min = np.zeros((numOfRows))
            Imax_Nb_min = np.zeros((numOfRows))
            Isub_Nb_min = np.zeros((numOfRows))
            Smax_Nb_min = np.zeros((numOfRows))
            Ssub_Nb_min = np.zeros((numOfRows))

            # ---------------------------------
            # create output folder for results
            # save RD results to the *.dat file:
            outDirPath = create_out_data_folder(self.baseOutDirRatios, first_part_of_folder_name = 'RD_rslt')
            if  not (os.path.isdir(outDirPath)):
                        os.makedirs(outDirPath, exist_ok=True)

            # scan directory and load data:
            for f in filesFullPathName:
                # load data from the result_*.txt file:
                data = np.loadtxt(f, float)
                data = data[np.argsort(data[:, 0])] # sort array by first column
                # help:
                # data[data[:,0].argsort()]
                # data[:,n] -- get entire column of index n
                # argsort() -- get the indices that would sort it
                # data[data[:,n].argsort()] -- get data array sorted by n-th column

                # select RD values eq x :
                if len(data[:, 0]) == numOfRows:
                    Imax_Si[:, i] = data[:, 1]
                    Isub_Si[:, i] = data[:, 3]
                    Smax_Si[:, i] = data[:, 5]
                    Ssub_Si[:, i] = data[:, 7]
                    Imax_Nb[:, i] = data[:, 2]
                    Isub_Nb[:, i] = data[:, 4]
                    Smax_Nb[:, i] = data[:, 6]
                    Ssub_Nb[:, i] = data[:, 8]
                else:
                    print('you have unexpected numbers of rows in your output files')
                    print('input file name is: ', f)

                i+=1

            x = data[:, 0]

            Imax_Si_std =    np.std   (Imax_Si[:, :], axis=1)
            Imax_Si_mean =   np.mean  (Imax_Si[:, :], axis=1)
            Imax_Si_median = np.median(Imax_Si[:, :], axis=1)
            Imax_Si_max    = np.amax  (Imax_Si[:, :], axis=1)
            Imax_Si_min    = np.amin  (Imax_Si[:, :], axis=1)


            self.Imax_Si_out_array = np.zeros((numOfRows, 3+3))
            self.Imax_Si_out_array[:, 0] = x
            self.Imax_Si_out_array[:, 1] = Imax_Si_mean
            self.Imax_Si_out_array[:, 2] = Imax_Si_std
            self.Imax_Si_out_array[:, 3] = Imax_Si_median
            self.Imax_Si_out_array[:, 4] = Imax_Si_max
            self.Imax_Si_out_array[:, 5] = Imax_Si_min

            # ---------------------------------
            # save Imax_Si results to the *.dat file:
            out_array = self.Imax_Si_out_array
            case_of_calc = 'Imax_Si'
            headerTxt = 'k\t<Imax_Si>\tstd\tImax_Si_median\tImax_Si_max\tImax_Si_min'
            np.savetxt(os.path.join(outDirPath, 'Imax_Si_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y =               Imax_Si_mean,
                     error =           Imax_Si_std,
                     labelStartName = 'Imax(Si)',
                     y_median=         Imax_Si_median,
                     y_max=            Imax_Si_max,
                     y_min=            Imax_Si_min,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     xlabeltxt = 'etching time (min)', ylabeltxt = 'Ratio (a.u.)',
                     case = case_of_calc)

            Imax_Nb_std =    np.std   (Imax_Nb[:, :], axis=1)
            Imax_Nb_mean =   np.mean  (Imax_Nb[:, :], axis=1)
            Imax_Nb_median = np.median(Imax_Nb[:, :], axis=1)
            Imax_Nb_max    = np.amax  (Imax_Nb[:, :], axis=1)
            Imax_Nb_min    = np.amin  (Imax_Nb[:, :], axis=1)


            self.Imax_Nb_out_array = np.zeros((numOfRows, 3+3))
            self.Imax_Nb_out_array[:, 0] = x
            self.Imax_Nb_out_array[:, 1] = Imax_Nb_mean
            self.Imax_Nb_out_array[:, 2] = Imax_Nb_std
            self.Imax_Nb_out_array[:, 3] = Imax_Nb_median
            self.Imax_Nb_out_array[:, 4] = Imax_Nb_max
            self.Imax_Nb_out_array[:, 5] = Imax_Nb_min

            # ---------------------------------
            # save Imax_Nb results to the *.dat file:
            out_array = self.Imax_Nb_out_array
            case_of_calc = 'Imax_Nb'
            headerTxt = 'k\t<Imax_Nb>\tstd\tImax_Nb_median\tImax_Nb_max\tImax_Nb_min'
            np.savetxt(os.path.join(outDirPath, 'Imax_Nb_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y =               Imax_Nb_mean,
                     error =           Imax_Nb_std,
                     labelStartName = 'Imax(Nb)',
                     y_median=         Imax_Nb_median,
                     y_max=            Imax_Nb_max,
                     y_min=            Imax_Nb_min,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     xlabeltxt = 'etching time (min)', ylabeltxt = 'Ratio (a.u.)',
                     case = case_of_calc)

            # ======================================
            Isub_Si_std =    np.std   (Isub_Si[:, :], axis=1)
            Isub_Si_mean =   np.mean  (Isub_Si[:, :], axis=1)
            Isub_Si_median = np.median(Isub_Si[:, :], axis=1)
            Isub_Si_max    = np.amax  (Isub_Si[:, :], axis=1)
            Isub_Si_min    = np.amin  (Isub_Si[:, :], axis=1)


            self.Isub_Si_out_array = np.zeros((numOfRows, 3+3))
            self.Isub_Si_out_array[:, 0] = x
            self.Isub_Si_out_array[:, 1] = Isub_Si_mean
            self.Isub_Si_out_array[:, 2] = Isub_Si_std
            self.Isub_Si_out_array[:, 3] = Isub_Si_median
            self.Isub_Si_out_array[:, 4] = Isub_Si_max
            self.Isub_Si_out_array[:, 5] = Isub_Si_min

            # ---------------------------------
            # save Isub_Si results to the *.dat file:
            out_array = self.Isub_Si_out_array
            case_of_calc = 'Isub_Si'
            headerTxt = 'k\t<Isub_Si>\tstd\tIsub_Si_median\tIsub_Si_max\tIsub_Si_min'
            np.savetxt(os.path.join(outDirPath, 'Isub_Si_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y =               Isub_Si_mean,
                     error =           Isub_Si_std,
                     labelStartName = 'Isub(Si)',
                     y_median=         Isub_Si_median,
                     y_max=            Isub_Si_max,
                     y_min=            Isub_Si_min,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     xlabeltxt = 'etching time (min)', ylabeltxt = 'Ratio (a.u.)',
                     case = case_of_calc)

            Isub_Nb_std =    np.std   (Isub_Nb[:, :], axis=1)
            Isub_Nb_mean =   np.mean  (Isub_Nb[:, :], axis=1)
            Isub_Nb_median = np.median(Isub_Nb[:, :], axis=1)
            Isub_Nb_max    = np.amax  (Isub_Nb[:, :], axis=1)
            Isub_Nb_min    = np.amin  (Isub_Nb[:, :], axis=1)


            self.Isub_Nb_out_array = np.zeros((numOfRows, 3+3))
            self.Isub_Nb_out_array[:, 0] = x
            self.Isub_Nb_out_array[:, 1] = Isub_Nb_mean
            self.Isub_Nb_out_array[:, 2] = Isub_Nb_std
            self.Isub_Nb_out_array[:, 3] = Isub_Nb_median
            self.Isub_Nb_out_array[:, 4] = Isub_Nb_max
            self.Isub_Nb_out_array[:, 5] = Isub_Nb_min

            # ---------------------------------
            # save Isub_Nb results to the *.dat file:
            out_array = self.Isub_Nb_out_array
            case_of_calc = 'Isub_Nb'
            headerTxt = 'k\t<Isub_Nb>\tstd\tIsub_Nb_median\tIsub_Nb_max\tIsub_Nb_min'
            np.savetxt(os.path.join(outDirPath, 'Isub_Nb_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y =               Isub_Nb_mean,
                     error =           Isub_Nb_std,
                     labelStartName = 'Isub(Nb)',
                     y_median=         Isub_Nb_median,
                     y_max=            Isub_Nb_max,
                     y_min=            Isub_Nb_min,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     xlabeltxt = 'etching time (min)', ylabeltxt = 'Ratio (a.u.)',
                     case = case_of_calc)

            # ======================================
            # ======================================
            Smax_Si_std =    np.std   (Smax_Si[:, :], axis=1)
            Smax_Si_mean =   np.mean  (Smax_Si[:, :], axis=1)
            Smax_Si_median = np.median(Smax_Si[:, :], axis=1)
            Smax_Si_max    = np.amax  (Smax_Si[:, :], axis=1)
            Smax_Si_min    = np.amin  (Smax_Si[:, :], axis=1)


            self.Smax_Si_out_array = np.zeros((numOfRows, 3+3))
            self.Smax_Si_out_array[:, 0] = x
            self.Smax_Si_out_array[:, 1] = Smax_Si_mean
            self.Smax_Si_out_array[:, 2] = Smax_Si_std
            self.Smax_Si_out_array[:, 3] = Smax_Si_median
            self.Smax_Si_out_array[:, 4] = Smax_Si_max
            self.Smax_Si_out_array[:, 5] = Smax_Si_min

            # ---------------------------------
            # save Smax_Si results to the *.dat file:
            out_array = self.Smax_Si_out_array
            case_of_calc = 'Smax_Si'
            headerTxt = 'k\t<Smax_Si>\tstd\tSmax_Si_median\tSmax_Si_max\tSmax_Si_min'
            np.savetxt(os.path.join(outDirPath, 'Smax_Si_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y =               Smax_Si_mean,
                     error =           Smax_Si_std,
                     labelStartName = 'Smax(Si)',
                     y_median=         Smax_Si_median,
                     y_max=            Smax_Si_max,
                     y_min=            Smax_Si_min,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     xlabeltxt = 'etching time (min)', ylabeltxt = 'Ratio (a.u.)',
                     case = case_of_calc)

            Smax_Nb_std =    np.std   (Smax_Nb[:, :], axis=1)
            Smax_Nb_mean =   np.mean  (Smax_Nb[:, :], axis=1)
            Smax_Nb_median = np.median(Smax_Nb[:, :], axis=1)
            Smax_Nb_max    = np.amax  (Smax_Nb[:, :], axis=1)
            Smax_Nb_min    = np.amin  (Smax_Nb[:, :], axis=1)


            self.Smax_Nb_out_array = np.zeros((numOfRows, 3+3))
            self.Smax_Nb_out_array[:, 0] = x
            self.Smax_Nb_out_array[:, 1] = Smax_Nb_mean
            self.Smax_Nb_out_array[:, 2] = Smax_Nb_std
            self.Smax_Nb_out_array[:, 3] = Smax_Nb_median
            self.Smax_Nb_out_array[:, 4] = Smax_Nb_max
            self.Smax_Nb_out_array[:, 5] = Smax_Nb_min

            # ---------------------------------
            # save Smax_Nb results to the *.dat file:
            out_array = self.Smax_Nb_out_array
            case_of_calc = 'Smax_Nb'
            headerTxt = 'k\t<Smax_Nb>\tstd\tSmax_Nb_median\tSmax_Nb_max\tSmax_Nb_min'
            np.savetxt(os.path.join(outDirPath, 'Smax_Nb_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y =               Smax_Nb_mean,
                     error =           Smax_Nb_std,
                     labelStartName = 'Smax(Nb)',
                     y_median=         Smax_Nb_median,
                     y_max=            Smax_Nb_max,
                     y_min=            Smax_Nb_min,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     xlabeltxt = 'etching time (min)', ylabeltxt = 'Ratio (a.u.)',
                     case = case_of_calc)


            # ======================================
            Ssub_Si_std =    np.std   (Ssub_Si[:, :], axis=1)
            Ssub_Si_mean =   np.mean  (Ssub_Si[:, :], axis=1)
            Ssub_Si_median = np.median(Ssub_Si[:, :], axis=1)
            Ssub_Si_max    = np.amax  (Ssub_Si[:, :], axis=1)
            Ssub_Si_min    = np.amin  (Ssub_Si[:, :], axis=1)


            self.Ssub_Si_out_array = np.zeros((numOfRows, 3+3))
            self.Ssub_Si_out_array[:, 0] = x
            self.Ssub_Si_out_array[:, 1] = Ssub_Si_mean
            self.Ssub_Si_out_array[:, 2] = Ssub_Si_std
            self.Ssub_Si_out_array[:, 3] = Ssub_Si_median
            self.Ssub_Si_out_array[:, 4] = Ssub_Si_max
            self.Ssub_Si_out_array[:, 5] = Ssub_Si_min

            # ---------------------------------
            # save Ssub_Si results to the *.dat file:
            out_array = self.Ssub_Si_out_array
            case_of_calc = 'Ssub_Si'
            headerTxt = 'k\t<Ssub_Si>\tstd\tSsub_Si_median\tSsub_Si_max\tSsub_Si_min'
            np.savetxt(os.path.join(outDirPath, 'Ssub_Si_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y =               Ssub_Si_mean,
                     error =           Ssub_Si_std,
                     labelStartName = 'Ssub(Si)',
                     y_median=         Ssub_Si_median,
                     y_max=            Ssub_Si_max,
                     y_min=            Ssub_Si_min,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     xlabeltxt = 'etching time (min)', ylabeltxt = 'Ratio (a.u.)',
                     case = case_of_calc)

            Ssub_Nb_std =    np.std   (Ssub_Nb[:, :], axis=1)
            Ssub_Nb_mean =   np.mean  (Ssub_Nb[:, :], axis=1)
            Ssub_Nb_median = np.median(Ssub_Nb[:, :], axis=1)
            Ssub_Nb_max    = np.amax  (Ssub_Nb[:, :], axis=1)
            Ssub_Nb_min    = np.amin  (Ssub_Nb[:, :], axis=1)


            self.Ssub_Nb_out_array = np.zeros((numOfRows, 3+3))
            self.Ssub_Nb_out_array[:, 0] = x
            self.Ssub_Nb_out_array[:, 1] = Ssub_Nb_mean
            self.Ssub_Nb_out_array[:, 2] = Ssub_Nb_std
            self.Ssub_Nb_out_array[:, 3] = Ssub_Nb_median
            self.Ssub_Nb_out_array[:, 4] = Ssub_Nb_max
            self.Ssub_Nb_out_array[:, 5] = Ssub_Nb_min

            # ---------------------------------
            # save Ssub_Nb results to the *.dat file:
            out_array = self.Ssub_Nb_out_array
            case_of_calc = 'Ssub_Nb'
            headerTxt = 'k\t<Ssub_Nb>\tstd\tSsub_Nb_median\tSsub_Nb_max\tSsub_Nb_min'
            np.savetxt(os.path.join(outDirPath, 'Ssub_Nb_result.dat'), out_array, fmt='%1.6e', delimiter='\t',header=headerTxt)
            plotData(x = x,
                     y =               Ssub_Nb_mean,
                     error =           Ssub_Nb_std,
                     labelStartName = 'Ssub(Nb)',
                     y_median=         Ssub_Nb_median,
                     y_max=            Ssub_Nb_max,
                     y_min=            Ssub_Nb_min,
                     numOfIter = i,
                     out_dir = outDirPath,
                     title_txt = 'Differences between theoretical and experimental data\n'+
                                 'Number of cases involved in the calculation: {}'.format(numOfColumns),
                     xlabeltxt = 'etching time (min)', ylabeltxt = 'Ratio (a.u.)',
                     case = case_of_calc)


            print('-> RD for: Imax(Si), Imax(Nb), Isub(Si), Isub(Nb), Smax(Si), Smax(Nb), Ssub(Si), Ssub(Nb)  was calculated')

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
                     xlabeltxt = 'case number',
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
                     xlabeltxt = 'case number',
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
                     xlabeltxt = 'case number',
                     case = case_of_calc,
                     labelStartName = 'RD(Nb)',
                     y_median= RD_Nb_median,
                     y_max=RD_Nb_max,
                     y_min=RD_Nb_min)


            print('-> <RD>, <RD(Si)>, <RD(Nb)> was calculated')

if __name__ == "__main__":
    print ('-> you run ',  __file__, ' file in a main mode' )
    a = CompareTwoModels()
    a.dataPath = "/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/together_refSpectra"
    a.wantPlotSpectraBeforeAndAfterFiltering = False
    a.wantPlotSpectraExperimentalAndAfterFiltering = False
    a.wantSpectraAndRatios = False
    a.loadSESSAspectra()
    # a.loadSESSAspectra()
    # a.baseOutDirRatios = '/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/together/calc/set_of_ratios/cake/'
    # a.plotMeanOfRatios()
    # a.baseOutDirRatios = '/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/together/calc/set_of_ratios/mix/'
    # a.plotMeanOfRatios()
    a.baseOutDirResiduals = '/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/together_refSpectra/calc/set_of_residuals'
    a.plotMeanOfResiduals()


