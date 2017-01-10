'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-12-22
Calculated by SESSA spectra for selected cases in CoO project.
sample:
substrate / Au[h=200A] / Co_metal[h=18A] / CoO[3h=A] / MgO [h=40A] / MgCO3 [h=5A] / Mg(OH)2[h=5A] <-- top surface
You can modify the thickness, percent of composition for all layers in investigated material.
The script use a brute force method
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

    case_R_factor = 'without_Co_and_Au'
    # timestamp = datetime.datetime.now().strftime("_[%Y-%m-%d_%H_%M_%S]_")
    # methodName = 'Nelder-Mead'
    # methodName = 'randtobest1exp'
    methodName = 'rand1exp'
    # methodName = 'BFGS'
    newProjPath = create_out_data_folder(projPath, first_part_of_folder_name=methodName+'_CoO_Au__R_'+case_R_factor)

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
        y[0] = x[0]
        y[1] = x[1]
        y[2] = x[2]
        y[3] = 3
        y[4] = 3
        y[5] = 18
        y[6] = x[3]
        return func_CoO(y, projPath=newProjPath, case_R_factor=case_R_factor)

    # # 1
    bounds = [(0.001, 5),  # MgOH
              (5, 15),  # MgCO3
              (5, 15),  # MgO
              (0.001, 5),  # C
              ]
    result = differential_evolution(fun, bounds, maxiter=10000, disp=True, strategy=methodName)



    # sample.Mg_Hydrate.thickness = x[0]
    # sample.MgCO3.thickness = x[1]
    # sample.MgO.thickness = x[2]
    # sample.Au_interlayer.thickness = x[3]
    # sample.Co_oxide.thickness = x[4]
    # sample.Co_metal.thickness = x[5]
    # sample.C_contamination.thickness = x[6]
    # x0 = [0.713,
    #       11.262,
    #       11.916,
    #       2.358,
    #       3.116,
    #       16.33,
    #       1.837]

    # 3306
    # x0 = [5.136,
    #       11.186,
    #       8.739,
    #       0.835,
    #       2.427,
    #       9.766,
    #       1.932]
    # result = minimize(fun, x0, )
    # result = minimize(fun, x0, method=methodName, options={'maxiter' : 10000}, tol=1e-6)
    # result = minimize(fun, x0, method=methodName, options={'gtol': 1e-6, 'disp': True, 'maxiter' : 10000})

    print('-*'*25)
    print('==  Answer is:')
    print (result)
    print('-*'*25)
    # print('Answer is: x= {0:1.3f}, R= {1}'(result.x, result.fun))




if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    startCalculation()