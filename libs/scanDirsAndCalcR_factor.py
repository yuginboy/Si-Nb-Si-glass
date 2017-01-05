'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-12-28
'''
import os
import datetime
import time
import numpy as np
from libs.dataProperties import NumericData
from libs.dir_and_file_operations import listdirs, listdirsFN
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
import progressbar #progressbar2
import tkinter as tk
from tkinter import filedialog

def main(dataPath = r'/home/yugin/VirtualboxShare/Co-CoO/test', saveFigs=True, showFigs=True):
    # load SESSA calculated spectra:
    # dirPathList = listdirs(dataPath)
    dirFullPathList = sorted(listdirsFN(dataPath))
    time.sleep(60)
    arrR_factor = np.zeros((len(dirFullPathList), 10))
    i = 0
    bar = progressbar.ProgressBar(maxval = len(dirFullPathList),\
                                   widgets = [progressbar.Bar('=', '[', ']'), ' ',
                                              progressbar.Percentage()])
    for currentPath in dirFullPathList:
        a = NumericData()
        a.theoryDataPath = currentPath
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


        a.showFigs = showFigs
        a.setupAxes()
        a.updatePlot(saveFigs=saveFigs)

        arrR_factor[i, 0] = i+1

        arrR_factor[i, 1] = a.Au4f._0.R_factor
        arrR_factor[i, 2] = a.Au4f._60.R_factor

        arrR_factor[i, 3] = a.Co2p._0.R_factor
        arrR_factor[i, 4] = a.Co2p._60.R_factor

        arrR_factor[i, 5] = a.O1s._0.R_factor
        arrR_factor[i, 6] = a.O1s._60.R_factor

        arrR_factor[i, 7] = a.Mg1s._0.R_factor
        arrR_factor[i, 8] = a.Mg1s._60.R_factor

        arrR_factor[i, 9] = a.total_R_faktor
        i = i + 1
        bar.update(i)

    bar.finish()
    headerTxt = 'case\tAu4f._0\tAu4f._60\tCo2p._0\tCo2p._60\tO1s._0\tO1s._60\tMg1s._0\tMg1s._60\ttotal.R_factor'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d__%H_%M_%S")

    np.savetxt(os.path.join(dataPath, 'R-factor_' + timestamp + '.txt'), arrR_factor,
               fmt='%1.6e', delimiter='\t', header=headerTxt)

    # create figure with axes:

    pylab.ion()  # Force interactive
    plt.close('all')

    fig = plt.figure()
    figManager = plt.get_current_fig_manager()
    DPI = fig.get_dpi()
    fig.set_size_inches(800.0 / DPI, 600.0 / DPI)

    gs = gridspec.GridSpec(1, 1)

    fig.clf()
    axes = fig.add_subplot(gs[0, 0])
    axes.set_title('$R_{factor}$')
    axes.grid(True)
    axes.set_ylabel('$R_{factor}$', fontsize=16, fontweight='bold')
    axes.set_xlabel('case number', fontsize=16, fontweight='bold')
    # Change the axes border width
    for axis in ['top', 'bottom', 'left', 'right']:
        axes.spines[axis].set_linewidth(2)

    fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

    figManager.window.setGeometry(1920, 20, 1920, 1180)
    plt.show()
    figManager.window.setWindowTitle('CoO fitting')
    fig.suptitle('', fontsize=22, fontweight='normal')
    axes.plot(arrR_factor[:,0], arrR_factor[:,1], '-', label=('Au4f $\\alpha=0^O$'),  linewidth=2.5, alpha=0.5)
    axes.plot(arrR_factor[:,0], arrR_factor[:,2], '-', label=('Au4f $\\alpha=60^O$'),  linewidth=2.5, alpha=0.5)
    axes.plot(arrR_factor[:,0], arrR_factor[:,3], '-', label=('Co2p $\\alpha=0^O$'),  linewidth=2.5, alpha=0.5)
    axes.plot(arrR_factor[:,0], arrR_factor[:,4], '-', label=('Co2p $\\alpha=60^O$'),  linewidth=2.5, alpha=0.5)
    axes.plot(arrR_factor[:,0], arrR_factor[:,5], '-', label=('O1s $\\alpha=0^O$'),  linewidth=2.5, alpha=0.5)
    axes.plot(arrR_factor[:,0], arrR_factor[:,6], '-', label=('O1s $\\alpha=60^O$'),  linewidth=2.5, alpha=0.5)
    axes.plot(arrR_factor[:,0], arrR_factor[:,7], '--', label=('Mg1s $\\alpha=0^O$'),  linewidth=2.5, alpha=0.5)
    axes.plot(arrR_factor[:,0], arrR_factor[:,8], '--', label=('Mg1s $\\alpha=60^O$'),  linewidth=2.5, alpha=0.5)
    axes.plot(arrR_factor[:,0], arrR_factor[:,9], '-', label=('total R'),  linewidth=5, alpha=0.5)

    axes.legend(shadow=True, fancybox=True, loc='best')
    # save to the PNG file:
    fig.savefig(os.path.join(dataPath, 'R-factor_' + timestamp + '.png'))

    print('-> main worked in {0} directory and has been finished'.format(dataPath))
if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    #openfile dialoge
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(initialdir=r'/home/yugin/VirtualboxShare/Co-CoO/')
    if len(file_path) > 0:
        print('-> you are working in directory: ', file_path)
        main(dataPath = file_path, saveFigs=False, showFigs=False)
