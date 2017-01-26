'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-01-16
'''
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
from libs.dir_and_file_operations import createFolder
import pickle
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
import datetime
import numpy as np
from libs.dir_and_file_operations import get_folder_name, create_out_data_folder
from libs.classFuncMinimize import BaseClassForCalcAndMinimize, runningScriptDir
from libs.execCommandInSESSA import execProjectSessionWithTimeoutControl

# Create structure of layered material:
class SAMPLE_CoO_with_Au(SAMPLE):
    def __init__(self):
        super(SAMPLE_CoO_with_Au, self).__init__()

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
        # add Au 3A:
        self.addLayerToStructure(self.Au_top)
        # add C contamination on a surface:
        self.addLayerToStructure(self.C_contamination)


# Create Numerical data class for new sample:
class NumericData_CoO_with_Au(NumericData):
    def __init__(self):
        super(NumericData_CoO_with_Au, self).__init__()
        # self.colorsForGraph = ['darkviolet', 'dodgerblue', 'brown', 'red', 'darkviolet']
        self.Au4f._0.experiment.filename = r'raw_Au4f_Mg2s_alpha=0deg.txt'
        self.Au4f._60.experiment.filename = r'raw_Au4f_Mg2s_alpha=60deg.txt'

        self.Co2p._0.experiment.filename = r'raw_Co2p_alpha=0deg.txt'
        self.Co2p._60.experiment.filename = r'raw_Co2p_alpha=60deg.txt'

        self.O1s._0.experiment.filename = r'raw_O1s_alpha=0deg.txt'
        self.O1s._60.experiment.filename = r'raw_O1s_alpha=60deg.txt'

        self.Mg1s._0.experiment.filename = r'raw_Mg1s_alpha=0deg.txt'
        self.Mg1s._60.experiment.filename = r'raw_Mg1s_alpha=60deg.txt'

        self.k_R_Au_0 = 1
        self.k_R_Au_60 = 1
        self.k_R_Co_0 = 1
        self.k_R_Co_60 = 1
        self.k_R_O_0 = 1
        self.k_R_O_60 = 1
        self.k_R_Mg_0 = 1
        self.k_R_Mg_60 = 1

        self.suptitle_fontsize = 18

        # use only 1 iteration for bg subtraction:
        self.bg_sub_iterations = 2
        self.set_bg_sub_iterations()


class Class_CoO_with_Au(BaseClassForCalcAndMinimize):
    def __init__(self):
        self.sample = SAMPLE_CoO_with_Au()
        self.a = NumericData_CoO_with_Au()
        # use this variable to create full path to the experimental raw spectra:
        self.modelName = 'model_with_Au'

        self.projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out'
        self.case_R_factor = 'all'
        self.workFolder = self.projPath
        self.returncode = -1

        self.a.k_R_Co_0 =  1
        self.a.k_R_Co_60 = 1
        self.a.k_R_Au_0 =  1
        self.a.k_R_Au_60 = 1
        self.a.k_R_O_0 =   1
        self.a.k_R_O_60 =  1
        self.a.k_R_Mg_0 =  1
        self.a.k_R_Mg_60 = 1
        #                   Au        Co    CoOx x    CoO  Au  MgO     MgCO3  MgOH   Au    C=O
        self.x = np.array([200.000, 15.000, 3.0, 0.9, 4,   4, 40.000, 5.000, 5.000, 0.001, 5.000])

    def calculateTheory(self):
        # run SESSA calculation with a new structure:
        if not self.checkStopFile(self.projPath):
            self.workFolder = create_out_data_folder(self.projPath, first_part_of_folder_name='')
            self.generateWorkPlace(self.workFolder)
            self.sample.workDir = self.workFolder

            #  layer 3 is a layer with mix of CoO and Au which takes 2 variables
            if len(self.sample.layerStructure) == len(self.x)-1:
                for i in self.sample.layerStructure:
                    if i is 3:
                        self.sample.layerStructure[i]['material'].setThickness(self.x[i-1])
                        self.sample.layerStructure[i]['material'].set_x_amount_CoO_in_Au(self.x[i])
                        print('------------------ x CoO-Au is {} '.format(self.x[i]))
                    elif i > 3:
                        self.sample.layerStructure[i]['material'].setThickness(self.x[i])
                    elif i < 3:
                        self.sample.layerStructure[i]['material'].setThickness(self.x[i - 1])

            else:
                print('Number of layers is not equal to dimension of minimization variable')
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
            self.returncode = execProjectSessionWithTimeoutControl(workDir=self.workFolder, timeOut=120)
            self.clearWorkPlace(self.workFolder)

    def generateWorkPlace(self, dirPath=r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'):
        # created folder and copy the files:
        createFolder(os.path.join(dirPath, 'out'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'run.exe'),
                 os.path.join(dirPath, 'run.exe'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'exec.bat'),
                 os.path.join(dirPath, 'exec.bat'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'additional_commands_Co_with_Au_normalized.ses'),
                 os.path.join(dirPath, 'additional_commands.ses'))

    def setPeakRegions(self):
        self.a.Au4f._0.experiment.data.energyRegion = [1395, 1405]
        self.a.Au4f._0.theory.data.energyRegion = [1395, 1405]
        self.a.Au4f._60.experiment.data.energyRegion = [1395, 1405]
        self.a.Au4f._60.theory.data.energyRegion = [1395, 1405]

        self.a.Co2p._0.experiment.data.energyRegion = [702, 710]
        self.a.Co2p._0.theory.data.energyRegion = [702, 710]
        self.a.Co2p._60.experiment.data.energyRegion = [702, 710]
        self.a.Co2p._60.theory.data.energyRegion = [702, 710]

        self.a.O1s._0.experiment.data.energyRegion = [950, 960]
        self.a.O1s._0.theory.data.energyRegion = [950, 960]
        self.a.O1s._60.experiment.data.energyRegion = [950, 960]
        self.a.O1s._60.theory.data.energyRegion = [950, 960]

        self.a.Mg1s._0.experiment.data.energyRegion = [179, 185]
        self.a.Mg1s._0.theory.data.energyRegion = [179, 185]
        self.a.Mg1s._60.experiment.data.energyRegion = [179, 185]
        self.a.Mg1s._60.theory.data.energyRegion = [179, 185]


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    testCase = 3
    if testCase == 1:
        a = NumericData_CoO_with_Au()
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
        a = SAMPLE_CoO_with_Au()
        a.writeSesFile()
        a.getLayersStructureInfo()

    elif testCase == 3:
        b1 = Class_CoO_with_Au()
        #        Au        Co    CoOx  x  CoO  Au  MgO     MgCO3  MgOH   Au    C=O
        b1.x = [200.000, 8.500, 3.0, 0.7, 0.1,   0.1, 11.000, 8.000, 3.000, 0.0001, 4.000]
        # calc theory and compare with experiment data:
        z = b1.compareTheoryAndExperiment()
        # b2 = Class_CoO_no_Au()
        # b2.x = [200.000, 15.000, 3.0, 0.001, 30.000, 15.000,7.000, 3.0, 5.000]
        # z = b2.compareTheoryAndExperiment()

