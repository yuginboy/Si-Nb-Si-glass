'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-01-13
The base classes for minimization procedure
'''
import os, sys
import datetime
from shutil import copyfile
from libs.dir_and_file_operations import create_out_data_folder, createFolder, listOfFilesFN_with_selected_ext, \
                                        create_unique_out_data_file
import numpy as np
from libs.dataProperties import NumericData
from libs.createSESSAprojectFile_CoO import SAMPLE
from libs.CoO_Au_mix_classes import Sample_with_mix_of_CoO_Au, Class_for_mix_CoO_Au
from libs.execCommandInSESSA import execProjectSessionWithTimeoutControl
import numpy as np
import pickle

runningScriptDir = os.path.dirname(os.path.abspath(__file__))
# get root project folder name:
runningScriptDir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

class BaseClassForCalcAndMinimize():
    # tmp value of global minimal R-factor (used for copy current global_min_R_factor to the kernel project dir):
    tmp_global_min_R_factor = 10
    def __init__(self):
        self.sample = SAMPLE()
        self.a = NumericData()

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

        self.x = np.array([200.000, 15.000, 0.001, 0.001, 50.000, 5.000, 5.000, 5.000])

    def generateWorkPlace(self, dirPath=r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'):
        # created folder and copy the files:
        createFolder(os.path.join(dirPath, 'out'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'run.exe'),
                 os.path.join(dirPath, 'run.exe'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'exec.bat'),
                 os.path.join(dirPath, 'exec.bat'))
        copyfile(os.path.join(runningScriptDir, 'exe', 'additional_commands.ses'),
                 os.path.join(dirPath, 'additional_commands.ses'))

    def clearWorkPlace(self, dirPath=r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'):
        # remove all standard files:
        os.remove(os.path.join(dirPath, 'run.exe'))
        os.remove(os.path.join(dirPath, 'exec.bat'))
        # os.remove(os.path.join(dirPath, 'additional_commands.ses'))

    def checkStopFile(self, dirPath=r'/home/yugin/VirtualboxShare/Co-CoO/out/', stopFileName='stop'):
        # return 1 if stop file is placed in the project working directory
        if os.path.isfile(os.path.join(dirPath, stopFileName)):
            return 1
        else:
            return 0

    def calculateTheory(self):
        # run SESSA calculation with a new structure:
        if not self.checkStopFile(self.projPath):
            self.workFolder = create_out_data_folder(self.projPath, first_part_of_folder_name='')
            self.generateWorkPlace(self.workFolder)
            self.sample.workDir = self.workFolder


            if len(self.sample.layerStructure) == len(self.x):
                for i in self.sample.layerStructure:
                    self.sample.layerStructure[i]['material'].setThickness(self.x[i-1])
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
    def checkCase_R_factor(self):

        if self.case_R_factor is 'without_Mg':
            self.a.k_R_Mg_0 = 0
            self.a.k_R_Mg_60 = 0
        if self.case_R_factor is 'without_Co_and_Au':
            self.a.k_R_Co_0 = 0
            self.a.k_R_Co_60 = 0
            self.a.k_R_Au_0 = 0
            self.a.k_R_Au_60 = 0
        if self.case_R_factor is 'without_O_and_Mg':
            self.a.k_R_O_0 = 0
            self.a.k_R_O_60 = 0
            self.a.k_R_Mg_0 = 0
            self.a.k_R_Mg_60 = 0

    def setPeakRegions(self):
        self.a.Au4f._0.experiment.data.energyRegion = [1395, 1405]
        self.a.Au4f._0.theory.data.energyRegion = [1395, 1405]
        self.a.Au4f._60.experiment.data.energyRegion = [1395, 1405]
        self.a.Au4f._60.theory.data.energyRegion = [1395, 1405]

        self.a.Co2p._0.experiment.data.energyRegion = [700, 710]
        self.a.Co2p._0.theory.data.energyRegion = [700, 710]
        self.a.Co2p._60.experiment.data.energyRegion = [700, 710]
        self.a.Co2p._60.theory.data.energyRegion = [700, 710]

        self.a.O1s._0.experiment.data.energyRegion = [950, 960]
        self.a.O1s._0.theory.data.energyRegion = [950, 960]
        self.a.O1s._60.experiment.data.energyRegion = [950, 960]
        self.a.O1s._60.theory.data.energyRegion = [950, 960]

        self.a.Mg1s._0.experiment.data.energyRegion = [179, 185]
        self.a.Mg1s._0.theory.data.energyRegion = [179, 185]
        self.a.Mg1s._60.experiment.data.energyRegion = [179, 185]
        self.a.Mg1s._60.theory.data.energyRegion = [179, 185]

    def applyGlobalIntensityNormalization(self):
        # start to Global Normolize procedure:
        self.a.Au4f._0.getMaxIntensityValue()
        self.a.Au4f._60.getMaxIntensityValue()
        # print('a.Au4f._0.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._0.experiment.data.fit.maxIntensity))
        # print('a.Au4f._0.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._0.theory.data.fit.maxIntensity))
        # print('a.Au4f._60.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._60.experiment.data.fit.maxIntensity))
        # print('a.Au4f._60.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._60.theory.data.fit.maxIntensity))

        self.a.Co2p._0.getMaxIntensityValue()
        self.a.Co2p._60.getMaxIntensityValue()
        # print('a.Co2p._0.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._0.experiment.data.fit.maxIntensity))
        # print('a.Co2p._0.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._0.theory.data.fit.maxIntensity))
        # print('a.Co2p._60.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._60.experiment.data.fit.maxIntensity))
        # print('a.Co2p._60.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._60.theory.data.fit.maxIntensity))

        self.a.O1s._0.getMaxIntensityValue()
        self.a.O1s._60.getMaxIntensityValue()
        # print('a.O1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._0.experiment.data.fit.maxIntensity))
        # print('a.O1s._0.theory.data.fit.maxIntensity = {0}'.format(a.O1s._0.theory.data.fit.maxIntensity))
        # print('a.O1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._60.experiment.data.fit.maxIntensity))
        # print('a.O1s._60.theory.data.fit.maxIntensity = {0}'.format(a.O1s._60.theory.data.fit.maxIntensity))

        self.a.Mg1s._0.getMaxIntensityValue()
        self.a.Mg1s._60.getMaxIntensityValue()
        # print('a.Mg1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.experiment.data.fit.maxIntensity))
        # print('a.Mg1s._0.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.theory.data.fit.maxIntensity))
        # print('a.Mg1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.experiment.data.fit.maxIntensity))
        # print('a.Mg1s._60.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.theory.data.fit.maxIntensity))

        maxIntensity_0_theory = np.max(
            [self.a.Au4f._0.theory.data.fit.maxIntensity, self.a.Co2p._0.theory.data.fit.maxIntensity,
             self.a.O1s._0.theory.data.fit.maxIntensity,  self.a.Mg1s._0.theory.data.fit.maxIntensity])
        maxIntensity_60_theory = np.max(
            [self.a.Au4f._60.theory.data.fit.maxIntensity, self.a.Co2p._60.theory.data.fit.maxIntensity,
             self.a.O1s._60.theory.data.fit.maxIntensity,  self.a.Mg1s._60.theory.data.fit.maxIntensity])

        maxIntensity_0_experiment = np.max(
            [self.a.Au4f._0.experiment.data.fit.maxIntensity, self.a.Co2p._0.experiment.data.fit.maxIntensity,
             self.a.O1s._0.experiment.data.fit.maxIntensity,  self.a.Mg1s._0.experiment.data.fit.maxIntensity])
        maxIntensity_60_experiment = np.max(
            [self.a.Au4f._60.experiment.data.fit.maxIntensity, self.a.Co2p._60.experiment.data.fit.maxIntensity,
             self.a.O1s._60.experiment.data.fit.maxIntensity,  self.a.Mg1s._60.experiment.data.fit.maxIntensity])

        self.a.Au4f._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
        self.a.Au4f._0.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_0_theory

        self.a.Co2p._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
        self.a.Co2p._0.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_0_theory

        self.a.O1s._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
        self.a.O1s._0.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_0_theory

        self.a.Mg1s._0.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_0_experiment
        self.a.Mg1s._0.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_0_theory

        self.a.Au4f._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
        self.a.Au4f._60.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_60_theory

        self.a.Co2p._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
        self.a.Co2p._60.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_60_theory

        self.a.O1s._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
        self.a.O1s._60.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_60_theory

        self.a.Mg1s._60.valueForNormalizingSpectraInAllRegions_experiment = maxIntensity_60_experiment
        self.a.Mg1s._60.valueForNormalizingSpectraInAllRegions_theory = maxIntensity_60_theory

    def compareTheoryAndExperiment(self):

        self.calculateTheory()
        if not self.checkStopFile(self.projPath):
            # calculate total R-factor with the selected R-factors:
            self.checkCase_R_factor()

            if self.returncode is not -1:
                # if process has been finished properly:
                self.a.theoryDataPath = self.workFolder
                self.a.experimentDataPath = r'/home/yugin/PycharmProjects/Si-Nb-Si-glass/exe/raw'
                self.a.loadExperimentData()
                self.a.loadTheoryData()

                self.setPeakRegions()
                self.applyGlobalIntensityNormalization()


                self.a.setupAxes()
                self.a.updatePlot()
                print('=*' * 15)
                print('-> total R-factor is: {}'.format(self.a.total_R_faktor))
                self.a.set_global_R_factor()
                self.a.get_global_R_factor()
                self.a.set_global_min_R_factor(structure=self.sample)
                self.a.get_global_min_R_factor()
                optimal_structure = self.a.get_global_min_R_factor_Structure()
                print('-> global minimum R-factor is: {}'.format(self.a.global_min_R_factor))
                print('-> global minimum R-factor project folder: {}'.format(self.a.global_min_R_factor_path))
                print('-> |R - Rmin| = {}'.format(np.abs(self.a.global_min_R_factor - self.a.total_R_faktor)))
                print('Optimal structure:\n')
                print(optimal_structure.getLayersStructureInfo())
                print('=*' * 15)
                print('\n'*3)
                print('---> going to the next step')
                self.copyCurrentMinimumParametersToTheKernelProjectFolder()
            else:
                self.a.get_global_R_factor()
                self.a.total_R_faktor = self.a.total_R_faktor + 0.1
                self.copyCurrentMinimumParametersToTheKernelProjectFolder()

            return self.a.total_R_faktor
        else:
            print('====***' * 15)
            print('==== stop-file was found: program has been finished')
            print('====***' * 15)
            self.a.get_global_R_factor()
            self.a.get_global_min_R_factor()
            optimal_structure = self.a.get_global_min_R_factor_Structure()
            print('-> global minimum R-factor is: {}'.format(self.a.global_min_R_factor))
            print('-> global minimum R-factor project folder: {}'.format(self.a.global_min_R_factor_path))
            print('-> |R - Rmin| = {}'.format(np.abs(self.a.global_min_R_factor - self.a.total_R_faktor)))
            print('Optimal structure:\n')
            print(optimal_structure.getLayersStructureInfo())
            print('====***' * 15)

            textFile = open(os.path.join(self.projPath, 'readme.txt'), 'a')
            # load calculated data from the best case:
            lsFiles = listOfFilesFN_with_selected_ext(folder=self.a.global_min_R_factor_path)
            copyfile(lsFiles[-1],
                     os.path.join(self.projPath, os.path.basename(lsFiles[-1])))

            textFile.write('\n')
            textFile.write('-> global minimum R-factor is: {}'.format(self.a.global_min_R_factor))
            textFile.write('\n')
            textFile.write('-> global minimum R-factor project folder: {}'.format(self.a.global_min_R_factor_path))
            textFile.write('\n')
            textFile.write('-> |R - Rmin| = {}'.format(np.abs(self.a.global_min_R_factor - self.a.total_R_faktor)))
            textFile.write('\n')
            textFile.write('Optimal structure:\n')
            textFile.write(optimal_structure.tabledLayersStructureInfo)
            textFile.close()

            sys.exit(0)

            return self.a.total_R_faktor

    def copyCurrentMinimumParametersToTheKernelProjectFolder(self):
        self.a.get_global_R_factor()
        self.a.get_global_min_R_factor()
        if BaseClassForCalcAndMinimize.tmp_global_min_R_factor > self.a.global_min_R_factor:

            BaseClassForCalcAndMinimize.tmp_global_min_R_factor = self.a.global_min_R_factor

            optimal_structure = self.a.get_global_min_R_factor_Structure()

            fpath = create_unique_out_data_file(self.projPath, first_part_of_file_name='min_R', ext='txt')
            textFile = open(fpath, 'a')
            # load calculated data from the best case:
            lsFiles = listOfFilesFN_with_selected_ext(folder=self.a.global_min_R_factor_path)
            copyfile(lsFiles[-1],
                     os.path.join(self.projPath, os.path.basename(lsFiles[-1])))

            textFile.write('\n')
            textFile.write('-> global minimum R-factor is: {}'.format(self.a.global_min_R_factor))
            textFile.write('\n')
            textFile.write('-> global minimum R-factor project folder: {}'.format(self.a.global_min_R_factor_path))
            textFile.write('\n')
            textFile.write('-> |R - Rmin| = {}'.format(np.abs(self.a.global_min_R_factor - self.a.total_R_faktor)))
            textFile.write('\n')
            textFile.write('\n')
            textFile.write('Optimal structure:\n')
            textFile.write(optimal_structure.tabledLayersStructureInfo)
            textFile.close()




if __name__=='__main__':

    print('-> you run ', __file__, ' file in a main mode')
    obj = BaseClassForCalcAndMinimize()
    obj.x = [200.000, 15.000, 1, 0.001, 40.000, 5.000, 2.000, 5.000]
    z = obj.compareTheoryAndExperiment()
    print('Answer is: {}'.format(z))
    obj1 = BaseClassForCalcAndMinimize()
    obj1.x = [200.000, 15.000, 1, 0.001, 40.000, 5.000, 3.000, 3.000]
    z = obj1.compareTheoryAndExperiment()
    print('Answer is: {}'.format(z))
    print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))