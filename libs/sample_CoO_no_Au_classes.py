'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-01-12
'''
from libs.createSESSAprojectFile_CoO import SAMPLE
from libs.dataProperties import NumericData
import os
from shutil import copyfile
from libs.dir_and_file_operations import createFolder
import pickle
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
import datetime
import numpy as np
from libs.dir_and_file_operations import get_folder_name
from libs.classFuncMinimize import BaseClassForCalcAndMinimize, runningScriptDir

# Create structure of layered material:
class SAMPLE_CoO_no_Au(SAMPLE):
    def __init__(self):
        super(SAMPLE_CoO_no_Au, self).__init__()

    def initializeStructure(self):
        # init the structure with the default parameters for layers:

        # add Au:
        self.addLayerToStructure(self.Au_bottom)
        # add Co-metal:
        self.addLayerToStructure(self.Co_metal)

        # # add CoO_Au_mix:
        # self.addLayer(self.CoO_Au_mix)

        # add CoO:
        self.addLayerToStructure(self.Co_oxide)
        # add Au 3A:
        self.addLayerToStructure(self.Au_interlayer)

        # add MgO:
        self.addLayerToStructure(self.MgO)
        # add MgCO3:
        self.addLayerToStructure(self.MgCO3)
        # add Mg[OH]2:
        self.addLayerToStructure(self.Mg_Hydrate)
        # add Au 3A:
        self.addLayerToStructure(self.Au_top)
        # add C contamination on a surface:
        self.addLayerToStructure(self.C_contamination)


# Create Numerical data class for new sample:
class NumericData_CoO_no_Au(NumericData):
    def __init__(self):
        super(NumericData_CoO_no_Au, self).__init__()
        # self.colorsForGraph = ['darkviolet', 'dodgerblue', 'brown', 'red', 'darkviolet']
    def updatePlot(self, saveFigs=True, doLoadMaterialsData=True):


        if doLoadMaterialsData:
            self.loadMaterialsData()

        self.updateRfactor()

        if self.showFigs:

            self.fig.clf()
            gs = gridspec.GridSpec(2, 2)

            self.Co2p.axes = self.fig.add_subplot(gs[0, 0])
            self.Co2p.axes.invert_xaxis()
            if abs(self.k_R_Co_0 + self.k_R_Co_60) > 0:
                Rtot = (self.k_R_Co_0  * self.Co2p._0.R_factor + self.k_R_Co_60 * self.Co2p._60.R_factor)/(self.k_R_Co_0 + self.k_R_Co_60)
            else:
                Rtot = (self.k_R_Co_0  * self.Co2p._0.R_factor + self.k_R_Co_60 * self.Co2p._60.R_factor)/2
            self.Co2p.axes.set_title('Co2p, $R_{{0}}=${0:1.4}, $R_{{tot}}=${2:1.4}'.format(self.Co2p._0.R_factor, self.Co2p._60.R_factor, Rtot))
            self.Co2p.axes.grid(True)

            self.Au4f.axes = self.fig.add_subplot(gs[0, 1])
            self.Au4f.axes.invert_xaxis()
            if abs(self.k_R_Au_0 + self.k_R_Au_60) > 0:
                Rtot = (self.k_R_Au_0  * self.Au4f._0.R_factor + self.k_R_Au_60 * self.Au4f._60.R_factor)/(self.k_R_Au_0 + self.k_R_Au_60)
            else:
                Rtot = (self.k_R_Au_0  * self.Au4f._0.R_factor + self.k_R_Au_60 * self.Au4f._60.R_factor)/2
            self.Au4f.axes.set_title('Au4f, $R_{{0}}=${0:1.4}, $R_{{tot}}=${2:1.4}'.format(self.Au4f._0.R_factor, self.Au4f._60.R_factor, Rtot))
            self.Au4f.axes.grid(True)

            self.O1s.axes = self.fig.add_subplot(gs[1, 0])
            self.O1s.axes.invert_xaxis()
            if abs(self.k_R_O_0 + self.k_R_O_60) > 0:
                Rtot = (self.k_R_O_0  * self.O1s._0.R_factor + self.k_R_O_60 * self.O1s._60.R_factor)/(self.k_R_O_0 + self.k_R_O_60)
            else:
                Rtot = (self.k_R_O_0  * self.O1s._0.R_factor + self.k_R_O_60 * self.O1s._60.R_factor)/2
            self.O1s.axes.set_title('O1s, $R_{{0}}=${0:1.4}, $R_{{tot}}=${2:1.4}'.format(self.O1s._0.R_factor, self.O1s._60.R_factor, Rtot))
            self.O1s.axes.grid(True)

            self.Mg1s.axes = self.fig.add_subplot(gs[1, 1])
            self.Mg1s.axes.invert_xaxis()
            if abs(self.k_R_Mg_0 + self.k_R_Mg_60) > 0:
                Rtot = (self.k_R_Mg_0  * self.Mg1s._0.R_factor + self.k_R_Mg_60 * self.Mg1s._60.R_factor)/(self.k_R_Mg_0 + self.k_R_Mg_60)
            else:
                Rtot = (self.k_R_Mg_0  * self.Mg1s._0.R_factor + self.k_R_Mg_60 * self.Mg1s._60.R_factor)/2
            self.Mg1s.axes.set_title('Mg1s, $R_{{0}}=${0:1.4}, $R_{{tot}}=${2:1.4}'.format(self.Mg1s._0.R_factor, self.Mg1s._60.R_factor, Rtot))
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
            # self.Co2p.axes.plot(self.Co2p._60.experiment.data.fit.bindingEnergy,
            #                     self.Co2p._60.experiment.data.fit.intensity, '--', label=('Co2p $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)

            self.Au4f.axes.plot(self.Au4f._0.experiment.data.fit.bindingEnergy,
                                self.Au4f._0.experiment.data.fit.intensity, '--', label=('Au4f $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            # self.Au4f.axes.plot(self.Au4f._60.experiment.data.fit.bindingEnergy,
            #                     self.Au4f._60.experiment.data.fit.intensity, '--', label=('Au4f $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)

            self.O1s.axes.plot(self.O1s._0.experiment.data.fit.bindingEnergy,
                                self.O1s._0.experiment.data.fit.intensity, '--', label=('O1s $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            # self.O1s.axes.plot(self.O1s._60.experiment.data.fit.bindingEnergy,
            #                     self.O1s._60.experiment.data.fit.intensity, '--', label=('O1s $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)

            self.Mg1s.axes.plot(self.Mg1s._0.experiment.data.fit.bindingEnergy,
                                self.Mg1s._0.experiment.data.fit.intensity, '--', label=('Mg1s $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            # self.Mg1s.axes.plot(self.Mg1s._60.experiment.data.fit.bindingEnergy,
            #                     self.Mg1s._60.experiment.data.fit.intensity, '--', label=('Mg1s $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)



            # plot theoretical data
            self.Co2p.axes.plot(self.Co2p._0.theory.data.fit.bindingEnergy,
                                self.Co2p._0.theory.data.fit.intensity, '-', label=('Co2p $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            # self.Co2p.axes.plot(self.Co2p._60.theory.data.fit.bindingEnergy,
            #                     self.Co2p._60.theory.data.fit.intensity, '-', label=('Co2p $\\alpha=60^O$' + ' theory'),
            #                  color=self.colorsForGraph[3], linewidth=5, alpha=0.5)

            self.Au4f.axes.plot(self.Au4f._0.theory.data.fit.bindingEnergy,
                                self.Au4f._0.theory.data.fit.intensity, '-', label=('Au4f $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            # self.Au4f.axes.plot(self.Au4f._60.theory.data.fit.bindingEnergy,
            #                     self.Au4f._60.theory.data.fit.intensity, '-', label=('Au4f $\\alpha=60^O$' + ' theory'),
            #                  color=self.colorsForGraph[3], linewidth=5, alpha=0.5)

            self.O1s.axes.plot(self.O1s._0.theory.data.fit.bindingEnergy,
                                self.O1s._0.theory.data.fit.intensity, '-', label=('O1s $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            # self.O1s.axes.plot(self.O1s._60.theory.data.fit.bindingEnergy,
            #                     self.O1s._60.theory.data.fit.intensity, '-', label=('O1s $\\alpha=60^O$' + ' theory'),
            #                  color=self.colorsForGraph[3], linewidth=5, alpha=0.5)

            self.Mg1s.axes.plot(self.Mg1s._0.theory.data.fit.bindingEnergy,
                                self.Mg1s._0.theory.data.fit.intensity, '-', label=('Mg1s $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            # self.Mg1s.axes.plot(self.Mg1s._60.theory.data.fit.bindingEnergy,
            #                     self.Mg1s._60.theory.data.fit.intensity, '-', label=('Mg1s $\\alpha=60^O$' + ' theory'),
            #                  color=self.colorsForGraph[3], linewidth=5, alpha=0.5)


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

class Class_CoO_no_Au(BaseClassForCalcAndMinimize):
    def __init__(self):
        self.sample = SAMPLE_CoO_no_Au()
        self.a = NumericData_CoO_no_Au()
        self.a.Au4f._0.experiment.filename = r'raw_Au4f_Mg2s_alpha=0deg_CoO_no_Au.txt'
        self.a.Au4f._60.experiment.filename = r'raw_Au4f_Mg2s_alpha=60deg.txt'

        self.a.Co2p._0.experiment.filename = r'raw_Co2p_alpha=0deg_CoO_no_Au.txt'
        self.a.Co2p._60.experiment.filename = r'raw_Co2p_alpha=60deg.txt'

        self.a.O1s._0.experiment.filename = r'raw_O1s_alpha=0deg_CoO_no_Au.txt'
        self.a.O1s._60.experiment.filename = r'raw_O1s_alpha=60deg.txt'

        self.a.Mg1s._0.experiment.filename = r'raw_Mg1s_alpha=0deg_CoO_no_Au.txt'
        self.a.Mg1s._60.experiment.filename = r'raw_Mg1s_alpha=60deg.txt'

        self.projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out'
        self.case_R_factor = 'all'
        self.workFolder = self.projPath
        self.returncode = -1

        self.a.k_R_Co_0 =  1
        self.a.k_R_Co_60 = 0
        self.a.k_R_Au_0 =  1
        self.a.k_R_Au_60 = 0
        self.a.k_R_O_0 =   1
        self.a.k_R_O_60 =  0
        self.a.k_R_Mg_0 =  1
        self.a.k_R_Mg_60 = 0

        self.x = np.array([200.000, 15.000, 3.0, 0.001, 40.000, 5.000, 5.000, 3.0, 5.000])

    def generateWorkPlace(self, dirPath=r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'):
        # created folder and copy the files:
        createFolder(os.path.join(dirPath, 'out'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'run.exe'),
                 os.path.join(dirPath, 'run.exe'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'exec.bat'),
                 os.path.join(dirPath, 'exec.bat'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'additional_commands_Co_no_Au.ses'),
                 os.path.join(dirPath, 'additional_commands.ses'))


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    testCase = 3
    if testCase == 1:
        a = NumericData_CoO_no_Au()
        a.theoryDataPath = r'/home/yugin/VirtualboxShare/Co-CoO/out/00007'
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
                                        a.O1s._0.theory.data.fit.maxIntensity, a.Mg1s._0.theory.data.fit.maxIntensity])
        maxIntensity_60_theory = np.max(
            [a.Au4f._60.theory.data.fit.maxIntensity, a.Co2p._60.theory.data.fit.maxIntensity,
             a.O1s._60.theory.data.fit.maxIntensity, a.Mg1s._60.theory.data.fit.maxIntensity])

        maxIntensity_0_experiment = np.max(
            [a.Au4f._0.experiment.data.fit.maxIntensity, a.Co2p._0.experiment.data.fit.maxIntensity,
             a.O1s._0.experiment.data.fit.maxIntensity, a.Mg1s._0.experiment.data.fit.maxIntensity])
        maxIntensity_60_experiment = np.max(
            [a.Au4f._60.experiment.data.fit.maxIntensity, a.Co2p._60.experiment.data.fit.maxIntensity,
             a.O1s._60.experiment.data.fit.maxIntensity, a.Mg1s._60.experiment.data.fit.maxIntensity])

        a.Au4f._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
        a.Au4f._0.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_0_theory

        a.Co2p._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
        a.Co2p._0.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_0_theory

        a.O1s._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
        a.O1s._0.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_0_theory

        a.Mg1s._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
        a.Mg1s._0.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_0_theory

        a.Au4f._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
        a.Au4f._60.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_60_theory

        a.Co2p._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
        a.Co2p._60.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_60_theory

        a.O1s._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
        a.O1s._60.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_60_theory

        a.Mg1s._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
        a.Mg1s._60.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_60_theory

        a.updatePlot()
        print('R-factor = {}'.format(a.Au4f._60.R_factor))

    elif testCase == 2:
        a = SAMPLE_CoO_no_Au()
        a.writeSesFile()
        a.getLayersStructureInfo()

    elif testCase == 3:
        b1 = Class_CoO_no_Au()
        b1.x = [200.000, 15.000, 3.0, 0.001, 40.000, 5.000, 5.000, 3.0, 5.000]
        z = b1.compareTheoryAndExperiment()
        # b2 = Class_CoO_no_Au()
        # b2.x = [200.000, 15.000, 3.0, 0.001, 30.000, 15.000,7.000, 3.0, 5.000]
        # z = b2.compareTheoryAndExperiment()
