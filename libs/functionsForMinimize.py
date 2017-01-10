'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-12-29
'''

import os
import datetime
from shutil import copyfile
from libs.dir_and_file_operations import create_out_data_folder, createFolder
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


def generateWorkPlace(dirPath = r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'):
    # created folder and copy the files:
    createFolder(os.path.join(dirPath, 'out'))
    copyfile(os.path.join(runningScriptDir, 'exe', 'run.exe'),
             os.path.join(dirPath, 'run.exe'))
    copyfile(os.path.join(runningScriptDir, 'exe', 'exec.bat'),
             os.path.join(dirPath, 'exec.bat'))
    copyfile(os.path.join(runningScriptDir, 'exe', 'additional_commands.ses'),
             os.path.join(dirPath, 'additional_commands.ses'))

def clearWorkPlace(dirPath = r'/home/yugin/VirtualboxShare/Co-CoO/out/00001'):
    # remove all standard files:
    os.remove(os.path.join(dirPath, 'run.exe'))
    os.remove(os.path.join(dirPath, 'exec.bat'))
    # os.remove(os.path.join(dirPath, 'additional_commands.ses'))

def checkStopFile(dirPath = r'/home/yugin/VirtualboxShare/Co-CoO/out/', stopFileName='stop'):
    # return 1 if stop file is placed in the project working directory
    if os.path.isfile(os.path.join(dirPath, stopFileName)):
        return 1
    else:
        return 0


def func_CoO(x, projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out', case_R_factor='all'):
    # main function for minimize:
    sample = SAMPLE()
    workFolder = create_out_data_folder(projPath, first_part_of_folder_name = '')
    generateWorkPlace(workFolder)
    sample.workDir = workFolder


    sample.Mg_Hydrate.thickness = x[0]
    sample.MgCO3.thickness = x[1]
    sample.MgO.thickness = x[2]
    sample.Au_interlayer.thickness = x[3]
    sample.Co_oxide.thickness = x[4]
    sample.Co_metal.thickness = x[5]
    sample.C_contamination.thickness = x[6]

    sample.writeSesFile()
    # Saving the objects:
    pcklFile = os.path.join(workFolder, 'objs.pickle')
    with open(pcklFile, 'wb') as f:
        pickle.dump([sample], f)

    # # Getting back the objects:
    # with open(pcklFile, 'rb') as f:
    #     obj0 = pickle.load(f)
    returncode = execProjectSessionWithTimeoutControl(workDir=workFolder, timeOut=120)
    clearWorkPlace(workFolder)
    a = NumericData()
    # calculate total R-factor with the selected R-factors:
    if case_R_factor is 'without_Mg':
        a.k_R_Mg_0 = 0
        a.k_R_Mg_60 = 0
    if returncode is not -1:
        # if process has been finished properly:
        a.theoryDataPath = workFolder
        a.experimentDataPath = r'/home/yugin/PycharmProjects/Si-Nb-Si-glass/exe/raw'
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

        # start to Global Normolize procedure:
        a.Au4f._0.getMaxIntensityValue()
        a.Au4f._60.getMaxIntensityValue()
        # print('a.Au4f._0.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._0.experiment.data.fit.maxIntensity))
        # print('a.Au4f._0.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._0.theory.data.fit.maxIntensity))
        # print('a.Au4f._60.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._60.experiment.data.fit.maxIntensity))
        # print('a.Au4f._60.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._60.theory.data.fit.maxIntensity))

        a.Co2p._0.getMaxIntensityValue()
        a.Co2p._60.getMaxIntensityValue()
        # print('a.Co2p._0.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._0.experiment.data.fit.maxIntensity))
        # print('a.Co2p._0.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._0.theory.data.fit.maxIntensity))
        # print('a.Co2p._60.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._60.experiment.data.fit.maxIntensity))
        # print('a.Co2p._60.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._60.theory.data.fit.maxIntensity))

        a.O1s._0.getMaxIntensityValue()
        a.O1s._60.getMaxIntensityValue()
        # print('a.O1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._0.experiment.data.fit.maxIntensity))
        # print('a.O1s._0.theory.data.fit.maxIntensity = {0}'.format(a.O1s._0.theory.data.fit.maxIntensity))
        # print('a.O1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._60.experiment.data.fit.maxIntensity))
        # print('a.O1s._60.theory.data.fit.maxIntensity = {0}'.format(a.O1s._60.theory.data.fit.maxIntensity))

        a.Mg1s._0.getMaxIntensityValue()
        a.Mg1s._60.getMaxIntensityValue()
        # print('a.Mg1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.experiment.data.fit.maxIntensity))
        # print('a.Mg1s._0.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.theory.data.fit.maxIntensity))
        # print('a.Mg1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.experiment.data.fit.maxIntensity))
        # print('a.Mg1s._60.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.theory.data.fit.maxIntensity))

        maxIntensity_0_theory = np.max(
            [a.Au4f._0.theory.data.fit.maxIntensity, a.Co2p._0.theory.data.fit.maxIntensity,
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

        a.setupAxes()
        a.updatePlot()
        print('=*'*15)
        print('-> total R-factor is: {}'.format(a.total_R_faktor))
        a.set_global_R_factor()
        a.get_global_R_factor()
        a.set_global_min_R_factor()
        a.get_global_min_R_factor()
        print('-> global minimum R-factor is: {}'.format(a.global_min_R_factor))
        print('-> global minimum R-factor project folder: {}'.format(a.global_min_R_factor_path))
        print('-> |R - Rmin| = {}'.format( np.abs(a.global_min_R_factor - a.total_R_faktor)) )
        print('=*'*15)

    else:
        a.get_global_R_factor()
        a.total_R_faktor = a.total_R_faktor + 0.1


    return a.total_R_faktor

def func_mix_of_CoO_Au(x, projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out', case_R_factor = 'without_Mg'):
    # main function for minimize:

    if not checkStopFile(projPath):

        sample = Sample_with_mix_of_CoO_Au()
        workFolder = create_out_data_folder(projPath, first_part_of_folder_name = '')
        generateWorkPlace(workFolder)
        sample.workDir = workFolder


        sample.Mg_Hydrate.thickness = x[0]
        sample.MgCO3.thickness = x[1]
        sample.MgO.thickness = x[2]
        sample.CoO_Au_mix.set_x_amount_CoO_in_Au(x[3])
        sample.CoO_Au_mix.thickness = x[4]
        sample.Au_interlayer.thickness = 0.001
        sample.Co_oxide.thickness = 0.001
        sample.Co_metal.thickness = x[5]
        sample.C_contamination.thickness = x[6]

        sample.writeSesFile()
        # Saving the objects:
        pcklFile = os.path.join(workFolder, 'objs.pickle')
        with open(pcklFile, 'wb') as f:
            pickle.dump([sample], f)

        # # Getting back the objects:
        # with open(pcklFile, 'rb') as f:
        #     obj0 = pickle.load(f)
        returncode = execProjectSessionWithTimeoutControl(workDir=workFolder, timeOut=120)
        clearWorkPlace(workFolder)
        a = Class_for_mix_CoO_Au()

        # calculate total R-factor with the selected R-factors:
        if case_R_factor is 'without_Mg':
            a.k_R_Mg_0 = 0
            a.k_R_Mg_60 = 0


        if returncode is not -1:
            # if process has been finished properly:
            a.theoryDataPath = workFolder
            a.experimentDataPath = r'/home/yugin/PycharmProjects/Si-Nb-Si-glass/exe/raw'
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

            # start to Global Normolize procedure:
            a.Au4f._0.getMaxIntensityValue()
            a.Au4f._60.getMaxIntensityValue()
            # print('a.Au4f._0.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._0.experiment.data.fit.maxIntensity))
            # print('a.Au4f._0.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._0.theory.data.fit.maxIntensity))
            # print('a.Au4f._60.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._60.experiment.data.fit.maxIntensity))
            # print('a.Au4f._60.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._60.theory.data.fit.maxIntensity))

            a.Co2p._0.getMaxIntensityValue()
            a.Co2p._60.getMaxIntensityValue()
            # print('a.Co2p._0.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._0.experiment.data.fit.maxIntensity))
            # print('a.Co2p._0.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._0.theory.data.fit.maxIntensity))
            # print('a.Co2p._60.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._60.experiment.data.fit.maxIntensity))
            # print('a.Co2p._60.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._60.theory.data.fit.maxIntensity))

            a.O1s._0.getMaxIntensityValue()
            a.O1s._60.getMaxIntensityValue()
            # print('a.O1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._0.experiment.data.fit.maxIntensity))
            # print('a.O1s._0.theory.data.fit.maxIntensity = {0}'.format(a.O1s._0.theory.data.fit.maxIntensity))
            # print('a.O1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._60.experiment.data.fit.maxIntensity))
            # print('a.O1s._60.theory.data.fit.maxIntensity = {0}'.format(a.O1s._60.theory.data.fit.maxIntensity))

            a.Mg1s._0.getMaxIntensityValue()
            a.Mg1s._60.getMaxIntensityValue()
            # print('a.Mg1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.experiment.data.fit.maxIntensity))
            # print('a.Mg1s._0.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.theory.data.fit.maxIntensity))
            # print('a.Mg1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.experiment.data.fit.maxIntensity))
            # print('a.Mg1s._60.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.theory.data.fit.maxIntensity))

            maxIntensity_0_theory = np.max(
                [a.Au4f._0.theory.data.fit.maxIntensity, a.Co2p._0.theory.data.fit.maxIntensity,
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

            a.setupAxes()
            a.updatePlot()
            print('=*'*15)
            print('-> total R-factor is: {}'.format(a.total_R_faktor))
            a.set_global_R_factor()
            a.get_global_R_factor()
            a.set_global_min_R_factor()
            a.get_global_min_R_factor()
            print('-> global minimum R-factor is: {}'.format(a.global_min_R_factor))
            print('-> global minimum R-factor project folder: {}'.format(a.global_min_R_factor_path))
            print('-> |R - Rmin| = {}'.format( np.abs(a.global_min_R_factor - a.total_R_faktor)) )
            print('=*'*15)

        else:
            a.get_global_R_factor()
            a.total_R_faktor = a.total_R_faktor + 0.1


        return a.total_R_faktor
    else:
        print('====***' * 15)
        print('==== stop-file was found: program has been finished')
        print('====***' * 15)
        return 0




if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    # print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))
    #  print('Answer is: {}'.format(func_CoO ([1, 10, 15, 3, 3, 15, 1])))
    print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))
    print('Answer is: {}'.format(func_mix_of_CoO_Au ([10, 10, 15, 0.6, 3, 15, 2])))
    print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))