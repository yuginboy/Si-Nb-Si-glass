'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-01-09
'''
from libs.createSESSAprojectFile_CoO import SAMPLE
from libs.dataProperties import NumericData
import os
import pickle
import matplotlib.gridspec as gridspec
from matplotlib import pylab
import matplotlib.pyplot as plt
import datetime
import numpy as np
from libs.dir_and_file_operations import get_folder_name

# Create and write correct structure of layered material in *.ses project file:
class Sample_with_mix_of_CoO_Au(SAMPLE):
    def __init__(self):
        super(Sample_with_mix_of_CoO_Au, self).__init__()

    def createOutSesTxt(self):
        # put all txt information in outTxt variable:
        self.createSubstrate()

        self.outTxt = self.txtProperties
        self.outTxt = self.outTxt + self.txtSubstrate

        # add Au:
        self.addLayer(self.Au_bottom)
        # add Co-metal:
        self.addLayer(self.Co_metal)

        # add CoO_Au_mix:
        self.addLayer(self.CoO_Au_mix)

        # add CoO:
        self.addLayer(self.Co_oxide)
        # add Au 3A:
        self.addLayer(self.Au_interlayer)

        # add MgO:
        self.addLayer(self.MgO)
        # add MgCO3:
        self.addLayer(self.MgCO3)
        # add Mg[OH]2:
        self.addLayer(self.Mg_Hydrate)
        # add Mg[OH]2:
        self.addLayer(self.C_contamination)

        self.outTxt = self.outTxt + r'\PROJECT LOAD SESSION "additional_commands.ses"' + ' \n'


# change the load variables from the pickle file (loadMaterialsData),
# change the title on the figure (updatePlot)
class Class_for_mix_CoO_Au(NumericData):
    def __init__(self):
        super(Class_for_mix_CoO_Au, self).__init__()
        self.colorsForGraph = ['darkviolet', 'dodgerblue', 'brown', 'red', 'darkviolet']

    def loadMaterialsData(self):
        # Getting back the objects:
        pcklFile = os.path.join(self.theoryDataPath, 'objs.pickle')
        with open(pcklFile, 'rb') as f:
            obj = pickle.load(f)
        # print('')
        self.thicknessVector[0] = obj[0].Au_bottom.thickness
        self.thicknessVector[1] = obj[0].Co_metal.thickness
        self.thicknessVector[2] = obj[0].CoO_Au_mix.thickness
        self.thicknessVector[3] = obj[0].CoO_Au_mix._x_amount_CoO_in_Au
        self.thicknessVector[4] = obj[0].MgO.thickness
        self.thicknessVector[5] = obj[0].MgCO3.thickness
        self.thicknessVector[6] = obj[0].Mg_Hydrate.thickness
        self.thicknessVector[7] = obj[0].C_contamination.thickness

    def updatePlot(self, saveFigs=True):

        self.updateRfactor()
        self.loadMaterialsData()

        if self.showFigs:

            self.suptitle_txt = '$Fit$ $for$ $model$ $of$ $sample$' + \
                '$Au[{0:1.3f}\AA]/Co[{1:1.3f}\AA]'.format(self.thicknessVector[0], self.thicknessVector[1]) + \
                '/(CoO)|_{{{0:1.3f}}}Au|_{{{1:1.3f}}}[h={2:1.3f}\AA]'.format( self.thicknessVector[3], (1-self.thicknessVector[3]), self.thicknessVector[2]) + \
                '/MgO[{0:1.3f}\AA]/MgCO_3[{1:1.3f}\AA]/Mg(OH)_2[{2:1.3f}\AA]/C[{3:1.3f}\AA]$'.format(
                self.thicknessVector[4], self.thicknessVector[5], self.thicknessVector[6], self.thicknessVector[7])

            self.fig.clf()
            gs = gridspec.GridSpec(2, 2)

            self.Co2p.axes = self.fig.add_subplot(gs[0, 0])
            self.Co2p.axes.invert_xaxis()
            if abs(self.k_R_Co_0 + self.k_R_Co_60) > 0:
                Rtot = (self.k_R_Co_0 * self.Co2p._0.R_factor + self.k_R_Co_60 * self.Co2p._60.R_factor) / (
                self.k_R_Co_0 + self.k_R_Co_60)
            else:
                Rtot = (self.k_R_Co_0 * self.Co2p._0.R_factor + self.k_R_Co_60 * self.Co2p._60.R_factor) / 2
            self.Co2p.axes.set_title(
                'Co2p, $R_{{0}}=${0:1.4}, $R_{{60}}=${1:1.4}, $R_{{tot}}=${2:1.4}'.format(self.Co2p._0.R_factor,
                                                                                          self.Co2p._60.R_factor, Rtot))
            self.Co2p.axes.grid(True)

            self.Au4f.axes = self.fig.add_subplot(gs[0, 1])
            self.Au4f.axes.invert_xaxis()
            if abs(self.k_R_Au_0 + self.k_R_Au_60) > 0:
                Rtot = (self.k_R_Au_0 * self.Au4f._0.R_factor + self.k_R_Au_60 * self.Au4f._60.R_factor) / (
                self.k_R_Au_0 + self.k_R_Au_60)
            else:
                Rtot = (self.k_R_Au_0 * self.Au4f._0.R_factor + self.k_R_Au_60 * self.Au4f._60.R_factor) / 2
            self.Au4f.axes.set_title(
                'Au4f, $R_{{0}}=${0:1.4}, $R_{{60}}=${1:1.4}, $R_{{tot}}=${2:1.4}'.format(self.Au4f._0.R_factor,
                                                                                          self.Au4f._60.R_factor, Rtot))
            self.Au4f.axes.grid(True)

            self.O1s.axes = self.fig.add_subplot(gs[1, 0])
            self.O1s.axes.invert_xaxis()
            if abs(self.k_R_O_0 + self.k_R_O_60) > 0:
                Rtot = (self.k_R_O_0 * self.O1s._0.R_factor + self.k_R_O_60 * self.O1s._60.R_factor) / (
                self.k_R_O_0 + self.k_R_O_60)
            else:
                Rtot = (self.k_R_O_0 * self.O1s._0.R_factor + self.k_R_O_60 * self.O1s._60.R_factor) / 2
            self.O1s.axes.set_title(
                'O1s, $R_{{0}}=${0:1.4}, $R_{{60}}=${1:1.4}, $R_{{tot}}=${2:1.4}'.format(self.O1s._0.R_factor,
                                                                                         self.O1s._60.R_factor, Rtot))
            self.O1s.axes.grid(True)

            self.Mg1s.axes = self.fig.add_subplot(gs[1, 1])
            self.Mg1s.axes.invert_xaxis()
            if abs(self.k_R_Mg_0 + self.k_R_Mg_60) > 0:
                Rtot = (self.k_R_Mg_0 * self.Mg1s._0.R_factor + self.k_R_Mg_60 * self.Mg1s._60.R_factor) / (
                self.k_R_Mg_0 + self.k_R_Mg_60)
            else:
                Rtot = (self.k_R_Mg_0 * self.Mg1s._0.R_factor + self.k_R_Mg_60 * self.Mg1s._60.R_factor) / 2
            self.Mg1s.axes.set_title(
                'Mg1s, $R_{{0}}=${0:1.4}, $R_{{60}}=${1:1.4}, $R_{{tot}}=${2:1.4}'.format(self.Mg1s._0.R_factor,
                                                                                          self.Mg1s._60.R_factor, Rtot))
            self.Mg1s.axes.grid(True)

            self.Co2p.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.Co2p.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.Au4f.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.Au4f.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.O1s.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.O1s.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')
            self.Mg1s.axes.set_ylabel('Reletive Intensity (a.u.)', fontsize=16, fontweight='bold')
            self.Mg1s.axes.set_xlabel('Binding Energy (eV)', fontsize=16, fontweight='bold')

            # plot experimental data:
            self.Co2p.axes.plot(self.Co2p._0.experiment.data.fit.bindingEnergy,
                                self.Co2p._0.experiment.data.fit.intensity, '--', label=('Co2p $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            self.Co2p.axes.plot(self.Co2p._60.experiment.data.fit.bindingEnergy,
                                self.Co2p._60.experiment.data.fit.intensity, '--', label=('Co2p $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)

            self.Au4f.axes.plot(self.Au4f._0.experiment.data.fit.bindingEnergy,
                                self.Au4f._0.experiment.data.fit.intensity, '--', label=('Au4f $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            self.Au4f.axes.plot(self.Au4f._60.experiment.data.fit.bindingEnergy,
                                self.Au4f._60.experiment.data.fit.intensity, '--', label=('Au4f $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)

            self.O1s.axes.plot(self.O1s._0.experiment.data.fit.bindingEnergy,
                                self.O1s._0.experiment.data.fit.intensity, '--', label=('O1s $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            self.O1s.axes.plot(self.O1s._60.experiment.data.fit.bindingEnergy,
                                self.O1s._60.experiment.data.fit.intensity, '--', label=('O1s $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)

            self.Mg1s.axes.plot(self.Mg1s._0.experiment.data.fit.bindingEnergy,
                                self.Mg1s._0.experiment.data.fit.intensity, '--', label=('Mg1s $\\alpha=0^O$' + ' experiment'), color = self.colorsForGraph[0], linewidth=2.5)
            self.Mg1s.axes.plot(self.Mg1s._60.experiment.data.fit.bindingEnergy,
                                self.Mg1s._60.experiment.data.fit.intensity, '--', label=('Mg1s $\\alpha=60^O$' + ' experiment'), color = self.colorsForGraph[2], linewidth=2.5)



            # plot theoretical data
            self.Co2p.axes.plot(self.Co2p._0.theory.data.fit.bindingEnergy,
                                self.Co2p._0.theory.data.fit.intensity, '-', label=('Co2p $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            self.Co2p.axes.plot(self.Co2p._60.theory.data.fit.bindingEnergy,
                                self.Co2p._60.theory.data.fit.intensity, '-', label=('Co2p $\\alpha=60^O$' + ' theory'),
                             color=self.colorsForGraph[3], linewidth=5, alpha=0.5)

            self.Au4f.axes.plot(self.Au4f._0.theory.data.fit.bindingEnergy,
                                self.Au4f._0.theory.data.fit.intensity, '-', label=('Au4f $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            self.Au4f.axes.plot(self.Au4f._60.theory.data.fit.bindingEnergy,
                                self.Au4f._60.theory.data.fit.intensity, '-', label=('Au4f $\\alpha=60^O$' + ' theory'),
                             color=self.colorsForGraph[3], linewidth=5, alpha=0.5)

            self.O1s.axes.plot(self.O1s._0.theory.data.fit.bindingEnergy,
                                self.O1s._0.theory.data.fit.intensity, '-', label=('O1s $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            self.O1s.axes.plot(self.O1s._60.theory.data.fit.bindingEnergy,
                                self.O1s._60.theory.data.fit.intensity, '-', label=('O1s $\\alpha=60^O$' + ' theory'),
                             color=self.colorsForGraph[3], linewidth=5, alpha=0.5)

            self.Mg1s.axes.plot(self.Mg1s._0.theory.data.fit.bindingEnergy,
                                self.Mg1s._0.theory.data.fit.intensity, '-', label=('Mg1s $\\alpha=0^O$' + ' theory'),
                             color=self.colorsForGraph[1], linewidth=5, alpha=0.5)
            self.Mg1s.axes.plot(self.Mg1s._60.theory.data.fit.bindingEnergy,
                                self.Mg1s._60.theory.data.fit.intensity, '-', label=('Mg1s $\\alpha=60^O$' + ' theory'),
                             color=self.colorsForGraph[3], linewidth=5, alpha=0.5)


            self.Co2p.axes.legend(shadow=True, fancybox=True, loc='upper left')
            # Change the axes border width
            for axis in ['top', 'bottom', 'left', 'right']:
                self.Co2p.axes.spines[axis].set_linewidth(2)
                self.Au4f.axes.spines[axis].set_linewidth(2)
                self.O1s.axes.spines[axis].set_linewidth(2)
                self.Mg1s.axes.spines[axis].set_linewidth(2)

            # plt.subplots_adjust(top=0.85)
            # gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
            # self.fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)

            # put window to the second monitor
            # figManager.window.setGeometry(1923, 23, 640, 529)
            self.figManager.window.setGeometry(1920, 20, 1920, 1180)

            # plt.show()
            plt.draw()
            self.fig.suptitle(self.suptitle_txt, fontsize=22, fontweight='normal')

            # put window to the second monitor
            # figManager.window.setGeometry(1923, 23, 640, 529)
            # self.figManager.window.setGeometry(780, 20, 800, 600)



            self.figManager.window.setWindowTitle('CoO fitting')
            self.figManager.window.showMinimized()

        if saveFigs and self.showFigs:
            # save to the PNG file:
            timestamp = datetime.datetime.now().strftime("_[%Y-%m-%d_%H_%M_%S]_")
            out_file_name = get_folder_name(self.theoryDataPath) + timestamp + \
                            '_R={0:1.4}.png'.format(self.total_R_faktor)
            self.fig.savefig(os.path.join(self.theoryDataPath, out_file_name))



if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    a = Sample_with_mix_of_CoO_Au()
    a.CoO_Au_mix.set_x_amount_CoO_in_Au(0.7)
    a.CoO_Au_mix.info()
    a.Au_interlayer.thickness = 0.001
    a.Co_oxide.thickness = 0.001

    a = Class_for_mix_CoO_Au()
    a.theoryDataPath = r'/home/yugin/VirtualboxShare/Co-CoO/out/00003'
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

    # a.loadMaterialsData()
    # a.Au4f._0.experiment.data.selectEnergyValues()
    # a.Au4f._0.interpolateTheorData()
    # a.Au4f._0.calcRfactor()
    # a.Au4f._60.calcRfactor()
    #
    # a.Co2p._0.calcRfactor()
    # a.Co2p._60.calcRfactor()
    #
    # a.O1s._0.calcRfactor()
    # a.O1s._60.calcRfactor()
    #
    # a.Mg1s._0.calcRfactor()
    # a.Mg1s._60.calcRfactor()


    a.setupAxes()

    # start to Global Normolize procedure:
    a.Au4f._0.getMaxIntensityValue()
    a.Au4f._60.getMaxIntensityValue()
    print('a.Au4f._0.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._0.experiment.data.fit.maxIntensity))
    print('a.Au4f._0.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._0.theory.data.fit.maxIntensity))
    print('a.Au4f._60.experiment.data.fit.maxIntensity = {0}'.format(a.Au4f._60.experiment.data.fit.maxIntensity))
    print('a.Au4f._60.theory.data.fit.maxIntensity = {0}'.format(a.Au4f._60.theory.data.fit.maxIntensity))

    a.Co2p._0.getMaxIntensityValue()
    a.Co2p._60.getMaxIntensityValue()
    print('a.Co2p._0.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._0.experiment.data.fit.maxIntensity))
    print('a.Co2p._0.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._0.theory.data.fit.maxIntensity))
    print('a.Co2p._60.experiment.data.fit.maxIntensity = {0}'.format(a.Co2p._60.experiment.data.fit.maxIntensity))
    print('a.Co2p._60.theory.data.fit.maxIntensity = {0}'.format(a.Co2p._60.theory.data.fit.maxIntensity))

    a.O1s._0.getMaxIntensityValue()
    a.O1s._60.getMaxIntensityValue()
    print('a.O1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._0.experiment.data.fit.maxIntensity))
    print('a.O1s._0.theory.data.fit.maxIntensity = {0}'.format(a.O1s._0.theory.data.fit.maxIntensity))
    print('a.O1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.O1s._60.experiment.data.fit.maxIntensity))
    print('a.O1s._60.theory.data.fit.maxIntensity = {0}'.format(a.O1s._60.theory.data.fit.maxIntensity))

    a.Mg1s._0.getMaxIntensityValue()
    a.Mg1s._60.getMaxIntensityValue()
    print('a.Mg1s._0.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.experiment.data.fit.maxIntensity))
    print('a.Mg1s._0.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._0.theory.data.fit.maxIntensity))
    print('a.Mg1s._60.experiment.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.experiment.data.fit.maxIntensity))
    print('a.Mg1s._60.theory.data.fit.maxIntensity = {0}'.format(a.Mg1s._60.theory.data.fit.maxIntensity))

    maxIntensity_0_theory = np.max([a.Au4f._0.theory.data.fit.maxIntensity, a.Co2p._0.theory.data.fit.maxIntensity,
                                    a.O1s._0.theory.data.fit.maxIntensity, a.Mg1s._0.theory.data.fit.maxIntensity])
    maxIntensity_60_theory = np.max([a.Au4f._60.theory.data.fit.maxIntensity, a.Co2p._60.theory.data.fit.maxIntensity,
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

    a.updatePlot()
    print('R-factor = {}'.format(a.Au4f._60.R_factor))
