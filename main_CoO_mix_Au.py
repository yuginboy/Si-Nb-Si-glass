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

    case_R_factor = 'without_Mg'
    # timestamp = datetime.datetime.now().strftime("_[%Y-%m-%d_%H_%M_%S]_")
    # methodName = 'Nelder-Mead'
    methodName = 'randtobest1exp'
    # methodName = 'BFGS'
    newProjPath = create_out_data_folder(projPath, first_part_of_folder_name=methodName+'_CoO_Au_x__R_'+case_R_factor)



    # ====================================================================================================
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
    bounds = [(0.001, 5),  # MgOH
              (5, 15),  # MgCO3
              (5, 15),  # MgO
              (0.1, 0.9),  # x of (CoO)x_Au(1-x)
              (1, 7),  # (CoO)x_Au(1-x)
              (7, 25),  # Co
              (0.001, 5),  # C
              ]
    def fun(x):
        return func_mix_of_CoO_Au(x, projPath=newProjPath, case_R_factor=case_R_factor)
    try:
        result = differential_evolution(fun, bounds, maxiter=10000, disp=True, strategy='randtobest1exp')
    except KeyboardInterrupt:
        print('====***' * 15)
        print('==== stop-file was found: program has been finished')
        print('====***' * 15)
        sys.exit(0)





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