'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-12-22
Calculated by SESSA spectra for selected cases in CoO project.
sample:
substrate / Au[h=200A] / Co_metal[h=18A] / CoO[3h=A] / MgO [h=40A] / MgCO3 [h=5A] / Mg(OH)2[h=5A] <-- top surface
You can modify the thickness, percent of composition for all layers in investigated material.
The script use a differential_evolution method
'''
import sys
import os
import datetime
from io import StringIO
from shutil import copyfile
from libs.dir_and_file_operations import create_out_data_folder, createFolder

import numpy as np
import pickle
from libs.functionsForMinimize import func_CoO, func_mix_of_CoO_Au
from scipy.optimize import  differential_evolution
from scipy.optimize import minimize
from libs.dir_and_file_operations import create_out_data_folder

def startCalculation(projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out_genetic'):
    # Finds the global minimum of a multivariate function. Differential Evolution is stochastic in nature
    # (does not use gradient methods) to find the minimium, and can search large areas of candidate space,
    # but often requires larger numbers of function evaluations than conventional gradient based techniques.

    # case_mix_or_layers = 'layers' # with separates CoO and Au
    case_mix_or_layers = 'mix' # with mix interlayer

    # case_R_factor = 'without_Co_and_Au'
    case_R_factor = 'without_O_and_Mg'

    # timestamp = datetime.datetime.now().strftime("_[%Y-%m-%d_%H_%M_%S]_")
    # methodName = 'Nelder-Mead'
    methodName = 'randtobest1exp'
    # methodName = 'rand1exp'
    # methodName = 'BFGS'
    if case_mix_or_layers is 'layers':
        newProjPath = create_out_data_folder(projPath, first_part_of_folder_name=methodName+'_CoO_layers__R_'+case_R_factor)

        # ====================================================================================================
        # CoO and Au interlayer:
        def fun(x):
            # sample.Mg_Hydrate.thickness = x[0]
            # sample.MgCO3.thickness = x[1]
            # sample.MgO.thickness = x[2]
            # sample.Au_interlayer.thickness = x[3]
            # sample.Co_oxide.thickness = x[4]
            # sample.Co_metal.thickness = x[5]
            # sample.C_contamination.thickness = x[6]
            y = np.zeros(7)

            # 03306
            y[0] =  5.136
            y[1] =  11.186
            y[2] =  8.739
            y[3] = x[0]
            y[4] = x[1]
            y[5] = x[2]
            y[6] = 1.932
            return func_CoO(y, projPath=newProjPath, case_R_factor=case_R_factor)

        # # 1
        bounds = [
            (0.5, 10),  # Au
            (0.5, 10),  # CoO
            (1, 25),  # Co
                  ]



    if case_mix_or_layers is 'mix':
        newProjPath = create_out_data_folder(projPath, first_part_of_folder_name=methodName+'_CoO_mix__R_'+case_R_factor)
        # 2 for mix of CoO - Au
        # sample.Mg_Hydrate.thickness = x[0]
        # sample.MgCO3.thickness = x[1]
        # sample.MgO.thickness = x[2]
        # sample.CoO_Au_mix.set_x_amount_CoO_in_Au(x[3])
        # sample.CoO_Au_mix.thickness = x[4]
        # sample.Au_interlayer.thickness = 0.001
        # sample.Co_oxide.thickness = 0.001
        # sample.Co_metal.thickness = x[5]
        # sample.C_contamination.thickness = x[6]


        def fun(x):
            y = np.zeros(7)
            # 00841
            y[0] =  2.331
            y[1] =  11.667
            y[2] =  11.663
            y[3] = x[0]
            y[4] = x[1]
            y[5] = x[2]
            y[6] = 0.759
            # 03306
            y[0] =  5.136
            y[1] =  11.186
            y[2] =  8.739
            y[3] = x[0]
            y[4] = x[1]
            y[5] = x[2]
            y[6] = 1.932
            return func_mix_of_CoO_Au(y, projPath=newProjPath, case_R_factor=case_R_factor)
        # ====================================================================================================

        bounds = [
            (0.1, 0.9),  # x of (CoO)x_Au(1-x)
            (0.5, 10),  # (CoO)x_Au(1-x)
            (1, 25),  # Co
        ]

    result = differential_evolution(fun, bounds, maxiter=10000, disp=True, strategy=methodName, init='random')
    print('-*'*25)
    print('==  Answer is:')
    print (result)
    print('-*'*25)
    # print('Answer is: x= {0:1.3f}, R= {1}'(result.x, result.fun))




if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    startCalculation()