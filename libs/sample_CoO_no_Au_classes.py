'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-01-12
Set of classes for sample Au/Co/MgO/Au which named: CoO_no_Au or S1614
'''
from libs.createSESSAprojectFile_CoO import SAMPLE
from libs.dataProperties import NumericData
import os
from shutil import copyfile
from libs.dir_and_file_operations import createFolder, create_out_data_folder
import pickle
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
import datetime
import numpy as np
from libs.dir_and_file_operations import get_folder_name
from libs.classFuncMinimize import BaseClassForCalcAndMinimize, runningScriptDir
from libs.execCommandInSESSA import execProjectSessionWithTimeoutControl



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

        # add CoO_Au_mix:
        self.addLayerToStructure(self.CoO_Au_mix)

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

        # add mix of MgCO3 and Mg[OH]2:
        self.addLayerToStructure(self.MgCO3_MgOH_mix)

        # add Au 3A:
        self.addLayerToStructure(self.Au_top)

        # add C contamination on a surface:
        self.addLayerToStructure(self.C_contamination)


# Create Numerical data class for new sample:
class NumericData_CoO_no_Au(NumericData):
    def __init__(self):
        super(NumericData_CoO_no_Au, self).__init__()
        self.suptitle_fontsize = 18
        # self.colorsForGraph = ['darkviolet', 'dodgerblue', 'brown', 'red', 'darkviolet']
        self.experimentDataPath = r'/home/yugin/PycharmProjects/Si-Nb-Si-glass/exe/model_no_Au/raw'

        self.Au4f._0.experiment.filename = r'raw_Au4f_Mg2s_alpha=0deg_CoO_no_Au.txt'
        self.Au4f._60.experiment.filename = r'raw_Au4f_Mg2s_alpha=60deg.txt'

        self.Co2p._0.experiment.filename = r'raw_Co2p_alpha=0deg_CoO_no_Au.txt'
        self.Co2p._60.experiment.filename = r'raw_Co2p_alpha=60deg.txt'

        self.O1s._0.experiment.filename = r'raw_O1s_alpha=0deg_CoO_no_Au.txt'
        self.O1s._60.experiment.filename = r'raw_O1s_alpha=60deg.txt'

        self.Mg1s._0.experiment.filename = r'raw_Mg1s_alpha=0deg_CoO_no_Au.txt'
        self.Mg1s._60.experiment.filename = r'raw_Mg1s_alpha=60deg.txt'

        self.k_R_Au_0 = 1
        self.k_R_Au_60 = 0
        self.k_R_Co_0 = 1
        self.k_R_Co_60 = 0
        self.k_R_O_0 = 1
        self.k_R_O_60 = 0
        self.k_R_Mg_0 = 1
        self.k_R_Mg_60 = 0

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

            # The formatting of tick labels is controlled by a Formatter object,
            # which assuming you haven't done anything fancy will be a ScalerFormatterby default.
            # This formatter will use a constant shift if the fractional change of the values visible is very small.
            # To avoid this, simply turn it off:
            self.Co2p.axes.get_xaxis().get_major_formatter().set_scientific(False)
            self.Au4f.axes.get_xaxis().get_major_formatter().set_scientific(False)
            self.O1s.axes.get_xaxis().get_major_formatter().set_scientific(False)
            self.Mg1s.axes.get_xaxis().get_major_formatter().set_scientific(False)

            self.Co2p.axes.get_xaxis().get_major_formatter().set_useOffset(False)
            self.Au4f.axes.get_xaxis().get_major_formatter().set_useOffset(False)
            self.O1s.axes.get_xaxis().get_major_formatter().set_useOffset(False)
            self.Mg1s.axes.get_xaxis().get_major_formatter().set_useOffset(False)
            # plt.subplots_adjust(top=0.85)
            # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
            # self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

            # put window to the second monitor
            # figManager.window.setGeometry(1923, 23, 640, 529)
            self.figManager.window.setGeometry(1920, 20, 1920, 1180)

            # plt.show()
            plt.draw()
            self.fig.suptitle(self.suptitle_txt, fontsize=self.suptitle_fontsize, fontweight='normal')

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

        # use this variable to create full path to the experimental raw spectra:
        # self.modelName = 'model_with_Au'
        self.modelName = 'model_no_Au'

        # self.a.Au4f._0.experiment.filename = r'raw_Au4f_Mg2s_alpha=0deg_CoO_no_Au.txt'
        # self.a.Au4f._60.experiment.filename = r'raw_Au4f_Mg2s_alpha=60deg.txt'
        #
        # self.a.Co2p._0.experiment.filename = r'raw_Co2p_alpha=0deg_CoO_no_Au.txt'
        # self.a.Co2p._60.experiment.filename = r'raw_Co2p_alpha=60deg.txt'
        #
        # self.a.O1s._0.experiment.filename = r'raw_O1s_alpha=0deg_CoO_no_Au.txt'
        # self.a.O1s._60.experiment.filename = r'raw_O1s_alpha=60deg.txt'
        #
        # self.a.Mg1s._0.experiment.filename = r'raw_Mg1s_alpha=0deg_CoO_no_Au.txt'
        # self.a.Mg1s._60.experiment.filename = r'raw_Mg1s_alpha=60deg.txt'

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

        #                  Au        Co    CoOx     x    CoO      Au   MgO     MgCO3  MgOH   MgCO3_y_Mg[OH]2   y     Au    C=O
        self.x = np.array([200.000, 6.036, 0.0001, 0.9, 6.581, 0.0001, 20.779, 9.834, 4.534,       0.0001,    0.05, 3.888, 0.564])

    def calculateTheory(self):
        # run SESSA calculation with a new structure:
        if not self.checkStopFile(self.projPath):
            self.workFolder = create_out_data_folder(self.projPath, first_part_of_folder_name='')
            self.generateWorkPlace(self.workFolder)
            self.sample.workDir = self.workFolder

            #  layer 3 is a layer with mix of CoO and Au which takes 2 variables
            # layer 9 is mix of MgCO3 and MgOH
            if len(self.sample.layerStructure) == len(self.x)-2:
                for i in self.sample.layerStructure:
                    if i == 3:
                        self.sample.layerStructure[i]['material'].setThickness(self.x[i-1])
                        self.sample.layerStructure[i]['material'].set_x_amount_CoO_in_Au(self.x[i])
                        print('------------------ x CoO-Au is {} '.format(self.x[i]))
                    if i == 9:
                        self.sample.layerStructure[i]['material'].setThickness(self.x[i])
                        self.sample.layerStructure[i]['material'].set_x_amount_MgCO3_in_MgOH(self.x[i+1])
                        print('------------------ x MgCO3 in Mg[OH]2 is {} '.format(self.x[i+1]))
                    elif (i > 3) and (i < 9):
                        self.sample.layerStructure[i]['material'].setThickness(self.x[i])
                    elif i > 9:
                        self.sample.layerStructure[i]['material'].setThickness(self.x[i+1])
                    elif i < 3:
                        self.sample.layerStructure[i]['material'].setThickness(self.x[i - 1])

            else:
                print('Number of layers is not equal to dimension of minimization variable')
                print('You put: {0} but Class {1} need: {2}'.format(len(self.sample.layerStructure),
                                                                    self.__class__.__name__, len(self.x)-1))
                return 1
            # sample.Mg_Hydrate.setThickness(x[0])
            # sample.MgCO3.setThickness(x[1])
            # sample.MgO.setThickness(x[2])
            # sample.Au_interlayer.setThickness(x[3])
            # sample.Co_oxide.setThickness(x[4])
            # sample.Co_metal.setThickness(x[5])
            # sample.C_contamination.setThickness(x[6])

            self.sample.writeSesFile()
            # Saving the objects:
            pcklFile = os.path.join(self.workFolder, 'objs.pickle')
            with open(pcklFile, 'wb') as f:
                pickle.dump([self.sample], f)

            # # Getting back the objects:
            # with open(pcklFile, 'rb') as f:
            #     obj0 = pickle.load(f)
            self.returncode = execProjectSessionWithTimeoutControl(workDir=self.workFolder)
            self.clearWorkPlace(self.workFolder)

    def generateWorkPlace(self, dirPath=r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'):
        # created folder and copy the files:
        createFolder(os.path.join(dirPath, 'out'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'run.exe'),
                 os.path.join(dirPath, 'run.exe'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'exec.bat'),
                 os.path.join(dirPath, 'exec.bat'))
        # copyfile(os.path.join(runningScriptDir, 'exe', 'additional_commands_Co_no_Au.ses'),
        #          os.path.join(dirPath, 'additional_commands.ses'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'additional_commands_Co_no_Au_normalized.ses'),
                 os.path.join(dirPath, 'additional_commands.ses'))

    def setPeakRegions(self):
        self.a.Au4f._0.experiment.data.energyRegion = [1393.3, 1405]
        self.a.Au4f._0.theory.data.energyRegion = [1393.3, 1405]
        self.a.Au4f._60.experiment.data.energyRegion = [1393.3, 1405]
        self.a.Au4f._60.theory.data.energyRegion = [1393.3, 1405]

        self.a.Co2p._0.experiment.data.energyRegion = [702, 712.6]
        self.a.Co2p._0.theory.data.energyRegion = [702, 712.6]
        self.a.Co2p._60.experiment.data.energyRegion = [702, 712.6]
        self.a.Co2p._60.theory.data.energyRegion = [702, 712.6]

        self.a.O1s._0.experiment.data.energyRegion = [948.7, 960]
        self.a.O1s._0.theory.data.energyRegion = [948.7, 960]
        self.a.O1s._60.experiment.data.energyRegion = [948.7, 960]
        self.a.O1s._60.theory.data.energyRegion = [948.7, 960]

        self.a.Mg1s._0.experiment.data.energyRegion = [178, 185.6]
        self.a.Mg1s._0.theory.data.energyRegion = [178, 185.6]
        self.a.Mg1s._60.experiment.data.energyRegion = [178, 185.6]
        self.a.Mg1s._60.theory.data.energyRegion = [178, 185.6]


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    testCase = 3
    if testCase == 1:
        a = NumericData_CoO_no_Au()
        print('R0 = {}, R60 = {}'.format(a.k_R_Au_0, a.k_R_Au_60))
        a.theoryDataPath = r'/home/yugin/VirtualboxShare/Co-CoO/out/00003'
        a.loadExperimentData()
        a.loadTheoryData()

        print('R0 = {}, R60 = {}'.format(a.k_R_Au_0, a.k_R_Au_60))

        a.Au4f._0.experiment.data.energyRegion = [1395, 1405]
        a.Au4f._0.theory.data.energyRegion = [1395, 1405]
        a.Au4f._60.experiment.data.energyRegion = [1395, 1405]
        a.Au4f._60.theory.data.energyRegion = [1395, 1405]

        a.Co2p._0.experiment.data.energyRegion = [702, 710]
        a.Co2p._0.theory.data.energyRegion = [702, 710]
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
        #                 Au        Co    CoOx     x    CoO      Au       MgO     MgCO3  MgOH   MgCO3_y_Mg[OH]2   y       Au    C=O
        b1.x = np.array([200.000, 6.036, 0.0001, 0.9,   6.581,  0.0001, 20.779,   9.834, 4.534,    0.0001,      0.05,    3.888, 0.564])
        # calc theory and compare with experiment data:
        z = b1.compareTheoryAndExperiment()
        # b2 = Class_CoO_no_Au()
        # b2.x = [200.000, 15.000, 3.0, 0.001, 30.000, 15.000,7.000, 3.0, 5.000]
        # z = b2.compareTheoryAndExperiment()

