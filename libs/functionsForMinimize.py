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


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))
    print('Answer is: {}'.format(func_CoO_no_Au ([200.000, 10.000, 8.0, 0.001, 40.000, 5.000, 5.000, 3.0, 5.000])))
    print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))
    print('Answer is: {}'.format(func_CoO_with_Au ([200.000, 8.500, 3.0, 0.7, 0.1,   0.1, 11.000, 8.000, 3.000, 0.001, 4.000])))
    print('-----------> NumericData.global_R_factor = {0}'.format(NumericData.global_R_factor))

