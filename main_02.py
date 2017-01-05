'''
Create file with calculated errors for the ratio between max intensity or area of experimental and theoretical spectra
'''
import sys
import os
from io import StringIO
import numpy as np

# load the main Class:
from libs.load_and_compare_only_2_spectra import CompareTwoModels

# for parallel calculation:
import time
from joblib import Parallel, delayed
import multiprocessing

if __name__ == "__main__":
    print ('-> you run ',  __file__, ' file in a main mode' )
    # a = CompareTwoModels()
    # load experimental data:
    # a.loadExperimentalData()
    # a.loadSESSAspectra()
    # n01: Region of interest for calc STD and residual integral values
    # RIO_Si = [105, 96]
    # RIO_Nb = [200, 208]

    # n02:  a little bit closer region then n01
    # RIO_Si = [105, 97.5]
    # RIO_Nb = [201, 207]

    # n03:  measure only biggest peak:
    # RIO_Si = [98, 101]
    # RIO_Nb = [202, 204]

    # n04:  measure only 1/2 of the biggest peak:
    # RIO_Si = [99.3, 101]
    # RIO_Nb = [202.85, 204]
    RIO_Si = ([105, 96],  [105, 97.5], [98, 101], [99.3, 101])
    RIO_Nb = ([200, 208], [201, 207],  [202, 204], [202.85, 204])
    blur_or_sharp = ('blur', ) # 'sharp', 'as_is', 'blur'
    alpha = np.array((0.4, 0.5, 0.6))
    gamma = np.array((0.4, 0.5, 0.6))
    window_len = np.array((150, 200))

    window_name = ('lorentzian',)
    # window_name = ('gauss', 'voigt')
    # window_name = ('gauss', 'lorentzian', 'voigt')
    # the value which we want to parallelize:

    numOfElem = len(RIO_Si)*len(blur_or_sharp)*len(alpha)*len(gamma)*len(window_len)*len(window_name)
    print('Number of Cases for calculate is about {}'.format(numOfElem))
    argv = RIO_Nb
    if len(argv) > 0:
        num_cores = multiprocessing.cpu_count()
        if (len(argv) <= num_cores):
            print ('Program will be calculating on {} numbers of CPUs'.format(len(argv)) )
            time.sleep(1)
            print('Programm will calculate the next cases:\n{:}\n'.format(argv))
            for blr in blur_or_sharp:
                if blr in ('blur', 'sharp'):
                    print('->> ', blr)
                    for winName in window_name:
                        for winLen in window_len:
                            if winName in ('voigt'):
                                print('->> ', winName)
                                for alf in alpha:
                                    for gam in gamma:
                                        def tmpFun(index):
                                            a = CompareTwoModels()
                                            a.RIO_Nb = RIO_Nb[index]
                                            a.RIO_Si = RIO_Si[index]
                                            a.blur_or_sharp = blr
                                            a.window_name = winName
                                            a.window_len = winLen
                                            a.alpha = alf
                                            a.gamma = gam
                                            a.loadSESSAspectra()

                                        Parallel(n_jobs=len(argv))( delayed(tmpFun)(i) for i in range(len(argv)) )
                            if winName in ('gauss'):
                                print('->> ', winName)
                                for alf in alpha:
                                    def tmpFun(index):
                                        a = CompareTwoModels()
                                        a.RIO_Nb = RIO_Nb[index]
                                        a.RIO_Si = RIO_Si[index]
                                        a.blur_or_sharp = blr
                                        a.window_name = winName
                                        a.window_len = winLen
                                        a.alpha = alf
                                        a.loadSESSAspectra()

                                    Parallel(n_jobs=len(argv))( delayed(tmpFun)(i) for i in range(len(argv)) )

                            if winName in ('lorentzian'):
                                print('->> ', winName)
                                for gam in gamma:
                                    def tmpFun(index):
                                        a = CompareTwoModels()
                                        a.RIO_Nb = RIO_Nb[index]
                                        a.RIO_Si = RIO_Si[index]
                                        a.blur_or_sharp = blr
                                        a.window_name = winName
                                        a.window_len = winLen
                                        a.gamma = gam
                                        a.loadSESSAspectra()

                                    Parallel(n_jobs=len(argv))( delayed(tmpFun)(i) for i in range(len(argv)) )

                else: # for as_is case:
                    print('->> ', blr)
                    def tmpFun(index):
                        a = CompareTwoModels()
                        a.RIO_Nb = RIO_Nb[index]
                        a.RIO_Si = RIO_Si[index]
                        a.blur_or_sharp = blr
                        a.loadSESSAspectra()

                    Parallel(n_jobs=len(argv))( delayed(tmpFun)(i) for i in range(len(argv)) )

        else:
            print('PC doesn''t have this numbers of needed CPUs for parallel calculation' )


    else:
        print('- > No selected case was found.')

    # Command for terminal to recursively find files in subdirectories and then copy to target directory:
    # find ./ -name 'result_*.png' -exec cp {} /home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/Version_45-deg_v03_001/result_images  \;

# You can also use awk for these purposes, since it allows you to perform more complex checks in a clearer way:
#
# Lines not containing foo:
#
# awk '!/foo/'
#
# Lines not containing neither foo nor bar:
#
# awk '!/foo/ && !/bar/'
#
# Lines not containing neither foo nor bar but containing either foo2 or bar2:
#
# awk '!/foo/ && !/bar/ && (/foo2/ || /bar2/)'
