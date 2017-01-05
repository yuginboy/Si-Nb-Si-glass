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
        self.thickness = 3 #A
        self.density = 19.3 #g/cm^3
        self.Egap = 7.8 #eV
        self.DIIMFP = '/MG/O/'
        Material.count = Material.count + 1
        self.id = Material.count
        self.number = self.id

    def info(self):
        print('-'*10)
        print ('id: {0}'.format(self.id))
        print ('current number: {0}'.format(self.number))
        print ('material: {0}'.format(self.material))
        print ('thickness: {0} A'.format(self.thickness))
        print ('density: {0} g/cm^3'.format(self.density))
        print ('Egap: {0} eV'.format(self.Egap))
        print ('DIIMFP: {0}'.format(self.DIIMFP))
        print('=' * 10)

class Au_bottom(Material):
    # bottom layer of gold
    def __init__(self):
        super(Au_bottom, self).__init__()
        self.thickness = 200  # A
        self.Egap = 0  # eV
        self.DIIMFP = '/Au/'

class Au_top(Au_bottom):
    # top layer of gold
    def __init__(self):
        super(Au_top, self).__init__()
        self.thickness = 3  # A

class Co_metal(Material):
    # metallic Cobalt layer
    def __init__(self):
        super(Co_metal, self).__init__()
        self.material = '/Co[metal]/'
        self.density = 8.896  # g/cm^3
        self.thickness = 15  # A
        self.Egap = 0  # eV
        self.DIIMFP = '/Co/'

class Co_Oxide(Material):
    # Cobalt Oxide layer CoO
    def __init__(self):
        super(Co_Oxide, self).__init__()
        self.material = '/Co[Co-O]/O[Co-O]/'
        self.density = 6.44  # g/cm^3
        self.thickness = 3  # A
        self.Egap = 2.6  # eV
        self.DIIMFP = '/Co/'

class Mg_Oxide(Material):
    # Magnesium Oxide layer MgO
    def __init__(self):
        super(Mg_Oxide, self).__init__()
        self.material = '/Mg[Mg-O]/O[Mg-O]/'
        self.density = 3.58  # g/cm^3
        self.thickness = 50  # A
        self.Egap = 7.8  # eV
        self.DIIMFP = '/MG/O/'

class Mg_Carbonate(Material):
    # Magnesium Carbonate MgCO3
    def __init__(self):
        super(Mg_Carbonate, self).__init__()
        self.material = '/Mg[Mg-CO3]/C/O[Mg-CO3]3/'
        self.density = 2.958  # g/cm^3
        self.thickness = 5  # A
        self.Egap = 5.1  # eV
        self.DIIMFP = '/MG/O/'

class Mg_Hydrate(Material):
    # Magnesium Hydrate Mg[OH]2
    def __init__(self):
        super(Mg_Hydrate, self).__init__()
        self.material = '/Mg[Mg-OH]/O[Mg-OH]2/H2/'
        self.density = 2.345  # g/cm^3
        self.thickness = 5  # A
        self.Egap = 7.6  # eV
        self.DIIMFP = '/MG/O/'

class C_contamination(Material):
    # Carbon contamination top layer
    def __init__(self):
        super(C_contamination, self).__init__()
        self.material = '/C/'
        self.density = 2.2  # g/cm^3
        self.thickness = 5  # A
        self.Egap = 0.0  # eV
        self.DIIMFP = '/C/'


if __name__ == "__main__":
    print ('-> you run ',  __file__, ' file in a main mode' )
    a = Material()
    a.density=5.4
    a.info()
    a = Mg_Hydrate()
    a.info()
