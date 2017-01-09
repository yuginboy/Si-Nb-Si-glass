'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-12-20
'''
from libs.materialProperties import *
import os

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

        self.sesFilename = 'load.ses'
        self.workDir = '/home/yugin/VirtualboxShare/Co-CoO/src/2016-11-21/tmp'

        self.txtProperties = r'\proj reset ' + ' \n' + r'\PREFERENCES SET THRESHOLD 0.090000 ' + ' \n' \
                             + r'\PREFERENCES SET PLOT_ZERO 1.000000e-008 ' + ' \n' + r'\PREFERENCES SET DENSITY_SCALE MASS' + ' \n'



    def createSubstrate(self):
        # put info about substrate:
        self.txtSubstrate = r'\SAMPLE SET MATERIAL /Si[x]/ LAYER 1' + ' \n' + \
                            r'\SAMPLE SET MATERIAL /Co[metal]/Co[Co-O]/O[Co-O]/Au/Mg[Mg-O]/O[Mg-O]/Mg[Mg-OH]/O[Mg-OH]/Mg[Mg-CO3]/O[Mg-CO3]/ LAYER 1' + ' \n'


    def addLayer(self, mat = tmpMaterial):
        # create  layer above the last created:
        t1 = r'\SAMPLE ADD LAYER /Si1.0/ THICKNESS 5 ABOVE 0' + ' \n'
        t2 = r'\SAMPLE SET MATERIAL ' + mat.material + ' LAYER 1' + ' \n'
        t3 = r'\SAMPLE SET THICKNESS ' + '{0:.3f}'.format(mat.thickness) + ' LAYER 1' + ' \n'
        t4 = r'\SAMPLE SET EGAP ' + '{0:.1f}'.format(mat.Egap) + ' LAYER 1' + ' \n'
        t5 = r'\SAMPLE PARAMETERS SET DIIMFP MATERIAL "' + '{0}'.format(mat.DIIMFP) + '" LAYER 1' + ' \n'
        t6 = r'\SAMPLE SET DENSITY ' + '{0:1.3e}'.format(mat.density) + ' LAYER 1' + ' \n'

        self.outTxt = self.outTxt + t1 + t2 + t3 + t4 + t5 + t6 + ' \n'

    def createOutSesTxt(self):
        # put all txt information in outTxt variable:
        self.createSubstrate()

        self.outTxt =  self.txtProperties
        self.outTxt = self.outTxt + self.txtSubstrate

        # add Au:
        self.addLayer(self.Au_bottom)
        # add Co-metal:
        self.addLayer(self.Co_metal)

        # # add CoO_Au_mix:
        # self.addLayer(self.CoO_Au_mix)

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


    def writeSesFile(self):
        # write to the disk SESSA project file:


        self.createOutSesTxt()

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
    a.CoO_Au_mix.set_x_amount_CoO_in_Au(0.7)
    a.CoO_Au_mix.info()
    a.Au_interlayer.thickness = 0.001
    a.Co_oxide.thickness = 0.001
    a.writeSesFile()