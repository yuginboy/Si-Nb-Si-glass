'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-12-27
'''
import os
import datetime
import numpy as np
from scipy.interpolate import interp1d
from libs.backgrounds import shirley_new
import matplotlib.gridspec as gridspec
from matplotlib import pylab
from libs.dir_and_file_operations import get_folder_name

import pickle
import matplotlib.pyplot as plt
# import guiqwt.pyplot as plt

def bg_subtraction(x, y):
    return y - shirley_new(x, y)

class RawFit():
    def __init__(self):
        self.kineticEnergy = []
        self.intensity = []
        self.bindingEnergy = []
        self.excitationEnergy = 1486.7  # eV
        self.maxIntensity = -1

    def calcBindingEnergy(self):
        self.bindingEnergy = self.excitationEnergy - self.kineticEnergy

class Spectra():
    def __init__(self):
        self.raw = RawFit()
        self.fit = RawFit()
        self.energyRegion = [0, self.raw.excitationEnergy]

    def selectEnergyValues(self):
        # select indices of elements inside the region and then select KE and Intencity
        idx = np.where( (self.raw.kineticEnergy >= np.min(self.energyRegion)) *
                        (self.raw.kineticEnergy <= np.max(self.energyRegion))
                        )
        self.fit.kineticEnergy = self.raw.kineticEnergy[idx]
        self.fit.calcBindingEnergy()
        # print('len BE = {}'.format(len(self.fit.bindingEnergy)))

        self.fit.intensity = self.raw.intensity[idx]



class DataStructure():
    def __init__(self):
        self.data = Spectra()
        self.filename = 'name.txt'


class TwoTypesData():
    def __init__(self):
        self.experiment = DataStructure()
        self.theory = DataStructure()
        self.R_factor = -1
        self.valueForNormalizingSpectraInAllRegions_experiment = -1
        self.valueForNormalizingSpectraInAllRegions_theory = -1


    def interpolateTheorData(self):
        # interpolate theory data on the range of KE of experimental data:
        f = interp1d(self.theory.data.raw.kineticEnergy, self.theory.data.raw.intensity)

        self.experiment.data.selectEnergyValues()
        self.theory.data.selectEnergyValues()

        self.theory.data.fit.intensity = f(self.experiment.data.fit.kineticEnergy)
        self.theory.data.fit.kineticEnergy = self.experiment.data.fit.kineticEnergy
        self.theory.data.fit.calcBindingEnergy()

    def subtractBG(self):
        self.interpolateTheorData()
        self.theory.data.fit.intensity = bg_subtraction(self.theory.data.fit.kineticEnergy,
                                                        self.theory.data.fit.intensity)
        self.experiment.data.fit.intensity = bg_subtraction(self.experiment.data.fit.kineticEnergy,
                                                            self.experiment.data.fit.intensity)

    def getMaxIntensityValue(self):
        self.subtractBG()
        self.experiment.data.fit.maxIntensity = np.max(self.experiment.data.fit.intensity)
        self.theory.data.fit.maxIntensity = np.max(self.theory.data.fit.intensity)

    def normolizeIntrinsicIntensity(self):
        # normolize intensity between experiment and theory
        self.subtractBG()
        M = np.max(self.experiment.data.fit.intensity)
        # if len(M)>1:
        #     M = M[0]
        self.experiment.data.fit.intensity = self.experiment.data.fit.intensity / M
        M = np.max(self.theory.data.fit.intensity)
        self.theory.data.fit.intensity = self.theory.data.fit.intensity / M

    def normolizeGlobalIntensity(self):
        # normolize intensity between experiment and theory by using a outside setted value
        self.subtractBG()

        M = self.valueForNormalizingSpectraInAllRegions_experiment
        self.experiment.data.fit.intensity = self.experiment.data.fit.intensity / M
        M = self.valueForNormalizingSpectraInAllRegions_theory
        self.theory.data.fit.intensity = self.theory.data.fit.intensity / M

    def calcRfactor(self):

        # self.normolizeIntrinsicIntensity()
        self.normolizeGlobalIntensity()

        n = self.experiment.data.fit.intensity.__len__()
        A = np.sum( np.abs(self.experiment.data.fit.intensity - self.theory.data.fit.intensity) )
        B = np.sum( np.abs(self.experiment.data.fit.intensity) )
        self.R_factor = (A/B)/n*100
        # > 0.10    Model may be fundamentally incorrect.
        # 0.05 - 0.10   Serious flaws in model or very low quality data.
        # 0.02 - 0.05 Either model has some details wrong, or data is low quality.Nevertheless, consistent with a broadly correct model.
        # < 0.02 Good enough R


class Angled():
    def __init__(self):
        self._0 = TwoTypesData()
        self._60 = TwoTypesData()


class NumericData():
    global_R_factor = -1
    global_min_R_factor = 1000
    global_min_R_factor_path = r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'
    def __init__(self):
        self.showFigs = True
        self.total_R_faktor = -1
        self.k_R_Au_0  = 1
        self.k_R_Au_60 = 1
        self.k_R_Co_0  = 1
        self.k_R_Co_60 = 1
        self.k_R_O_0  = 1
        self.k_R_O_60 = 1
        self.k_R_Mg_0  = 1
        self.k_R_Mg_60 = 1
        self.total_min_R_faktor = 1000
        self.suptitle_txt = '$Fit$ $for$ $model$ $of$ $sample$ $Au/Co/CoO/Au/MgO/MgCO_3/Mg[OH]_2$'
        self.experimentDataPath = r'/home/yugin/PycharmProjects/Si-Nb-Si-glass/exe/raw'
        self.theoryDataPath = r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'
        # Colors for lines on a graph, length of this value and number of time-point simulations should be the same:
        self.colorsForGraph = ['peru', 'dodgerblue', 'brown', 'red', 'darkviolet']

        self.Au4f = Angled()
        self.Co2p = Angled()
        self.O1s = Angled()
        self.Mg1s = Angled()

        self.Au4f._0.experiment.filename = r'raw_Au4f_Mg2s_alpha=0deg.txt'
        self.Au4f._60.experiment.filename = r'raw_Au4f_Mg2s_alpha=60deg.txt'

        self.Co2p._0.experiment.filename = r'raw_Co2p_alpha=0deg.txt'
        self.Co2p._60.experiment.filename = r'raw_Co2p_alpha=60deg.txt'

        self.O1s._0.experiment.filename = r'raw_O1s_alpha=0deg.txt'
        self.O1s._60.experiment.filename = r'raw_O1s_alpha=60deg.txt'

        self.Mg1s._0.experiment.filename = r'raw_Mg1s_alpha=0deg.txt'
        self.Mg1s._60.experiment.filename = r'raw_Mg1s_alpha=60deg.txt'

        self.thicknessVector = [200, 15, 3, 3, 20, 5, 4, 2]
    def set_global_R_factor(self):
        NumericData.global_R_factor = self.total_R_faktor

    def get_global_R_factor(self):
        self.total_R_faktor = NumericData.global_R_factor


    def set_global_min_R_factor(self):
        if self.total_R_faktor <= NumericData.global_min_R_factor:
            NumericData.global_min_R_factor = self.total_R_faktor
            NumericData.global_min_R_factor_path = self.theoryDataPath

    def get_global_min_R_factor(self):
        self.total_min_R_faktor = NumericData.global_min_R_factor


    def loadMaterialsData(self):
        # Getting back the objects:
        pcklFile = os.path.join(self.theoryDataPath, 'objs.pickle')
        with open(pcklFile, 'rb') as f:
            obj = pickle.load(f)
        # print('')
        self.thicknessVector[0] = obj[0].Au_bottom.thickness
        self.thicknessVector[1] = obj[0].Co_metal.thickness
        self.thicknessVector[2] = obj[0].Co_oxide.thickness
        self.thicknessVector[3] = obj[0].Au_interlayer.thickness
        self.thicknessVector[4] = obj[0].MgO.thickness
        self.thicknessVector[5] = obj[0].MgCO3.thickness
        self.thicknessVector[6] = obj[0].Mg_Hydrate.thickness
        self.thicknessVector[7] = obj[0].C_contamination.thickness


    def loadExperimentData(self):
        [x, y] = np.loadtxt(os.path.join(self.experimentDataPath, self.Au4f._0.experiment.filename), unpack=True)
        self.Au4f._0.experiment.data.raw.kineticEnergy = x
        self.Au4f._0.experiment.data.raw.intensity = y
        self.Au4f._0.experiment.data.raw.calcBindingEnergy()

        [x, y] = np.loadtxt(os.path.join(self.experimentDataPath, self.Au4f._60.experiment.filename), unpack=True)
        self.Au4f._60.experiment.data.raw.kineticEnergy = x
        self.Au4f._60.experiment.data.raw.intensity = y
        self.Au4f._60.experiment.data.raw.calcBindingEnergy()

        [x, y] = np.loadtxt(os.path.join(self.experimentDataPath, self.Co2p._0.experiment.filename), unpack=True)
        self.Co2p._0.experiment.data.raw.kineticEnergy = x
        self.Co2p._0.experiment.data.raw.intensity = y
        self.Co2p._0.experiment.data.raw.calcBindingEnergy()

        [x, y] = np.loadtxt(os.path.join(self.experimentDataPath, self.Co2p._60.experiment.filename), unpack=True)
        self.Co2p._60.experiment.data.raw.kineticEnergy = x
        self.Co2p._60.experiment.data.raw.intensity = y
        self.Co2p._60.experiment.data.raw.calcBindingEnergy()

        [x, y] = np.loadtxt(os.path.join(self.experimentDataPath, self.Mg1s._0.experiment.filename), unpack=True)
        self.Mg1s._0.experiment.data.raw.kineticEnergy = x
        self.Mg1s._0.experiment.data.raw.intensity = y
        self.Mg1s._0.experiment.data.raw.calcBindingEnergy()

        [x, y] = np.loadtxt(os.path.join(self.experimentDataPath, self.Mg1s._60.experiment.filename), unpack=True)
        self.Mg1s._60.experiment.data.raw.kineticEnergy = x
        self.Mg1s._60.experiment.data.raw.intensity = y
        self.Mg1s._60.experiment.data.raw.calcBindingEnergy()

        [x, y] = np.loadtxt(os.path.join(self.experimentDataPath, self.O1s._0.experiment.filename), unpack=True)
        self.O1s._0.experiment.data.raw.kineticEnergy = x
        self.O1s._0.experiment.data.raw.intensity = y
        self.O1s._0.experiment.data.raw.calcBindingEnergy()

        [x, y] = np.loadtxt(os.path.join(self.experimentDataPath, self.O1s._60.experiment.filename), unpack=True)
        self.O1s._60.experiment.data.raw.kineticEnergy = x
        self.O1s._60.experiment.data.raw.intensity = y
        self.O1s._60.experiment.data.raw.calcBindingEnergy()

    def loadTheoryData(self):
        [x1, y1, x2, y2] = np.loadtxt(os.path.join(self.theoryDataPath, 'out', 'Au4f.dat'), unpack=True)
        self.Au4f._0.theory.data.raw.kineticEnergy = x1
        self.Au4f._0.theory.data.raw.intensity = y1
        self.Au4f._0.theory.data.raw.calcBindingEnergy()

        self.Au4f._60.theory.data.raw.kineticEnergy = x2
        self.Au4f._60.theory.data.raw.intensity = y2
        self.Au4f._60.theory.data.raw.calcBindingEnergy()

        [x1, y1, x2, y2] = np.loadtxt(os.path.join(self.theoryDataPath, 'out', 'Co2p.dat'), unpack=True)
        self.Co2p._0.theory.data.raw.kineticEnergy = x1
        self.Co2p._0.theory.data.raw.intensity = y1
        self.Co2p._0.theory.data.raw.calcBindingEnergy()

        self.Co2p._60.theory.data.raw.kineticEnergy = x2
        self.Co2p._60.theory.data.raw.intensity = y2
        self.Co2p._60.theory.data.raw.calcBindingEnergy()

        [x1, y1, x2, y2] = np.loadtxt(os.path.join(self.theoryDataPath, 'out', 'Mg1s.dat'), unpack=True)
        self.Mg1s._0.theory.data.raw.kineticEnergy = x1
        self.Mg1s._0.theory.data.raw.intensity = y1
        self.Mg1s._0.theory.data.raw.calcBindingEnergy()

        self.Mg1s._60.theory.data.raw.kineticEnergy = x2
        self.Mg1s._60.theory.data.raw.intensity = y2
        self.Mg1s._60.theory.data.raw.calcBindingEnergy()

        [x1, y1, x2, y2] = np.loadtxt(os.path.join(self.theoryDataPath, 'out', 'O1s.dat'), unpack=True)
        self.O1s._0.theory.data.raw.kineticEnergy = x1
        self.O1s._0.theory.data.raw.intensity = y1
        self.O1s._0.theory.data.raw.calcBindingEnergy()

        self.O1s._60.theory.data.raw.kineticEnergy = x2
        self.O1s._60.theory.data.raw.intensity = y2
        self.O1s._60.theory.data.raw.calcBindingEnergy()

    def updateRfactor(self):
        self.Au4f._0.calcRfactor()
        self.Au4f._60.calcRfactor()

        self.Co2p._0.calcRfactor()
        self.Co2p._60.calcRfactor()

        self.O1s._0.calcRfactor()
        self.O1s._60.calcRfactor()

        self.Mg1s._0.calcRfactor()
        self.Mg1s._60.calcRfactor()

        self.total_R_faktor = (
                              self.k_R_Au_0  * self.Au4f._0.R_factor + \
                              self.k_R_Au_60 * self.Au4f._60.R_factor + \
                              self.k_R_Co_0  * self.Co2p._0.R_factor +  \
                              self.k_R_Co_60 * self.Co2p._60.R_factor + \
                              self.k_R_O_0  *  self.O1s._0.R_factor +   \
                              self.k_R_O_60 *  self.O1s._60.R_factor +  \
                              self.k_R_Mg_0 *  self.Mg1s._0.R_factor +  \
                              self.k_R_Mg_60 * self.Mg1s._60.R_factor
                              )/(
                                 self.k_R_Au_0 + self.k_R_Au_60 + \
                                 self.k_R_Co_0 + self.k_R_Co_60 + \
                                 self.k_R_O_0 + self.k_R_O_60 + \
                                 self.k_R_Mg_0 + self.k_R_Mg_60
                                 )

        # self.total_R_faktor = (
        #                       self.Au4f._0.R_factor + \
        #                       self.Au4f._60.R_factor + \
        #                       self.Co2p._0.R_factor +  \
        #                       self.Co2p._60.R_factor + \
        #                       self.O1s._0.R_factor +   \
        #                       self.O1s._60.R_factor
        #                       )/6


    def setupAxes(self):
        if self.showFigs:
            # create figure with axes:

            pylab.ion()  # Force interactive
            plt.close('all')
            ### for 'Qt4Agg' backend maximize figure
            # plt.switch_backend('QT5Agg')

            self.fig = plt.figure()
            # gs1 = gridspec.GridSpec(1, 2)
            # fig.show()
            # fig.set_tight_layout(True)
            self.figManager = plt.get_current_fig_manager()
            DPI = self.fig.get_dpi()
            self.fig.set_size_inches(800.0 / DPI, 600.0 / DPI)

            gs = gridspec.GridSpec(2, 2)

            self.fig.clf()

            self.Co2p.axes = self.fig.add_subplot(gs[0, 0])
            self.Co2p.axes.invert_xaxis()
            self.Co2p.axes.set_title('Co2p')
            self.Co2p.axes.grid(True)

            self.Au4f.axes = self.fig.add_subplot(gs[0, 1])
            self.Au4f.axes.invert_xaxis()
            self.Au4f.axes.set_title('Au4f')
            self.Au4f.axes.grid(True)

            self.O1s.axes = self.fig.add_subplot(gs[1, 0])
            self.O1s.axes.invert_xaxis()
            self.O1s.axes.set_title('O1s')
            self.O1s.axes.grid(True)

            self.Mg1s.axes = self.fig.add_subplot(gs[1, 1])
            self.Mg1s.axes.invert_xaxis()
            self.Mg1s.axes.set_title('Mg1s')
            self.Mg1s.axes.grid(True)

            self.Co2p.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.Co2p.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.Au4f.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.Au4f.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.O1s.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.O1s.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.Mg1s.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.Mg1s.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')

            # Change the axes border width
            for axis in ['top', 'bottom', 'left', 'right']:
                self.Co2p.axes.spines[axis].set_linewidth(2)
                self.Au4f.axes.spines[axis].set_linewidth(2)
                self.O1s.axes.spines[axis].set_linewidth(2)
                self.Mg1s.axes.spines[axis].set_linewidth(2)

            # plt.subplots_adjust(top=0.85)
            # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
            self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

            # put window to the second monitor
            # figManager.window.setGeometry(1923, 23, 640, 529)
            self.figManager.window.setGeometry(1920, 20, 1920, 1180)

            plt.show()

            self.fig.suptitle(self.suptitle_txt, fontsize=22, fontweight='normal')

            # put window to the second monitor
            # figManager.window.setGeometry(1923, 23, 640, 529)
            # self.figManager.window.setGeometry(780, 20, 800, 600)
            self.figManager.window.setWindowTitle('CoO fitting')
            self.figManager.window.showMinimized()


            # save to the PNG file:
            # out_file_name = '%s_' % (case) + "%05d.png" % (numOfIter)
            # fig.savefig(os.path.join(out_dir, out_file_name))
    def updatePlot(self, saveFigs=True, doLoadMaterialsData=True):


        if doLoadMaterialsData:
            self.loadMaterialsData()

        self.updateRfactor()

        if self.showFigs:

            self.suptitle_txt = '$Fit$ $for$ $model$ $of$ $sample$'+ \
                '$Au[{0:1.3f}\AA]/Co[{1:1.3f}\AA]/CoO[{2:1.3f}\AA]/Au[{3:1.3f}\AA]/MgO[{4:1.3f}\AA]/MgCO_3[{5:1.3f}\AA]/Mg(OH)_2[{6:1.3f}\AA]/C[{7:1.3f}\AA]$'.format(
                self.thicknessVector[0], self.thicknessVector[1], self.thicknessVector[2], self.thicknessVector[3],
                self.thicknessVector[4], self.thicknessVector[5], self.thicknessVector[6], self.thicknessVector[7],
            )

            self.fig.clf()
            gs = gridspec.GridSpec(2, 2)

            self.Co2p.axes = self.fig.add_subplot(gs[0, 0])
            self.Co2p.axes.invert_xaxis()
            if abs(self.k_R_Co_0 + self.k_R_Co_60) > 0:
                Rtot = (self.k_R_Co_0  * self.Co2p._0.R_factor + self.k_R_Co_60 * self.Co2p._60.R_factor)/(self.k_R_Co_0 + self.k_R_Co_60)
            else:
                Rtot = (self.k_R_Co_0  * self.Co2p._0.R_factor + self.k_R_Co_60 * self.Co2p._60.R_factor)/2
            self.Co2p.axes.set_title('Co2p, $R_{{0}}=${0:1.4}, $R_{{60}}=${1:1.4}, $R_{{tot}}=${2:1.4}'.format(self.Co2p._0.R_factor, self.Co2p._60.R_factor, Rtot))
            self.Co2p.axes.grid(True)

            self.Au4f.axes = self.fig.add_subplot(gs[0, 1])
            self.Au4f.axes.invert_xaxis()
            if abs(self.k_R_Au_0 + self.k_R_Au_60) > 0:
                Rtot = (self.k_R_Au_0  * self.Au4f._0.R_factor + self.k_R_Au_60 * self.Au4f._60.R_factor)/(self.k_R_Au_0 + self.k_R_Au_60)
            else:
                Rtot = (self.k_R_Au_0  * self.Au4f._0.R_factor + self.k_R_Au_60 * self.Au4f._60.R_factor)/2
            self.Au4f.axes.set_title('Au4f, $R_{{0}}=${0:1.4}, $R_{{60}}=${1:1.4}, $R_{{tot}}=${2:1.4}'.format(self.Au4f._0.R_factor, self.Au4f._60.R_factor, Rtot))
            self.Au4f.axes.grid(True)

            self.O1s.axes = self.fig.add_subplot(gs[1, 0])
            self.O1s.axes.invert_xaxis()
            if abs(self.k_R_O_0 + self.k_R_O_60) > 0:
                Rtot = (self.k_R_O_0  * self.O1s._0.R_factor + self.k_R_O_60 * self.O1s._60.R_factor)/(self.k_R_O_0 + self.k_R_O_60)
            else:
                Rtot = (self.k_R_O_0  * self.O1s._0.R_factor + self.k_R_O_60 * self.O1s._60.R_factor)/2
            self.O1s.axes.set_title('O1s, $R_{{0}}=${0:1.4}, $R_{{60}}=${1:1.4}, $R_{{tot}}=${2:1.4}'.format(self.O1s._0.R_factor, self.O1s._60.R_factor, Rtot))
            self.O1s.axes.grid(True)

            self.Mg1s.axes = self.fig.add_subplot(gs[1, 1])
            self.Mg1s.axes.invert_xaxis()
            if abs(self.k_R_Mg_0 + self.k_R_Mg_60) > 0:
                Rtot = (self.k_R_Mg_0  * self.Mg1s._0.R_factor + self.k_R_Mg_60 * self.Mg1s._60.R_factor)/(self.k_R_Mg_0 + self.k_R_Mg_60)
            else:
                Rtot = (self.k_R_Mg_0  * self.Mg1s._0.R_factor + self.k_R_Mg_60 * self.Mg1s._60.R_factor)/2
            self.Mg1s.axes.set_title('Mg1s, $R_{{0}}=${0:1.4}, $R_{{60}}=${1:1.4}, $R_{{tot}}=${2:1.4}'.format(self.Mg1s._0.R_factor, self.Mg1s._60.R_factor, Rtot))
            self.Mg1s.axes.grid(True)

            self.Co2p.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.Co2p.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.Au4f.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.Au4f.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.O1s.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.O1s.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.Mg1s.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.Mg1s.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')

            # plot experimental data:
            self.Co2p.axes.plot(self.Co2p._0.experiment.data.fit.bindingEnergy,
                                self.Co2p._0.experiment.data.fit.intensity, '--', label=('Co2p $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            self.Co2p.axes.plot(self.Co2p._60.experiment.data.fit.bindingEnergy,
                                self.Co2p._60.experiment.data.fit.intensity, '--', label=('Co2p $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)

            self.Au4f.axes.plot(self.Au4f._0.experiment.data.fit.bindingEnergy,
                                self.Au4f._0.experiment.data.fit.intensity, '--', label=('Au4f $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            self.Au4f.axes.plot(self.Au4f._60.experiment.data.fit.bindingEnergy,
                                self.Au4f._60.experiment.data.fit.intensity, '--', label=('Au4f $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)

            self.O1s.axes.plot(self.O1s._0.experiment.data.fit.bindingEnergy,
                                self.O1s._0.experiment.data.fit.intensity, '--', label=('O1s $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            self.O1s.axes.plot(self.O1s._60.experiment.data.fit.bindingEnergy,
                                self.O1s._60.experiment.data.fit.intensity, '--', label=('O1s $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)

            self.Mg1s.axes.plot(self.Mg1s._0.experiment.data.fit.bindingEnergy,
                                self.Mg1s._0.experiment.data.fit.intensity, '--', label=('Mg1s $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            self.Mg1s.axes.plot(self.Mg1s._60.experiment.data.fit.bindingEnergy,
                                self.Mg1s._60.experiment.data.fit.intensity, '--', label=('Mg1s $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)



            # plot theoretical data
            self.Co2p.axes.plot(self.Co2p._0.theory.data.fit.bindingEnergy,
                                self.Co2p._0.theory.data.fit.intensity, '-', label=('Co2p $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            self.Co2p.axes.plot(self.Co2p._60.theory.data.fit.bindingEnergy,
                                self.Co2p._60.theory.data.fit.intensity, '-', label=('Co2p $\\alpha=60^O$' + ' theory'),
                             color=self.colorsForGraph[3], linewidth=5, alpha=0.5)

            self.Au4f.axes.plot(self.Au4f._0.theory.data.fit.bindingEnergy,
                                self.Au4f._0.theory.data.fit.intensity, '-', label=('Au4f $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            self.Au4f.axes.plot(self.Au4f._60.theory.data.fit.bindingEnergy,
                                self.Au4f._60.theory.data.fit.intensity, '-', label=('Au4f $\\alpha=60^O$' + ' theory'),
                             color=self.colorsForGraph[3], linewidth=5, alpha=0.5)

            self.O1s.axes.plot(self.O1s._0.theory.data.fit.bindingEnergy,
                                self.O1s._0.theory.data.fit.intensity, '-', label=('O1s $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            self.O1s.axes.plot(self.O1s._60.theory.data.fit.bindingEnergy,
                                self.O1s._60.theory.data.fit.intensity, '-', label=('O1s $\\alpha=60^O$' + ' theory'),
                             color=self.colorsForGraph[3], linewidth=5, alpha=0.5)

            self.Mg1s.axes.plot(self.Mg1s._0.theory.data.fit.bindingEnergy,
                                self.Mg1s._0.theory.data.fit.intensity, '-', label=('Mg1s $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            self.Mg1s.axes.plot(self.Mg1s._60.theory.data.fit.bindingEnergy,
                                self.Mg1s._60.theory.data.fit.intensity, '-', label=('Mg1s $\\alpha=60^O$' + ' theory'),
                             color=self.colorsForGraph[3], linewidth=5, alpha=0.5)


            self.Co2p.axes.legend(shadow=True, fancybox=True, loc='upper left')
            # Change the axes border width
            for axis in ['top', 'bottom', 'left', 'right']:
                self.Co2p.axes.spines[axis].set_linewidth(2)
                self.Au4f.axes.spines[axis].set_linewidth(2)
                self.O1s.axes.spines[axis].set_linewidth(2)
                self.Mg1s.axes.spines[axis].set_linewidth(2)

            # plt.subplots_adjust(top=0.85)
            # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
            # self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

            # put window to the second monitor
            # figManager.window.setGeometry(1923, 23, 640, 529)
            self.figManager.window.setGeometry(1920, 20, 1920, 1180)

            # plt.show()
            plt.draw()
            self.fig.suptitle(self.suptitle_txt, fontsize=22, fontweight='normal')

            # put window to the second monitor
            # figManager.window.setGeometry(1923, 23, 640, 529)
            # self.figManager.window.setGeometry(780, 20, 800, 600)



            self.figManager.window.setWindowTitle('CoO fitting')
            self.figManager.window.showMinimized()

        if saveFigs and self.showFigs:
            # save to the PNG file:
            timestamp = datetime.datetime.now().strftime("_[%Y-%m-%d_%H_%M_%S]_")
            out_file_name = get_folder_name(self.theoryDataPath) + timestamp + \
                            '_R={0:1.4}.png'.format(self.total_R_faktor)
            self.fig.savefig(os.path.join(self.theoryDataPath, out_file_name))

if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    a = NumericData()
    a.theoryDataPath = r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'
    a.loadExperimentData()
    a.loadTheoryData()
    a.Au4f._0.experiment.data.energyRegion = [1395, 1405]
    a.Au4f._0.theory.data.energyRegion = [1395, 1405]
    a.Au4f._60.experiment.data.energyRegion = [1395, 1405]
    a.Au4f._60.theory.data.energyRegion = [1395, 1405]

    a.Co2p._0.experiment.data.energyRegion = [700, 710]
    a.Co2p._0.theory.data.energyRegion = [700, 710]
    a.Co2p._60.experiment.data.energyRegion = [700, 710]
    a.Co2p._60.theory.data.energyRegion = [700, 710]

    a.O1s._0.experiment.data.energyRegion = [950, 960]
    a.O1s._0.theory.data.energyRegion = [950, 960]
    a.O1s._60.experiment.data.energyRegion = [950, 960]
    a.O1s._60.theory.data.energyRegion = [950, 960]

    a.Mg1s._0.experiment.data.energyRegion = [179, 185]
    a.Mg1s._0.theory.data.energyRegion = [179, 185]
    a.Mg1s._60.experiment.data.energyRegion = [179, 185]
    a.Mg1s._60.theory.data.energyRegion = [179, 185]


    # a.loadMaterialsData()
    # a.Au4f._0.experiment.data.selectEnergyValues()
    # a.Au4f._0.interpolateTheorData()
    # a.Au4f._0.calcRfactor()
    # a.Au4f._60.calcRfactor()
    #
    # a.Co2p._0.calcRfactor()
    # a.Co2p._60.calcRfactor()
    #
    # a.O1s._0.calcRfactor()
    # a.O1s._60.calcRfactor()
    #
    # a.Mg1s._0.calcRfactor()
    # a.Mg1s._60.calcRfactor()


    a.setupAxes()

    # start to Global Normolize procedure:
    a.Au4f._0.getMaxIntensityValue()
    a.Au4f._60.getMaxIntensityValue()
    print('a.Au4f._0.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._0.experiment.data.fit.maxIntensity))
    print('a.Au4f._0.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._0.theory.data.fit.maxIntensity))
    print('a.Au4f._60.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._60.experiment.data.fit.maxIntensity))
    print('a.Au4f._60.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._60.theory.data.fit.maxIntensity))

    a.Co2p._0.getMaxIntensityValue()
    a.Co2p._60.getMaxIntensityValue()
    print('a.Co2p._0.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._0.experiment.data.fit.maxIntensity))
    print('a.Co2p._0.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._0.theory.data.fit.maxIntensity))
    print('a.Co2p._60.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._60.experiment.data.fit.maxIntensity))
    print('a.Co2p._60.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._60.theory.data.fit.maxIntensity))

    a.O1s._0.getMaxIntensityValue()
    a.O1s._60.getMaxIntensityValue()
    print('a.O1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._0.experiment.data.fit.maxIntensity))
    print('a.O1s._0.theory.data.fit.maxIntensity = {0}'.format(a.O1s._0.theory.data.fit.maxIntensity))
    print('a.O1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._60.experiment.data.fit.maxIntensity))
    print('a.O1s._60.theory.data.fit.maxIntensity = {0}'.format(a.O1s._60.theory.data.fit.maxIntensity))

    a.Mg1s._0.getMaxIntensityValue()
    a.Mg1s._60.getMaxIntensityValue()
    print('a.Mg1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.experiment.data.fit.maxIntensity))
    print('a.Mg1s._0.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.theory.data.fit.maxIntensity))
    print('a.Mg1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.experiment.data.fit.maxIntensity))
    print('a.Mg1s._60.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.theory.data.fit.maxIntensity))

    maxIntensity_0_theory = np.max([a.Au4f._0.theory.data.fit.maxIntensity, a.Co2p._0.theory.data.fit.maxIntensity,
                          a.O1s._0.theory.data.fit.maxIntensity,  a.Mg1s._0.theory.data.fit.maxIntensity])
    maxIntensity_60_theory = np.max([a.Au4f._60.theory.data.fit.maxIntensity, a.Co2p._60.theory.data.fit.maxIntensity,
                          a.O1s._60.theory.data.fit.maxIntensity,  a.Mg1s._60.theory.data.fit.maxIntensity])

    maxIntensity_0_experiment = np.max([a.Au4f._0.experiment.data.fit.maxIntensity, a.Co2p._0.experiment.data.fit.maxIntensity,
                          a.O1s._0.experiment.data.fit.maxIntensity,  a.Mg1s._0.experiment.data.fit.maxIntensity])
    maxIntensity_60_experiment = np.max([a.Au4f._60.experiment.data.fit.maxIntensity, a.Co2p._60.experiment.data.fit.maxIntensity,
                          a.O1s._60.experiment.data.fit.maxIntensity,  a.Mg1s._60.experiment.data.fit.maxIntensity])

    a.Au4f._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
    a.Au4f._0.valueForNormalizingSpectraInAllRegions_theory     = maxIntensity_0_theory

    a.Co2p._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
    a.Co2p._0.valueForNormalizingSpectraInAllRegions_theory     = maxIntensity_0_theory

    a.O1s._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
    a.O1s._0.valueForNormalizingSpectraInAllRegions_theory     = maxIntensity_0_theory

    a.Mg1s._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
    a.Mg1s._0.valueForNormalizingSpectraInAllRegions_theory     = maxIntensity_0_theory



    a.Au4f._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
    a.Au4f._60.valueForNormalizingSpectraInAllRegions_theory     = maxIntensity_60_theory

    a.Co2p._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
    a.Co2p._60.valueForNormalizingSpectraInAllRegions_theory     = maxIntensity_60_theory

    a.O1s._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
    a.O1s._60.valueForNormalizingSpectraInAllRegions_theory     = maxIntensity_60_theory

    a.Mg1s._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
    a.Mg1s._60.valueForNormalizingSpectraInAllRegions_theory     = maxIntensity_60_theory



    a.updatePlot()
    print('R-factor = {}'.format(a.Au4f._60.R_factor))