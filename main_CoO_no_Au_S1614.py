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
from libs.functionsForMinimize import func_CoO_no_Au
from scipy.optimize import  differential_evolution
from scipy.optimize import basinhopping, brute
from scipy.optimize import minimize
from libs.dir_and_file_operations import create_out_data_folder
from libs.minimization_additions import SESSA_Step
from libs.gensa import gensa

def startCalculation(projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out_genetic_CoO_no_Au'):
    # Finds the global minimum of a multivariate function. Differential Evolution is stochastic in nature
    # (does not use gradient methods) to find the minimium, and can search large areas of candidate space,
    # but often requires larger numbers of function evaluations than conventional gradient based techniques.

    case_mix_or_layers = 'layers' # with separates CoO and Au
    # at 2017-01-18 mix mode was not exist for case: CoO_no_Au
    # case_mix_or_layers = 'mix'  # with mix interlayer

    # case_R_factor = 'without_Co_and_Au'
    # case_R_factor = 'without_O_and_Mg'
    case_R_factor = 'all_lines'

    # case_optimize_method = 'differential evolution'
    # case_optimize_method = 'basinhopping'
    # Find the global minimum of a function using the Generalized Simulated Annealing algorithm:
    case_optimize_method = 'gensa'
    # case_optimize_method = 'brute force'

    # timestamp = datetime.datetime.now().strftime("_[%Y-%m-%d_%H_%M_%S]_")
    # methodName = 'Nelder-Mead'
    methodName = 'randtobest1exp'
    minimizer_kwargs = {"method": "L-BFGS-B", "jac": False}
    # methodName = 'rand1exp'
    # methodName = 'BFGS'

    if case_optimize_method is 'differential evolution':
        optimize_method = 'de'
    if case_optimize_method is 'gensa':
        optimize_method = 'gensa'
        methodName = ''
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
            # x = [200.000, 10.000, 8.0, 0.001, 40.000, 5.000, 5.000, 3.0, 5.000]
            y = np.zeros(9)
            #     Au      Co     CoO   Au     MgO   MgCO3   MgOH    Au    C=O
            y = [200.000, x[0],  x[1], 0.0001, x[2], x[3],   x[4],  x[5], x[6]]
            # # fix Au=200A thickness:
            # y[0] = 200
            # # fix Au interlayer thickness:
            # y[3] = 0.001
            #
            # y[1] = x[0]
            # y[2] = x[1]
            #
            # y[4] = x[2]
            # y[5] = x[3]
            # y[6] = x[4]
            # y[7] = x[5]
            # y[8] = x[6]
            return func_CoO_no_Au(y, projPath=newProjPath, case_R_factor=case_R_factor)

        # ====================================================================================================
        # # 1
        bounds = [
                  (3, 15),  # Co
                  (1, 10),  # CoO
                  (10, 45),  # MgO
                  (1, 20),  # MgCO3
                  (1, 20),  # Mg[OH]2
                  (0.3, 5),  # Au
                  (0.3, 6),  # C
                  ]
        x0 = [10.000, 8.0, 40.000, 5.000, 5.000, 3.0, 5.000]

        # rranges = (
        #     slice(0.001, 8, 0.2),  # MgOH
        #     slice(5, 15, 0.2),  # MgCO3
        #     slice(5, 15, 0.2),  # MgO
        #     slice(1, 7, 0.2),  # Au
        #     slice(1, 7, 0.2),  # CoO
        #     slice(7, 25, 0.2),  # Co
        #     slice(0.001, 8, 0.2),  # C
        # )
        rranges = []

    if case_optimize_method is 'differential evolution':
        result = differential_evolution(fun, bounds, disp=True, polish=False,
                                        mutation=(0.5, 1.3), recombination=0.8, seed=None,
                                        maxiter=3000, popsize=23, tol=0.01,
                                        )

    if case_optimize_method is 'gensa':
        result = gensa(fun, x0, bounds, maxiter=500, initial_temp=5230., visit=2.62,
                        accept=-5.0, maxfun=1e7, args=(), seed=None, pure_sa=False)

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
