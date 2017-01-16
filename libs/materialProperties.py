'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2016-12-20
'''
class Material:
    # Base class for all type materials
    count = 0
    def __init__(self):
        self.material = '/Au/'
        self.layerLabel = 'Au'
        self.thickness = 3 #A
        self.density = 19.3 #g/cm^3
        self.Egap = 7.8 #eV
        self.DIIMFP = '/MG/O/'
        Material.count = Material.count + 1
        self.id = Material.count
        self.number = self.id
        self.layerDescription = '$Au[3.000\AA]$'

    def setlayerDescription (self):
        self.layerDescription = '$' + self.layerLabel + '[{0:1.3f}\AA]$'.format(self.thickness)

    def setThickness(self, x):
        if x <= 0.0001:
            x = 0.001
        self.thickness = x
        self.setlayerDescription()
    def setDensity(self, x):
        if x <= 0.0001:
            x = 0.001
        self.density = x
        self.setlayerDescription()
    def setEgap(self, x):
        if x < 0.0:
            x = 0.0
        self.Egap = x
        self.setlayerDescription()
    def info(self):
        print('-'*10)
        print ('id: {0}'.format(self.id))
        print ('current number: {0}'.format(self.number))
        print ('material: {0}'.format(self.material))
        print ('thickness: {0} A'.format(self.thickness))
        print ('density: {0} g/cm^3'.format(self.density))
        print ('Egap: {0} eV'.format(self.Egap))
        print ('DIIMFP: {0}'.format(self.DIIMFP))
        print ('layer label: {0}'.format(self.layerLabel))
        print ('layer description: {0}'.format(self.layerDescription))
        print('=' * 10)

class Au(Material):
    # bottom layer of gold
    def __init__(self):
        super(Au, self).__init__()
        self.material = '/Au/'
        self.thickness = 3  # A
        self.density = 19.3  # g/cm^3
        self.Egap = 0  # eV
        self.DIIMFP = '/Au/'
        self.setlayerDescription()

class Au_bottom(Material):
    # bottom layer of gold
    def __init__(self):
        super(Au_bottom, self).__init__()
        self.thickness = 200  # A
        self.Egap = 0  # eV
        self.DIIMFP = '/Au/'
        self.setlayerDescription()

class Au_top(Au_bottom):
    # top layer of gold
    def __init__(self):
        super(Au_top, self).__init__()
        self.thickness = 3  # A
        self.setlayerDescription()

class Co_metal(Material):
    # metallic Cobalt layer
    def __init__(self):
        super(Co_metal, self).__init__()
        self.material = '/Co[metal]/'
        self.layerLabel = 'Co'
        self.density = 8.896  # g/cm^3
        self.thickness = 15  # A
        self.Egap = 0  # eV
        self.DIIMFP = '/Co/'
        self.setlayerDescription()


class Co_Oxide(Material):
    # Cobalt Oxide layer CoO
    def __init__(self):
        super(Co_Oxide, self).__init__()
        self.material = '/Co[Co-O]/O[Co-O]/'
        self.layerLabel = 'CoO'
        self.density = 6.44  # g/cm^3
        self.thickness = 3  # A
        self.Egap = 2.6  # eV
        self.DIIMFP = '/Co/'
        self.setlayerDescription()

class Mg_Oxide(Material):
    # Magnesium Oxide layer MgO
    def __init__(self):
        super(Mg_Oxide, self).__init__()
        self.material = '/Mg[Mg-O]/O[Mg-O]/'
        self.layerLabel = 'MgO'
        self.density = 3.58  # g/cm^3
        self.thickness = 50  # A
        self.Egap = 7.8  # eV
        self.DIIMFP = '/MG/O/'
        self.setlayerDescription()

class Mg_Carbonate(Material):
    # Magnesium Carbonate MgCO3
    def __init__(self):
        super(Mg_Carbonate, self).__init__()
        self.material = '/Mg[Mg-CO3]/C/O[Mg-CO3]3/'
        self.layerLabel = 'MgCO_3'
        self.density = 2.958  # g/cm^3
        self.thickness = 5  # A
        self.Egap = 5.1  # eV
        self.DIIMFP = '/MG/O/'
        self.setlayerDescription()

class Mg_Hydrate(Material):
    # Magnesium Hydrate Mg[OH]2
    def __init__(self):
        super(Mg_Hydrate, self).__init__()
        self.material = '/Mg[Mg-OH]/O[Mg-OH]2/H2/'
        self.layerLabel = 'Mg[OH]_2'
        self.density = 2.345  # g/cm^3
        self.thickness = 5  # A
        self.Egap = 7.6  # eV
        self.DIIMFP = '/MG/O/'
        self.setlayerDescription()

class C_contamination(Material):
    # Carbon contamination top layer
    def __init__(self):
        super(C_contamination, self).__init__()
        self.material = '/C/O[O-C]/'
        self.layerLabel = '(C=O)'
        self.density = 2.2  # g/cm^3
        self.thickness = 5  # A
        self.Egap = 0.0  # eV
        self.DIIMFP = '/C/'
        self.setlayerDescription()

class CoO_Au_mix(Material):
    # Carbon contamination top layer
    def __init__(self):
        super(CoO_Au_mix, self).__init__()
        self.material = '/Co[Co-O]/O[Co-O]/Au/'
        self.layerLabel = '(CoO)_xAu_{1-x}'
        self.density = 2.2  # g/cm^3
        self.thickness = 5  # A
        self.Egap = 0.0  # eV
        self.DIIMFP = '/Co[Co-O]/O[Co-O]/Au/'
        self._x_amount_CoO_in_Au = 0.5
        self.setlayerDescription()

    def setlayerDescription(self):
        self.layerDescription = '$(CoO)|_{{{0:1.3f}}}Au|_{{{1:1.3f}}}[h={2:1.3f}\AA]$'.format(self._x_amount_CoO_in_Au,
                                                                                    (1-self._x_amount_CoO_in_Au),
                                                                                              self.thickness)
    def set_x_amount_CoO_in_Au(self, x):
        self._x_amount_CoO_in_Au = x
        self.updateProperties()
        self.setlayerDescription()

    def updateProperties(self):
        if abs(self._x_amount_CoO_in_Au) > 1:
            self._x_amount_CoO_in_Au = 0.99
        x = abs(self._x_amount_CoO_in_Au)
        y = 1-x
        self.material = '/Co[Co-O]{0:1.2f}/O[Co-O]{0:1.2f}/Au{1:1.2f}/'.format(x/2, y)
        self.DIIMFP = '/Co[Co-O]{0:1.2f}/O[Co-O]{0:1.2f}/Au{1:1.2f}/'.format(x/2, y)
        # self.density = Au.density*y + Co_Oxide.density*x
        self.density = round(19.3*y + 6.44*x, 3)
        # self.Egap = Co_Oxide.Egap*x
        self.Egap = round(2.6*x, 3)


if __name__ == "__main__":
    print ('-> you run ',  __file__, ' file in a main mode' )
    a = Material()
    a.density=5.4
    a.info()
    a = CoO_Au_mix()
    a.set_x_amount_CoO_in_Au(0.6)
    a.info()
