'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-12-29
'''

import os, sys
import datetime
from shutil import copyfile
from libs.dir_and_file_operations import create_out_data_folder, createFolder, listOfFilesFN_with_selected_ext
import numpy as np
from libs.dataProperties import NumericData
from libs.createSESSAprojectFile_CoO import SAMPLE
# from libs.CoO_Au_mix_classes import Sample_with_mix_of_CoO_Au, Class_for_mix_CoO_Au
from libs.execCommandInSESSA import execProjectSessionWithTimeoutControl
from libs.sample_CoO_no_Au_classes import Class_CoO_no_Au
from libs.sample_CoO_with_Au_classes import Class_CoO_with_Au

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

def func_CoO_no_Au(x, projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out', case_R_factor='all'):
    # main function for minimize:
    data = Class_CoO_no_Au()
    data.projPath = projPath
    data.x = x
    data.case_R_factor = case_R_factor
    # calculate total R-factor with the selected R-factors:
    if case_R_factor is 'without_Mg':
        data.k_R_Mg_0 = 0
        data.k_R_Mg_60 = 0
    if case_R_factor is 'without_Co_and_Au':
        data.k_R_Co_0 = 0
        data.k_R_Co_60 = 0
        data.k_R_Au_0 = 0
        data.k_R_Au_60 = 0
    if case_R_factor is 'without_O_and_Mg':
        data.k_R_O_0 = 0
        data.k_R_O_60 = 0
        data.k_R_Mg_0 = 0
        data.k_R_Mg_60 = 0
    # calc theory and compare with experiment data:
    data.compareTheoryAndExperiment()
    return data.a.total_R_faktor

def func_CoO_with_Au(x, projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out', case_R_factor='all'):
    # main function for minimize:
    data = Class_CoO_with_Au()
    data.projPath = projPath
    data.x = x
    data.case_R_factor = case_R_factor
    # calculate total R-factor with the selected R-factors:
    if case_R_factor is 'without_Mg':
        data.k_R_Mg_0 = 0
        data.k_R_Mg_60 = 0
    if case_R_factor is 'without_Co_and_Au':
        data.k_R_Co_0 = 0
        data.k_R_Co_60 = 0
        data.k_R_Au_0 = 0
        data.k_R_Au_60 = 0
    if case_R_factor is 'without_O_and_Mg':
        data.k_R_O_0 = 0
        data.k_R_O_60 = 0
        data.k_R_Mg_0 = 0
        data.k_R_Mg_60 = 0
    # calc theory and compare with experiment data:
    data.compareTheoryAndExperiment()
    return data.a.total_R_faktor


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))


    # x = np.array([6.036, 6.581, 20.779, 13.0, 0.05, 3.888, 0.564])
    # x = np.array([6.036, 6.581, 23.132, 22.0, 0.05, 3.552, 1.353])
    # x = np.array([9.036, 6.581, 23.132, 22.0, 0.05, 3.552, 1.353])
    # x = np.array([8.036, 7.581, 23.132, 22.0, 0.05, 3.552, 1.353])
    # #     Au        Co    CoOx  x    CoO      Au   MgO   MgCO3    MgOH   MgCO3_y_Mg[OH]2   y     Au    C=O
    # y = np.array(
    #     [200.000, x[0], 0.0001, 0.9, x[1], 0.0001, x[2], 0.0001, 0.0001, x[3], x[4], x[5], x[6]])
    # print('Answer is: {}'.format(func_CoO_no_Au (y)))
    # print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))




    # x = np.asarray([11.158, 8.349, 0.889, 5.04, 12.77, 0.562, 0.954])
    # #       Au    Co    CoOx     x   CoO   Au     MgO     MgCO3   MgOH    Au    C=O
    # y = np.array(
    #     [200.000, x[0], 0.0001, 0.7,  x[1], x[2],  x[3],    x[4],  x[5],  0.0001, x[6]])
    # print('Answer is: {}'.format(func_CoO_with_Au (y)))


    x = np.asarray([11.158, 8.349, 0.889, 5.04, 12.77, 0.562, 0.954])
    x = np.asarray([10.158, 6.349, 0.8, 5.04, 12.77, 0.562, 0.954])
    #       Au    Co    CoOx     x   CoO   Au     MgO     MgCO3   MgOH    Au    C=O
    y = np.array(
        [200.000, x[0], x[1], x[2], 0.0001, 0.0001, x[3], x[4], x[5], 0.0001, x[6]])
    print('Answer is: {}'.format(func_CoO_with_Au (y)))
    # print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))

