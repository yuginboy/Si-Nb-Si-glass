'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-12-20
'''
from libs.materialProperties import *
import os
import prettytable as pt
import numpy as np

tmpMaterial = Au_bottom()

class SAMPLE():

    def __init__(self):
        self.outTxt = []
        self.txtSubstrate = []

        self.Au_bottom = Au_bottom()
        self.Co_metal = Co_metal()
        self.Co_oxide = Co_Oxide()
        self.Au_interlayer = Au_top()
        self.CoO_Au_mix = CoO_Au_mix()
        self.MgO = Mg_Oxide()
        self.MgCO3 = Mg_Carbonate()
        self.Mg_Hydrate = Mg_Hydrate()
        self.C_contamination = C_contamination()
        self.Au_top = Au_top()
        self.layersDescriptionTxt = ''
        self.layerDict = {}
        self.layerStructure = dict()
        self.layerIdNum = 0
        self.d = {}
        self.tabledLayersStructureInfo = ''
        self.layersThicknessVector = []
        # init the structure with the default parameters for layers:
        self.initializeStructure()

        self.sesFilename = 'load.ses'
        self.workDir = '/home/yugin/VirtualboxShare/Co-CoO/src/2016-11-21/tmp'

        self.txtProperties = r'\proj reset ' + ' \n' + r'\PREFERENCES SET THRESHOLD 0.090000 ' + ' \n' \
                             + r'\PREFERENCES SET PLOT_ZERO 1.000000e-008 ' + ' \n' + r'\PREFERENCES SET DENSITY_SCALE MASS' + ' \n'

    def addLayerToStructure(self, mat = tmpMaterial):
        # create  layer in structure:
        self.layerIdNum = self.layerIdNum + 1
        i = self.layerIdNum
        # tmpD = {}
        # tmpD['a'] = i**2
        # SAMPLE.d[i] = i
        # SAMPLE.d[i] = tmpD

        self.layerDict['layer Id Number'] = self.layerIdNum
        self.layerDict['material'] = mat
        # print(self.layerDict)
        # SAMPLE.layerStructure[i] = dict()
        # print(SAMPLE.layerStructure[i])
        self.layerStructure[i] = dict(self.layerDict)
        # print(SAMPLE.layerStructure[i])

    def initializeStructure(self):
        # init the structure with the default parameters for layers:

        # add Au:
        self.addLayerToStructure(self.Au_bottom)
        # add Co-metal:
        self.addLayerToStructure(self.Co_metal)

        # # add CoO_Au_mix:
        # self.addLayer(self.CoO_Au_mix)

        # add CoO:
        self.addLayerToStructure(self.Co_oxide)
        # add Au 3A:
        self.addLayerToStructure(self.Au_interlayer)

        # add MgO:
        self.addLayerToStructure(self.MgO)
        # add MgCO3:
        self.addLayerToStructure(self.MgCO3)
        # add Mg[OH]2:
        self.addLayerToStructure(self.Mg_Hydrate)

        # add C contamination on a surface:
        self.addLayerToStructure(self.C_contamination)

    def createSubstrate(self):
        # put info about substrate:
        self.txtSubstrate = r'\SAMPLE SET MATERIAL /Si[x]/ LAYER 1' + ' \n' + \
                            r'\SAMPLE SET MATERIAL /Co[metal]/Co[Co-O]/O[Co-O]/Au/Mg[Mg-O]/O[Mg-O]/Mg[Mg-OH]/O[Mg-OH]/Mg[Mg-CO3]/O[Mg-CO3]/ LAYER 1' + ' \n'

    def addLayersProfileToSESSA(self):
         for i in self.layerStructure:
            mat = self.layerStructure[i]['material']

            if i == 1:
                self.layersDescriptionTxt = self.layersDescriptionTxt + mat.layerDescription
            else:
                self.layersDescriptionTxt = self.layersDescriptionTxt + '/' + mat.layerDescription

            # mat = SAMPLE.layerStructure['material']
            # t1 = r'\SAMPLE ADD LAYER /Si1.0/ THICKNESS 5 ABOVE 0' + ' \n'
            # t2 = r'\SAMPLE SET MATERIAL ' + mat.material + ' LAYER 1' + ' \n'
            # t3 = r'\SAMPLE SET THICKNESS ' + '{0:.3f}'.format(mat.thickness) + ' LAYER 1' + ' \n'
            # t4 = r'\SAMPLE SET EGAP ' + '{0:.1f}'.format(mat.Egap) + ' LAYER 1' + ' \n'
            # t5 = r'\SAMPLE PARAMETERS SET DIIMFP MATERIAL "' + '{0}'.format(mat.DIIMFP) + '" LAYER 1' + ' \n'
            # t6 = r'\SAMPLE SET DENSITY ' + '{0:1.3e}'.format(mat.density) + ' LAYER 1' + ' \n'

            t1 = r'\SAMPLE ADD LAYER /Si1.0/ THICKNESS 5 ABOVE 0' + ' \n'
            t2 = r'\SAMPLE SET MATERIAL ' + mat.material + ' LAYER 1' + ' \n'
            t3 = r'\SAMPLE SET THICKNESS ' + '{0:.4f}'.format(mat.thickness) + ' LAYER 1' + ' \n'
            t4 = r'\SAMPLE SET EGAP ' + '{0:.1f}'.format(mat.Egap) + ' LAYER 1' + ' \n'
            t5 = r'\SAMPLE PARAMETERS SET DIIMFP MATERIAL "' + '{0}'.format(mat.DIIMFP) + '" LAYER 1' + ' \n'
            t6 = r'\SAMPLE SET DENSITY ' + '{0:1.3e}'.format(mat.density) + ' LAYER 1' + ' \n'

            self.outTxt = self.outTxt + t1 + t2 + t3 + t4 + t5 + t6 + ' \n'

    def getLayersStructureInfo(self):
        # create text info about structure:
        x = pt.PrettyTable(["Layer Num", "Material", "Thickness"])
        x.align["Material"] = "l"  # Left align city names
        for i in self.layerStructure:
            x.add_row(
                [self.layerStructure[i]['layer Id Number'],
                self.layerStructure[i]['material'].material,
                self.layerStructure[i]['material'].thickness]
                       )
        print(x)
        self.tabledLayersStructureInfo = x.get_string()

    def getLayersThicknessVector(self):
        self.layersThicknessVector =  np.zeros(len(self.layerStructure))
        for i in self.layerStructure:
            self.layersThicknessVector[i-1] = self.layerStructure[i]['material'].thickness

    def printLayersThicknessVector(self):
        txt = '('
        k = 0
        for i in self.layersThicknessVector:
            if k < 1:
                txt = txt + '{:1.3f}'.format(i)
            else:
                txt = txt + ', {:1.3f}'.format(i)
            k +=1
        print('layers thickness vector is: ' + txt + ')')

    def createOutSesTxt(self):
        # put all txt information in outTxt variable:
        self.createSubstrate()

        self.outTxt =  self.txtProperties
        self.outTxt = self.outTxt + self.txtSubstrate

        self.addLayersProfileToSESSA()

        self.outTxt = self.outTxt + r'\PROJECT LOAD SESSION "additional_commands.ses"' + ' \n'


    def writeSesFile(self):
        # write to the disk SESSA project file:


        self.createOutSesTxt()
        self.getLayersStructureInfo()
        self.getLayersThicknessVector()

        fn = os.path.join(self.workDir, self.sesFilename)
        # delete file if exist:
        if os.path.isfile(fn):
            os.remove(fn)
        # create new file for writing:
        f = open(fn, 'w')
        for line in self.outTxt:
            f.write(line)

        f.close()


if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    a = SAMPLE()
    # a.CoO_Au_mix.set_x_amount_CoO_in_Au(0.7)
    # a.CoO_Au_mix.info()
    # a.Au_interlayer.setThickness(0.001)
    # a.Co_oxide.setThickness(0.001)
    a.writeSesFile()
    print('layers description is: ' + a.layersDescriptionTxt)
    # print('number of layers is: {0}'.format(len(SAMPLE.layerStructure)))
    # a.getLayersStructureInfo()
    a.printLayersThicknessVector()