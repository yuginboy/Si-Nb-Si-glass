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
from libs.dir_and_file_operations import listdirs, listdirsFN, get_upper_folder_name, get_folder_name, createFolder
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
import progressbar #progressbar2
import tkinter as tk
from tkinter import filedialog
import pickle
def saveDataToColumnTxt(dataPath='~', fname='Au4f-60', xDataBE=0, xDataKE=0, yDataExperiment=0, yDataTheory=0):
    headerTxt = 'Binding Energy [eV]\tKinetic Energy [eV]\tExperiment [a.u.]\tTheory [a.u.]'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d__%H_%M_%S")
    outArr = np.zeros((len(xDataBE), 4))
    outArr[:, 0] =  xDataBE
    outArr[:, 1] =  xDataKE
    outArr[:, 2] =  yDataExperiment
    outArr[:, 3] =  yDataTheory
    np.savetxt(os.path.join(dataPath, fname + timestamp + '.txt'), outArr,
               fmt='%1.6e', delimiter='\t', header=headerTxt)
def main(dataPath = r'/home/yugin/VirtualboxShare/Co-CoO/test', saveFigs=True, showFigs=True, sample_case='with_Au'):
    # load SESSA calculated spectra:
    # dirPathList = listdirs(dataPath)
    # sample_case='no_Au'/'with_Au'
    dirFullPathList = sorted(listdirsFN(dataPath))
    time.sleep(1)
    arrR_factor = np.zeros((len(dirFullPathList), 10))
    i = 0
    bar = progressbar.ProgressBar(maxval = len(dirFullPathList),\
                                   widgets = [progressbar.Bar('=', '[', ']'), ' ',
                                              progressbar.Percentage()])
    for currentPath in dirFullPathList:
        if sample_case == 'no_Au':
            from libs.sample_CoO_no_Au_classes import Class_CoO_no_Au
            data = Class_CoO_no_Au()

        elif sample_case == 'with_Au':
            from libs.sample_CoO_with_Au_classes import Class_CoO_with_Au
            data = Class_CoO_with_Au()



        pcklFile = os.path.join(currentPath, 'objs.pickle')
        with open(pcklFile, 'rb') as f:
            obj = pickle.load(f)
        print(obj[0].tabledLayersStructureInfo)

        # a = NumericData()
        data.a.theoryDataPath = currentPath

        data.a.loadExperimentData()
        data.a.loadTheoryData()
        data.setPeakRegions()
        data.applyGlobalIntensityNormalization()
        data.a.showFigs = showFigs
        data.a.setupAxes()
        data.a.updatePlot(saveFigs=saveFigs)




        arrR_factor[i, 0] = i+1

        arrR_factor[i, 1] = data.a.Au4f._0.R_factor
        arrR_factor[i, 2] = data.a.Au4f._60.R_factor

        arrR_factor[i, 3] = data.a.Co2p._0.R_factor
        arrR_factor[i, 4] = data.a.Co2p._60.R_factor

        arrR_factor[i, 5] = data.a.O1s._0.R_factor
        arrR_factor[i, 6] = data.a.O1s._60.R_factor

        arrR_factor[i, 7] = data.a.Mg1s._0.R_factor
        arrR_factor[i, 8] = data.a.Mg1s._60.R_factor

        arrR_factor[i, 9] = data.a.total_R_faktor

        structToOut = data.a.Au4f._0
        saveDataToColumnTxt(dataPath=createFolder(os.path.join(currentPath, 'out_coldata')),
                            fname='Au4f-00', xDataBE=structToOut.experiment.data.fit.bindingEnergy,
                            xDataKE=structToOut.experiment.data.fit.kineticEnergy,
                            yDataExperiment=structToOut.experiment.data.fit.intensity,
                            yDataTheory=structToOut.theory.data.fit.intensity,
                            )

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
    file_path = filedialog.askdirectory(initialdir=os.path.join(os.path.expanduser('~'), r'VirtualboxShare/Co-CoO/results/introductory/'))
    if len(file_path) > 0:
        print('-> you are working in directory: ', file_path)
        main(dataPath = file_path, saveFigs=False, showFigs=True)
