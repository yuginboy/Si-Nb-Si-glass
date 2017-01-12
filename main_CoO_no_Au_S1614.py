'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-01-12
'''
import sys
import os
import datetime
from io import StringIO
from shutil import copyfile
from libs.dir_and_file_operations import create_out_data_folder, createFolder

import numpy as np
import pickle
from libs.functionsForMinimize import func_CoO_no_Au, func_mix_of_CoO_no_Au
from scipy.optimize import  differential_evolution
from scipy.optimize import basinhopping, brute
from scipy.optimize import minimize
from libs.dir_and_file_operations import create_out_data_folder
from libs.minimization_additions import SESSA_Step

def startCalculation(projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out_genetic_CoO_no_Au'):
    # Finds the global minimum of a multivariate function. Differential Evolution is stochastic in nature
    # (does not use gradient methods) to find the minimium, and can search large areas of candidate space,
    # but often requires larger numbers of function evaluations than conventional gradient based techniques.

    case_mix_or_layers = 'layers' # with separates CoO and Au
    # case_mix_or_layers = 'mix'  # with mix interlayer

    # case_R_factor = 'without_Co_and_Au'
    # case_R_factor = 'without_O_and_Mg'
    case_R_factor = 'all_lines'

    # case_optimize_method = 'differential evolution'
    case_optimize_method = 'basinhopping'
    # case_optimize_method = 'brute force'

    # timestamp = datetime.datetime.now().strftime("_[%Y-%m-%d_%H_%M_%S]_")
    # methodName = 'Nelder-Mead'
    methodName = 'randtobest1exp'
    minimizer_kwargs = {"method": "L-BFGS-B", "jac": False}
    # methodName = 'rand1exp'
    # methodName = 'BFGS'

    if case_optimize_method is 'differential evolution':
        optimize_method = 'de'
    if case_optimize_method is 'brute force':
        optimize_method = 'brute'
        methodName = ''
    if case_optimize_method is 'basinhopping':
        optimize_method = 'bh'
        methodName = minimizer_kwargs['method']

    if case_mix_or_layers is 'layers':
        newProjPath = create_out_data_folder(projPath,
                                             first_part_of_folder_name=optimize_method + '_' + methodName + '_CoO_layers__R_' + case_R_factor)

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

            # # 03306
            # y[0] = 5.136
            # y[1] = 11.186
            # y[2] = 8.739
            # y[3] = x[0]
            # y[4] = x[1]
            # y[5] = x[2]
            # y[6] = 1.932
            y = x
            return func_CoO_no_Au(y, projPath=newProjPath, case_R_factor=case_R_factor)

        # ====================================================================================================
        # # 1
        bounds = [
                  (0.001, 15),  # MgOH
                  (5, 35),  # MgCO3
                  (5, 35),  # MgO
                  (1, 7),  # Au
                  (1, 7),  # CoO
                  (7, 25),  # Co
                  (0.001, 8),  # C
                  ]
        # 3306
        # x0 = [5.136,
        #       11.186,
        #       8.739,
        #       0.835,
        #       2.427,
        #       9.766,
        #       1.932,
        #       ]

        # -> global minimum R-factor is: 0.4469234152433788
        # -> global minimum R-factor project folder: /home/yugin/VirtualboxShare/Co-CoO/out_genetic/bh_L-BFGS-B_CoO_layers__R_all_lines_00002/00001
        # x0 = [5.136,
        #       11.186,
        #       8.739,
        #       1.000,1.1
        #       2.427,
        #       9.766,
        #       1.932,
        #       ]
        x0 = [5.136,
              11.186,
              28.739,
              0.01,
              2.2,
              10.5,
              1.932,
              ]

        rranges = (
            slice(0.001, 8, 0.2),  # MgOH
            slice(5, 15, 0.2),  # MgCO3
            slice(5, 15, 0.2),  # MgO
            slice(1, 7, 0.2),  # Au
            slice(1, 7, 0.2),  # CoO
            slice(7, 25, 0.2),  # Co
            slice(0.001, 8, 0.2),  # C
        )

    if case_mix_or_layers is 'mix':
        newProjPath = create_out_data_folder(projPath,
                                             first_part_of_folder_name=optimize_method + '_' + methodName + '_CoO_mix__R_' + case_R_factor)

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
            # # 00841
            # y[0] = 2.331
            # y[1] = 11.667
            # y[2] = 11.663
            # y[3] = x[0]
            # y[4] = x[1]
            # y[5] = x[2]
            # y[6] = 0.759
            # # 03306
            # y[0] = 5.136
            # y[1] = 11.186
            # y[2] = 8.739
            # y[3] = x[0]
            # y[4] = x[1]
            # y[5] = x[2]
            # y[6] = 1.932
            y = x
            return func_mix_of_CoO_no_Au(y, projPath=newProjPath, case_R_factor=case_R_factor)

        # ====================================================================================================

        # # /home/yugin/VirtualboxShare/Co-CoO/out_genetic/randtobest1exp_CoO_mix__R_without_O_and_Mg_00001/00078
        # x0 = [
        #       5.136,   # MgOH
        #       11.186,  # MgCO3
        #       8.739,   # MgO
        #       0.863,   # x of (CoO)x_Au(1-x)
        #       2.212,   # (CoO)x_Au(1-x)
        #       8.975,   # Co
        #       1.932    # C
        #       ]
        # /home/yugin/VirtualboxShare/Co-CoO/out_genetic/randtobest1exp_CoO_mix__R_without_O_and_Mg_00001/00181
        x0 = [
              5.136,   # MgOH
              11.186,  # MgCO3
              28.739,   # MgO
              0.708,   # x of (CoO)x_Au(1-x)
              3.073,   # (CoO)x_Au(1-x)
              9.598,   # Co
              1.932    # C
              ]

        # ====================================================================================================
        bounds = [
                  (0.001, 15),  # MgOH
                  (7, 35),  # MgCO3
                  (7, 35),  # MgO
                  (0.05, 0.95),  # x of (CoO)x_Au(1-x)
                  (1, 7),  # (CoO)x_Au(1-x)
                  (7, 25),  # Co
                  (0.001, 8),  # C
                  ]
        rranges = (
            slice(0.001, 8, 0.5),  # MgOH
            slice(7, 15, 0.5),  # MgCO3
            slice(7, 15, 0.5),  # MgO
            slice(0.05, 0.95, 0.1),  # x of (CoO)x_Au(1-x)
            slice(1, 7, 0.5),  # (CoO)x_Au(1-x)
            slice(7, 25, 1),  # Co
            slice(0.001, 8, 0.5),  # C
        )

    if case_optimize_method is 'differential evolution':
        result = differential_evolution(fun, bounds, maxiter=10000, disp=True, strategy=methodName, init='random')

    if case_optimize_method is 'basinhopping':
        take_step = SESSA_Step()
        take_step.xmax = [x[1] for x in bounds]
        take_step.xmin = [x[0] for x in bounds]
        # # rewrite the bounds in the way required by L-BFGS-B
        # bounds = [(low, high) for low, high in zip(xmin, xmax)]

        # use method L-BFGS-B because the problem is smooth and bounded
        minimizer_kwargs = dict(method=minimizer_kwargs['method'], bounds=bounds)
        # res = basinhopping(f, x0, minimizer_kwargs=minimizer_kwargs)
        result = basinhopping(fun, x0, niter=200, take_step=take_step, minimizer_kwargs=minimizer_kwargs)
    if case_optimize_method is 'brute force':
        take_step = SESSA_Step()
        take_step.xmax = [x[1] for x in bounds]
        take_step.xmin = [x[0] for x in bounds]

        result = brute(fun, ranges=rranges, full_output=True, finish=None)


    print('-*'*25)
    print('==  Answer is:')
    print (result)
    print('-*'*25)
    # print('Answer is: x= {0:1.3f}, R= {1}'(result.x, result.fun))




if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    startCalculation()
