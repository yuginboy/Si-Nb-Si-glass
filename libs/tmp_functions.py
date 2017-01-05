"Main file for run this package"
import pandas as pd
import sys
import os
from io import StringIO
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
import scipy as sp
from scipy.interpolate import interp1d
import re
from libs.backgrounds import shirley_base, shirley_new
from libs.estimations import std_residual, y_in_region, get_integral_in_region
from libs.filtering import smooth_by_window

# for parallel calculation:
import time
from joblib import Parallel, delayed
import multiprocessing

def listdirs(folder):
    '''
    return only the names of the subdirectories
    :param folder:
    :return:
    '''
    '''
    :param folder:
    :return:
    '''
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

def listdirsFN(folder):
    '''
    Return list of full pathname subdirectories
    '''
    return [
        d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder))
        if os.path.isdir(d)
    ]


def defLabelFromFileName(txt):
    if '00' in txt:
        return '0 min'
    if '08' in txt:
        return '8 min'
    if '14' in txt:
        return '14 min'
    if '17' in txt:
        return '17 min'
    if '24' in txt:
        return '24 min'


def importExperimentDataNb(dataPath):
    # Import Si2p and Nb3d spectra from 2 files in experiment subfolder
    """

    """
    for file in os.listdir(os.path.join(dataPath, 'experiment')):
        if file.endswith(".dat"):
            if 'Nb' in file:
                # print('Nb:', os.path.join(dataPath, file))
                Nbexp = pd.read_csv(os.path.join(dataPath, 'experiment', file), comment='#', delimiter='\t')

    return Nbexp

def importExperimentDataSi(dataPath):
    # Import Si2p and Nb3d spectra from 2 files in experiment subfolder
    """

    """
    for file in os.listdir(os.path.join(dataPath, 'experiment')):
        if file.endswith(".dat"):

            if 'Si' in file:
                # print('Si:', os.path.join(dataPath, file))
                Siexp = pd.read_csv(os.path.join(dataPath, 'experiment', file), comment='#', delimiter='\t')

    return Siexp

def bg_substraction(x,y):
    return y-shirley_new(x,y)

def createFolder (folder_name):
    '''
    check for exist and if it is then create folder_name
    :param folder_name: full folder path name
    :return: folder_name of created directory
    '''
    if  not (os.path.isdir(folder_name)):
        os.mkdir(folder_name, exist_ok=True)
    return folder_name

def create_out_data_folder(main_folder_path):
    '''
    create out data directory like 0005 or 0004
    :param main_folder_path: path to the main project folder
    :return: full path to the new directory
    '''
    checkFile = 1
    i = 1
    while checkFile > 0:

        out_data_folder_path = os.path.join( main_folder_path, '%04d' % i )
        if  not (os.path.isdir(out_data_folder_path)):
            checkFile = 0
            os.makedirs(out_data_folder_path, exist_ok=True)
        i+=1
    return  out_data_folder_path

# d = np.array()

def main_func_to_run(dataPath = '/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/Version_45-deg_v03_001',
                     RIO_Si = [105, 96], RIO_Nb = [200, 208], blur_or_sharp = 'as_is', alpha=0.5, gamma = 0.5,
                     window_len = 200, window_name = 'gauss'):
    '''
        Function calculate spectra, trying to fit it and plot graphs for 2 region Si2p and Nb3d
    :param dataPath: name of the SESSA calculated data folder
    :param RIO_Si: region of interest for calculation integral residuals value for Si
    :param RIO_Nb: region of interest for calculation integral residuals value for Nb
    :param blur_or_sharp: the one from these values: 'blur', 'sharp', 'as_is'
    :param alpha: for gauss and voigt windows
    :param gamma: for larentzian and voigt windows
    :param window_len: length in numbers of points
    :param window_name: 'gauss', 'lorentzian', 'voigt'
    :return:
    '''
    # Import src data from files:
    Nbexp = importExperimentDataNb(dataPath)
    Siexp = importExperimentDataSi(dataPath)

    srcNb = np.zeros((len(Nbexp['BE (eV)']), 6))
    srcNb[:, 0 ]= Nbexp['BE (eV)'].values
    srcNb[:, 1] = Nbexp['0 min'].values
    srcNb[:, 2] = Nbexp['8 min'].values
    srcNb[:, 3] = Nbexp['14 min'].values
    srcNb[:, 4] = Nbexp['17 min'].values
    srcNb[:, 5] = Nbexp['24 min'].values

    srcSi = np.zeros((len(Siexp['BE (eV)']), 6))
    srcSi[:, 0] = Siexp['BE (eV)'].values
    srcSi[:, 1] = Siexp['0 min'].values
    srcSi[:, 2] = Siexp['8 min'].values
    srcSi[:, 3] = Siexp['14 min'].values
    srcSi[:, 4] = Siexp['17 min'].values
    srcSi[:, 5] = Siexp['24 min'].values

    for i in range(1,6):
        srcNb[:, i] = bg_substraction(srcNb[:, 0],srcNb[:, i])
        srcSi[:, i] = bg_substraction(srcSi[:, 0],srcSi[:, i])


    dirPathList = listdirs(dataPath)
    dirFullPathList = listdirsFN(dataPath)

    # Create new list only with elements which contains substring 'out'
    d = [i for i in dirPathList if 'out_' in i ]

    # folderName = '/home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/Version_45-deg_v03_001/out_Si0.01Ni0.99'
    Nbcalc = np.zeros((2048, 5, len(d)))
    Sicalc = np.zeros((2048, 5, len(d)))
    srcValuesFromExperiment_Nb  = np.zeros((2048, 5, len(d)))
    srcValuesFromExperiment_Si  = np.zeros((2048, 5, len(d)))
    nSiNb = np.zeros((len(d),2))

    graphLabelName = []

    i = 0
    j = 0
    for folderName in dirPathList:
        # check the 'out_' folders only
        if 'out_' in folderName:
            concentration = re.findall("\d+\.\d+", folderName)
            nSiNb[j, 0] = concentration[0] #Si
            nSiNb[j, 1] = concentration[1] #Nb
            folderFullName = os.path.join(dataPath,folderName)
            for file in os.listdir(folderFullName):
                if file.endswith(".dat"):
                    if 'Si' in file:
                        # print('Si:', os.path.join(folderFullName, file))
                        data = pd.read_csv(os.path.join(folderFullName, file), comment='#', header=None, delimiter='\t',
                                           names=('Energy', 'Intensity', 'NaN'))
                        data['Energy'] = 1486.6 - data['Energy']
                        Six = data['Energy'].values
                        Sicalc[:,i,j] = data['Intensity'].values

                    if 'Nb' in file:
                        # print('Nb:', os.path.join(folderFullName, file))
                        data = pd.read_csv(os.path.join(folderFullName, file), comment='#', header=None, delimiter='\t',
                                           names=('Energy', 'Intensity', 'NaN'))
                        data['Energy'] = 1486.6 - data['Energy']
                        Nbx = data['Energy'].values
                        Nbcalc[:, i, j] = data['Intensity'].values
                        graphLabelName.append(defLabelFromFileName(file))

                        i+=1

                # Nbcalc[:,i,j]=Nby
                # Sicalc[:,i,j]=Siy

            j += 1
            i = 0

    # interpolate data for Experimental data points
    interpSi = np.zeros((len(Six), 5))
    interpNb = np.zeros((len(Nbx), 5))

    for i in range(5):
        f = interp1d(srcSi[:, 0], srcSi[:, i+1])
        interpSi[:, i] = f(Six)
        f = interp1d(srcNb[:, 0], srcNb[:, i+1])
        interpNb[:, i] = f(Nbx)


    # Normalize the data
    maxVal = interpNb.max()
    interpNb = interpNb/maxVal

    maxVal = interpSi.max()
    interpSi = interpSi/maxVal

    # calculate BE shift between experiment and calculation
    calcBE = Six[Sicalc[:,0,0].argmax()]
    expBE = Six[interpSi[:,0].argmax()]
    deltaBE = expBE - calcBE - 0.1

    SiXexp = Six - deltaBE
    NbXexp = Nbx - deltaBE

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

    # Select only a top peaks area
    # RIO_Si = [99.4, 99.2]
    # RIO_Nb = [202.8, 202.9]


    pylab.ion()  # Force interactive
    plt.close('all')
    ### for 'Qt4Agg' backend maximize figure
    plt.switch_backend('QT4Agg')

    fig = plt.figure()
    # gs1 = gridspec.GridSpec(1, 2)
    fig.show()
    # fig.set_tight_layout(True)
    figManager = plt.get_current_fig_manager()
    DPI = fig.get_dpi()
    fig.set_size_inches(1920.0 / DPI, 1080.0 / DPI, dpi=DPI)

    gs = gridspec.GridSpec(3,2)

    axesNb = fig.add_subplot(gs[:-1,0])
    axesNb.invert_xaxis()
    axesNb.set_title('Nb')
    axesSi = fig.add_subplot(gs[:-1,1])
    axesSi.invert_xaxis()
    axesSi.set_title('Si')

    # for concentration and std
    axesNb_std = fig.add_subplot(gs[2,0])
    axesNb_std.set_title('std(Nb)')
    axesSi_std = fig.add_subplot(gs[2,1])
    axesSi_std.set_title('std(Si)')
    # Change the axes border width
    for axis in ['top','bottom','left','right']:
      axesSi.spines[axis].set_linewidth(2)
      axesNb.spines[axis].set_linewidth(2)
    # plt.subplots_adjust(top=0.85)
    # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
    fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

    # put window to the second monitor
    # figManager.window.setGeometry(1923, 23, 640, 529)
    figManager.window.setGeometry(1920, 20, 1920, 1180)

    plt.show()


    colorsForGraph = ['peru','dodgerblue','brown','red', 'darkviolet']

    # normalize to Intensity eq y=1:
    for i in range(len(d)):
        maxVal = Nbcalc[:,:,i].max()

        Nbcalc[:,:,i] = Nbcalc[:,:,i]/maxVal

        maxVal = Sicalc[:,:,i].max()
        Sicalc[:,:,i] = Sicalc[:,:,i]/maxVal

    # blur the spectra:
    # blur_or_sharp = 'as_is' # blur, sharp, as_is
    # alpha=0.5
    # gamma = 0.5
    # window_len = 200
    # window_name = 'gauss' # 'gauss', 'lorentzian', 'voigt'
    # Remember all calculation values as is before filtering for subsequent comparing:
    srcValuesFromExperiment_Si [:, :, :] = Sicalc [:, :, :]
    srcValuesFromExperiment_Nb [:, :, :] = Nbcalc [:, :, :]

    # apply filter to the spectra:
    for j in range(len(d)):
        for i in range(5):
            if blur_or_sharp in ['blur', 'sharp']:
                Nbcalc[:, i, j] = smooth_by_window (Nbcalc[:, i, j], window_len=window_len, window = window_name, alpha=alpha, gamma = gamma, blur_or_sharp= blur_or_sharp)
                Nbcalc[:, i, j] = y_in_region (Nbx, Nbcalc[:, i, j], region=RIO_Nb)

                Sicalc[:, i, j] = smooth_by_window (Sicalc[:, i, j], window_len=window_len, window = window_name, alpha=alpha, gamma = gamma, blur_or_sharp= blur_or_sharp)
                Sicalc[:, i, j] = y_in_region (Six, Sicalc[:, i, j], region=RIO_Si)

            else:
                Nbcalc[:, i, j] = y_in_region(Nbx, Nbcalc[:, i, j], region=RIO_Nb)
                Sicalc[:, i, j] = y_in_region(Six, Sicalc[:, i, j], region=RIO_Si)

    # create OUT data folder:
    ROI_txt = 'Si=[{},{}]_Nb=[{},{}]_'.format(RIO_Si[0], RIO_Si[1], RIO_Nb[0], RIO_Nb[1])
    if blur_or_sharp in ['blur', 'sharp']:
        if window_name in 'gauss':
            values_of_current_project = ROI_txt + blur_or_sharp + "_{}_alpha={}_window_len={}".format(window_name,alpha,window_len)
        if window_name in 'lorentzian':
            values_of_current_project = ROI_txt + blur_or_sharp + "_{}_gamma={}_window_len={}".format(window_name,gamma,window_len)
        if window_name in 'voigt':
            values_of_current_project = ROI_txt + blur_or_sharp + "_{}_alpha={}_gamma={}_window_len={}".format(window_name,alpha,gamma,window_len)
    else:
         values_of_current_project = ROI_txt + blur_or_sharp
    # create a base out subdirectory with name 'calc':
    baseOutDir = createFolder( os.path.join((dataPath), 'calc') )
    # create unique name for calculated data cases:
    name_of_out_folder = 'calc_' + values_of_current_project
    # create 0001-type of subdirectory inside unique subdirectory:
    out_dir = create_out_data_folder( os.path.join(baseOutDir, name_of_out_folder) )


    # test calculation spectra after filtering:
    for j in range(len(d)):
        axesNb.cla()
        axesSi.cla()
        for i in range(5):
            axesNb.plot(Nbx, srcValuesFromExperiment_Nb[:, i, j], '--', label=(graphLabelName[i] + ' src'), color = colorsForGraph[i], linewidth=2.5)
            axesSi.plot(Six, srcValuesFromExperiment_Si[:, i, j], '--', label=(graphLabelName[i] + ' src'), color = colorsForGraph[i], linewidth=2.5)
            axesNb.plot(Nbx, Nbcalc[:, i, j], label = (graphLabelName[i] + ' ' + blur_or_sharp), color = colorsForGraph[i])
            axesSi.plot(Six, Sicalc[:, i, j], label = (graphLabelName[i] + ' ' + blur_or_sharp), color = colorsForGraph[i])
            axesNb.legend(shadow=True, fancybox=True, loc='upper left')
            axesSi.legend(shadow=True, fancybox=True, loc='upper left')
            plt.draw()
        fig.suptitle('The mix ratio now is: $Si_{{{0}}}Nb_{{{1}}}$\n{2}'.format(nSiNb[j,0], nSiNb[j,1], values_of_current_project).replace('_',' ').
                 replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur',', blur,'), fontsize=22)
        # save to the PNG file:
        out_file_name = "src_vs_filtered__Si_%05.2f--Nb_%05.2f.png" %(nSiNb[j,0], nSiNb[j,1])
        fig.savefig( os.path.join(out_dir, out_file_name) )

    print('-- > Images with a comparison of calculated src spectra and calculated src spectra after filtering was saved')

    # normalize filtered spectra:
    for i in range(len(d)):
        maxVal = Nbcalc[:,:,i].max()

        Nbcalc[:,:,i] = Nbcalc[:,:,i]/maxVal

        maxVal = Sicalc[:,:,i].max()
        Sicalc[:,:,i] = Sicalc[:,:,i]/maxVal

    # test again for normalizing calculation spectra after filtering:
    for j in range(len(d)):
        axesNb.cla()
        axesSi.cla()
        for i in range(5):
            # plot source calculated data:
            axesNb.plot(Nbx, srcValuesFromExperiment_Nb[:, i, j], '--', label=(graphLabelName[i] + ' src'), color = colorsForGraph[i], linewidth=2.5)
            axesSi.plot(Six, srcValuesFromExperiment_Si[:, i, j], '--', label=(graphLabelName[i] + ' src'), color = colorsForGraph[i], linewidth=2.5)

            # plot filtered calculated data:
            axesNb.plot(Nbx, Nbcalc[:, i, j], label = (graphLabelName[i] + ' ' + blur_or_sharp), color = colorsForGraph[i])
            axesSi.plot(Six, Sicalc[:, i, j], label = (graphLabelName[i] + ' ' + blur_or_sharp), color = colorsForGraph[i])

            # plot interpolated experimental data
            axesNb.plot(NbXexp, interpNb[:,i], '-', label=(graphLabelName[i] + ' exp'), color = colorsForGraph[i], linewidth=5, alpha = 0.5)
            axesSi.plot(SiXexp, interpSi[:,i], '-', label=(graphLabelName[i] + ' exp'), color = colorsForGraph[i], linewidth=5, alpha = 0.5)

            # # fill integrated area of interpolated experimental data
            axesNb.fill_between(NbXexp, y_in_region(NbXexp, interpNb[:, i], RIO_Nb), interpolate=True, color = colorsForGraph[i], alpha = 0.1)
            axesSi.fill_between(SiXexp, y_in_region(SiXexp, interpSi[:, i], RIO_Si), interpolate=True, color = colorsForGraph[i], alpha = 0.1)

            # fill integrated area of filtered calculated data
            axesNb.fill_between(Nbx, y_in_region(Nbx, Nbcalc[:, i, j], RIO_Nb), interpolate=True, color = colorsForGraph[i], alpha = 0.1)
            axesSi.fill_between(Six, y_in_region(Six, Sicalc[:, i, j], RIO_Si), interpolate=True, color = colorsForGraph[i], alpha = 0.1)

            axesNb.legend(shadow=True, fancybox=True, loc='upper left')
            axesSi.legend(shadow=True, fancybox=True, loc='upper left')
            plt.draw()
        fig.suptitle('The mix ratio now is: $Si_{{{0}}}Nb_{{{1}}}$\n{2}'.format(nSiNb[j,0], nSiNb[j,1], values_of_current_project).replace('_',' ').
                 replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur',', blur,'), fontsize=22)
        # save to the PNG file:
        out_file_name = "norm(src_vs_filtered)__Si_%05.2f--Nb_%05.2f.png" %(nSiNb[j,0], nSiNb[j,1])
        fig.savefig( os.path.join(out_dir, out_file_name) )

    print('-- > Images with a comparison of calculated src spectra, normalized calculated spectra after filtering and raw experimental spectra was saved')

    # (xA, yA, xB, yB, region=None)
    # print(std_residual(SiXexp, interpSi, Six, Sicalc[:,:, 1]))
    # print(std_residual(SiXexp, interpSi, Six, Sicalc[:,:, 1], RIO_Si))
    # print(std_residual(NbXexp, interpNb, Nbx, Nbcalc[:,:, 1], RIO_Nb))



    stdSi = np.zeros((len(d),1))
    stdNb = np.zeros((len(d),1))
    for j in range(len(d)):
        axesNb.cla()
        axesSi.cla()
        axesNb_std.cla()
        axesSi_std.cla()
        for i in range(5):
            # labelName =
            # plot experimental values:
            axesNb.plot(NbXexp, interpNb[:,i], '-', label=(graphLabelName[i] + ' exp'), color = colorsForGraph[i], linewidth=5, alpha = 0.5)
            # check the RIO_Nb:
            # axesNb.plot(NbXexp, y_in_region(NbXexp,interpNb[:,i],RIO_Nb), '-', label=(graphLabelName[i] + ' exp'), color = colorsForGraph[i], linewidth=5, alpha = 0.5)

            axesSi.plot(SiXexp, interpSi[:,i], '-', label=(graphLabelName[i] + ' exp'), color = colorsForGraph[i], linewidth=5, alpha = 0.5)
            # check the RIO_Si:
            # axesSi.plot(SiXexp,y_in_region(SiXexp, interpSi[:,i],RIO_Si), '-', label=(graphLabelName[i] + ' exp'), color = colorsForGraph[i], linewidth=5, alpha = 0.5)

            # axesNb.plot(Nbx, shirley_base(Nbx, interpNb[:,i]), label=graphLabelName[i])
            # axesNb.plot(Nbx, shirley_new(Nbx, interpNb[:,i], numpoints=100), label=graphLabelName[i])

            # plot calculated values:
            axesNb.plot(Nbx, Nbcalc[:,i,j], label=graphLabelName[i], color = colorsForGraph[i])
            axesSi.plot(Six, Sicalc[:,i,j], label=graphLabelName[i], color = colorsForGraph[i])

            plt.draw()
        # txtMix =  'The mix ratio now is: $Si_{%d}Nb_{%d}$' % (nSiNb[j,0], nSiNb[j,1])
        # stdSi[j] = (std_residual(SiXexp,interpSi,Six,Sicalc[:,:,j],RIO_Si))
        # stdNb[j] = (std_residual(NbXexp,interpNb,Nbx,Nbcalc[:,:,j],RIO_Nb))

         # Calculate integrals, take subtraction between modules and then take a sum:
         #    dd = np.abs( get_integral_in_region(SiXexp,interpSi[:,3],RIO_Si) )
         #    dd = np.abs( get_integral_in_region(SiXexp,interpSi[:,3],RIO_Si) )
        stdSi[j] = np.abs(   np.abs( get_integral_in_region(SiXexp, interpSi, RIO_Si) ) - np.abs( get_integral_in_region(Six, Sicalc[:, :, j], RIO_Si) )   ).sum()
        stdNb[j] = np.abs(   np.abs( get_integral_in_region(NbXexp, interpNb, RIO_Nb) ) - np.abs( get_integral_in_region(Nbx, Nbcalc[:, :, j], RIO_Nb) )   ).sum()

        axesSi_std.plot(nSiNb[0:j+1,0], stdSi[0:j+1], 'o', color='b')
        axesSi_std.plot(nSiNb[j,0], stdSi[j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None',
                        markeredgewidth=3)
        axesSi_std.grid(True)
        axesSi_std.set_xlabel('part of Si', fontsize=14, fontweight='bold')
        axesSi_std.set_xlim([0, 1])
        axesSi_std.set_title('Residuals (Si)')

        axesNb_std.plot(nSiNb[0:j+1,1], stdNb[0:j+1], 'o', color='r')
        axesNb_std.plot(nSiNb[j,1], stdNb[j], 'o', markeredgecolor='red', markersize = 20, markerfacecolor = 'None',
                        markeredgewidth=3)
        axesNb_std.grid(True)
        axesNb_std.set_xlabel('part of Nb', fontsize=14, fontweight='bold')
        axesNb_std.set_xlim([0, 1])
        axesNb_std.set_title('Residuals (Nb)')

        txtMix =  'The mix ratio now is: $Si_{{{0}}}Nb_{{{1}}}$ \n'.format(nSiNb[j,0], nSiNb[j,1])
        print ( 'The mix ratio now is: Si{0} Nb{1} \n'.format(nSiNb[j,0], nSiNb[j,1]) )
        fig.suptitle('The mix ratio now is: $Si_{{{0}}}Nb_{{{1}}}$\n{2}'.format(nSiNb[j,0], nSiNb[j,1], values_of_current_project).replace('_',' ').
                 replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur',', blur,'), fontsize=22)
        axesSi.set_title('Si 2p', fontsize=20)
        axesSi.legend(shadow=True, fancybox=True, loc='upper left')
        axesSi.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
        axesSi.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
        axesSi.set_ylim([0, 1])
        axesSi.set_xlim([105, 96])
        axesSi.tick_params(axis='both', which='major', labelsize=14)
        axesSi.tick_params(axis='both', which='minor', labelsize=12)
        axesSi.grid(True)
        axesSi.axvline(x=calcBE,linewidth=2, color='black')

        axesNb.set_title('Nb 3d', fontsize=20)
        axesNb.legend(shadow=True, fancybox=True, loc='upper left')
        axesNb.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
        axesNb.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
        axesNb.set_ylim([0, 1])
        axesNb.set_xlim([208, 200])
        axesNb.tick_params(axis='both', which='major', labelsize=14)
        axesNb.tick_params(axis='both', which='minor', labelsize=12)
        axesNb.grid(True)
        axesNb.axvline(x=202.85,linewidth=2, color='black')

        fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
        plt.draw()

        # fig.set_tight_layout(True)

        # save to the PNG file:
        out_file_name = "Si_%05.2f--Nb_%05.2f.png" %(nSiNb[j,0], nSiNb[j,1])
        fig.savefig( os.path.join(out_dir, out_file_name) )

    # figManager.window.showMaximized()
    plt.clf()
    result_axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    # fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
    fig.suptitle('Differences between theoretical and experimental data\n{}'.format(values_of_current_project).replace('_',' ').
                 replace(' alpha', ', $\\alpha$').replace('gamma','$\gamma$').replace(' blur',', blur,'), fontsize=22)

    residuals_stdSi_in_au = (stdSi/stdSi.max())*100
    residuals_stdNb_in_au = (stdNb/stdNb.max())*100

    result_axes.plot(nSiNb[:, 0],residuals_stdSi_in_au , 'o', markersize=10, color='b', alpha = 0.5,
                     label='$ RD(\mathbf{Si}) = \left \|{ \left \|{ \int{I_{exp}^{Si}(E)dE} } \\right \| - \left \|{ \int{I_{theor}^{Si}(E)dE} } \\right \| } \\right \| $')
    result_axes.plot(nSiNb[:, 0], residuals_stdNb_in_au, 'o', markersize=10, color='r', alpha = 0.5,
                     label='$ RD(\mathbf{Nb}) = \left \|{ \left \|{ \int{I_{exp}^{Nb}(E)dE} } \\right \| - \left \|{ \int{I_{theor}^{Nb}(E)dE} } \\right \| } \\right \| $')
    result_axes.plot(nSiNb[:, 0], (residuals_stdSi_in_au + residuals_stdNb_in_au)/2, 'o',markersize=14, color='black', label='$\\frac{RD(\mathbf{Nb})+ RD(\mathbf{Si})}{2}$')

    result_axes.legend(shadow=True, fancybox=True, loc='best')
    result_axes.set_ylabel('Residuals (%)', fontsize=16, fontweight='bold')
    result_axes.set_xlabel('Concentration $x$ of Si ($Si_xNb_{1-x}$)', fontsize=16, fontweight='bold')
    result_axes.set_xlim([0, 1])
    # result_axes.set_xlim([105, 96])
    result_axes.tick_params(axis='both', which='major', labelsize=14)
    result_axes.tick_params(axis='both', which='minor', labelsize=12)
    result_axes.grid(True)
    plt.draw()

    # save to the PNG file:

    out_file_name = 'result_' + values_of_current_project + '.png'
    fig.savefig( os.path.join(out_dir, out_file_name) )

    fig.show()
    print('-> program was finished')

if __name__ == "__main__":
    print ('-> you run ',  __file__, ' file in a main mode' )
    main_func_to_run()
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
    blur_or_sharp = ('blur', 'as_is', ) # 'sharp', 'as_is', 'blur'
    alpha = 0.5
    gamma = 0.5
    window_len = np.array((50, 100, 150, 200))
    window_name = ('gauss', 'lorentzian', 'voigt')

    # the value which we want to parallelize:
    argv = RIO_Nb
    if len(argv) > 0:
        num_cores = multiprocessing.cpu_count()
        if (len(argv) <= num_cores):
            print ('Program will be calculating on {} numbers of CPUs'.format(len(argv)) )
            time.sleep(1)
            print('Programm will calculate the next cases:\n{:}\n'.format(argv))
            for blr in blur_or_sharp:
                # the case is important if it has value 'blur' or 'sharp':
                if blr in ('blur', 'sharp'):
                    for winName in window_name:
                        for winLen in window_len:
                            def tmpFun(index):
                                main_func_to_run( RIO_Si = RIO_Si[index], RIO_Nb = RIO_Nb[index], blur_or_sharp = blr,
                                                  alpha=0.5, gamma = 0.5, window_len = winLen, window_name = winName)
                            Parallel(n_jobs=len(argv))( delayed(tmpFun)(i) for i in range(len(argv)) )
                else: # other choice is case 'as_is' which doesn't need 'window_name', and  'window_len'
                    def tmpFun(index):
                            main_func_to_run( RIO_Si = RIO_Si[index], RIO_Nb = RIO_Nb[index], blur_or_sharp = blr)
                    Parallel(n_jobs=len(argv))( delayed(tmpFun)(i) for i in range(len(argv)) )

        else:
            print('PC doesn''t have this numbers of needed CPUs for parallel calculation' )


    else:
        print('- > No selected case was found.')

    # Command for terminal to recursively find files in subdirectories and then copy to target directory:
    # find ./ -name 'result_*.png' -exec cp {} /home/yugin/VirtualboxShare/Si-Nb-Si-Glass/L2822-6_10-1.3-10nm/Version_45-deg_v03_001/result_images  \;
