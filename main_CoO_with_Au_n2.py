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
from libs.functionsForMinimize import func_CoO_with_Au
from scipy.optimize import  differential_evolution
from scipy.optimize import basinhopping, brute
from scipy.optimize import minimize
from libs.dir_and_file_operations import create_out_data_folder
from libs.minimization_additions import SESSA_Step, BH_Bounds_for_SESSA
from libs.gensa import gensa

def startCalculation(projPath = r'/home/yugin/VirtualboxShare/Co-CoO/out_genetic_CoO_with_Au', case_mix_or_layers='layers'):
    # Finds the global minimum of a multivariate function. Differential Evolution is stochastic in nature
    # (does not use gradient methods) to find the minimium, and can search large areas of candidate space,
    # but often requires larger numbers of function evaluations than conventional gradient based techniques.

    # case_mix_or_layers = 'layers' # with separates CoO and Au
    # case_mix_or_layers = 'mix'  # with mix interlayer
    caseSet = {'layers', 'mix'}
    if case_mix_or_layers not in caseSet:
        print('case_mix_or_layers is not correct. Its should be mix/layers but not a -> {} <-'.format(case_mix_or_layers))
        sys.exit(0)
    else:


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

        if case_mix_or_layers == 'layers':
            newProjPath = create_out_data_folder(projPath,
                                                 first_part_of_folder_name=optimize_method + '_' + methodName + '_CoO_layers__R_' + case_R_factor)

            # ====================================================================================================
            # CoO and Au interlayer:
            def fun(x):

                y = np.zeros(11)
                #   Au        Co    CoOx     x   CoO   Au     MgO     MgCO3   MgOH    Au    C=O
                y = [200.000, x[0], 0.0001, 0.7,  x[1], x[2],  x[3],    x[4],  x[5],  0.0001, x[6]]

                return func_CoO_with_Au(y, projPath=newProjPath, case_R_factor=case_R_factor)

            # ====================================================================================================
            # # 1
            #                 Co    CoO   Au    MgO     MgCO3   MgOH    C=O
            # x0 = np.asarray([10,     3,  0.83,  8.7,     11.2,    5,     2.3])

            # R=0.3548
            x0 = np.array([14.699, 9.587, 23.132, 12.631, 10.032, 3.552, 1.353])

            # bounds = [
            #     (7, 25),  # Co
            #     (1, 7),  # CoO
            #     (1, 7),  # Au
            #     (5, 15),  # MgO
            #     (5, 15),  # MgCO3
            #     (0.001, 15),  # MgOH
            #     (0.001, 8),  # C
            #           ]

            bounds = [
                (9, 15),  # Co
                (6, 10),  # CoO
                (20, 25),  # MgO
                (9, 15),  # MgCO3
                (9, 15),  # Mg[OH]2
                (3, 4),  # Au
                (0.5, 2),  # C
            ]

            rranges = []
            # rranges = (
            #     slice(0.001, 8, 0.2),  # MgOH
            #     slice(5, 15, 0.2),  # MgCO3
            #     slice(5, 15, 0.2),  # MgO
            #     slice(1, 7, 0.2),  # Au
            #     slice(1, 7, 0.2),  # CoO
            #     slice(7, 25, 0.2),  # Co
            #     slice(0.001, 8, 0.2),  # C
            # )

        if case_mix_or_layers == 'mix':
            newProjPath = create_out_data_folder(projPath,
                                                 first_part_of_folder_name=optimize_method + '_' + methodName + '_CoO_mix__R_' + case_R_factor)

            # 2 for mix of CoO - Au
            def fun(x):
                y = np.zeros(11)
                #   Au        Co    CoOx     x   CoO    Au     MgO     MgCO3   MgOH    Au    C=O
                y = np.array(
                    [200.000, x[0], x[1],  x[2], 0.0001, 0.0001, x[3],    x[4],   x[5], 0.0001, x[6]])
                print('-------------------->>>> func(x)')
                print(y)
                print('--------------------<<<< func(x)')
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
                return func_CoO_with_Au(y, projPath=newProjPath, case_R_factor=case_R_factor)

            # ====================================================================================================


            # -> global minimum R-factor is: 0.7841880992402152
            # -> global minimum R-factor project folder: /home/yugin/VirtualboxShare/Co-CoO/out_genetic_CoO_with_Au/gensa__CoO_mix__R_all_lines_00001/00063
            #                 Co    CoOx     x       MgO     MgCO3   MgOH    C=O
            # x0 = np.asarray([ 16.5, 8.26, 0.75,      13.7,   9.2,     2,     2.3])

            # R=0.4531
            x0 = np.asarray([ 11.158, 8.349, 0.889,    5.04,   12.77,     0.562,     0.954])
            # ====================================================================================================
            # bounds = [
            #     (7, 25),  # Co
            #     (1, 15),  # h = CoOxAu_{1-x}
            #     (0.05, 0.95),  # x
            #     (5, 15),  # MgO
            #     (5, 15),  # MgCO3
            #     (0.001, 15),  # MgOH
            #     (0.001, 8),  # C
            #           ]

            bounds = [
                (10, 13),  # Co
                (6, 10),  # h = CoOxAu_{1-x}
                (0.05, 0.95),  # x
                (3, 7),  # MgO
                (10, 15),  # MgCO3
                (0.001, 2),  # MgOH
                (0.001, 2),  # C
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

        if case_optimize_method == 'differential evolution':
            result = differential_evolution(fun, bounds, maxiter=10000, disp=True, strategy=methodName, init='random')

        if case_optimize_method == 'gensa':
            print('=====  x0 is : {} '.format(x0))
            result = gensa(fun, x0, bounds, maxiter=500, initial_temp=5230., visit=2.62,
                            accept=-5.0, maxfun=1e7, args=(), seed=None, pure_sa=False)

        if case_optimize_method == 'basinhopping':
            take_step = SESSA_Step()
            take_step.xmax = [x[1] for x in bounds]
            take_step.xmin = [x[0] for x in bounds]
            # # rewrite the bounds in the way required by L-BFGS-B
            # bounds = [(low, high) for low, high in zip(xmin, xmax)]

            # use method L-BFGS-B because the problem is smooth and bounded
            minimizer_kwargs = dict(method=minimizer_kwargs['method'], bounds=bounds)
            # res = basinhopping(f, x0, minimizer_kwargs=minimizer_kwargs)
            print('=====  x0 is : {} '.format(x0))
            result = basinhopping(fun, x0, niter=200, take_step=take_step, minimizer_kwargs=minimizer_kwargs)
        if case_optimize_method == 'brute force':
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
    print('----- SYS.ARGV{}:')
    print(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            print('-- script run in debug mode:')
            if len(sys.argv) > 2:
                path = r'/home/yugin/VirtualboxShare/Co-CoO/debug/out_genetic_CoO_with_Au'
                startCalculation(projPath=path, case_mix_or_layers=sys.argv[2])
        else:
            startCalculation(case_mix_or_layers=sys.argv[1])
    else:
        print('Can not run')
        print(sys.argv)