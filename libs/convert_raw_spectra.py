'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-01-16
Convert raw spectra to normalize raw spectra
'''
import os
from libs.dir_and_file_operations import listOfFilesFN_with_selected_ext
from libs.classFuncMinimize import runningScriptDir
import numpy as np

class ConvertRawToNormRaw():
    def __init__(self):
        self.in_path = os.path.join(runningScriptDir, 'exe', 'fit')
        self.out_path = os.path.join(runningScriptDir, 'exe', 'normalized_fit')
        self.list_of_files_to_convert = []
        self.new_file_prefix = ''

    def loadFiles(self):
        self.list_of_files_to_convert = [x for x in listOfFilesFN_with_selected_ext(self.in_path, ext='txt') if 'ref' in os.path.basename(x)]
        for i in self.list_of_files_to_convert:
            print(i)

    def saveOutData(self, name, x, y):
        f = open(os.path.join(self.out_path, self.new_file_prefix+name), 'w')
        outArr = np.zeros((len(x), 2))
        outArr[:, 0] = x
        outArr[:, 1] = y
        idx = 0
        for line in outArr:
            f.write('{0:.2f} {1:.1f}'.format(line[0], line[1]))
            idx += 1
            if idx < len(x):
                f.write('\n')
        f.close()

    def convertData(self):
        for i in self.list_of_files_to_convert:
            data = np.loadtxt(i).T
            x, y = data[0, :], data[1, :]
            ymax = np.max(y)
            y = 1e6*y/ymax
            self.saveOutData(os.path.basename(i), x, y)

if __name__=='__main__':
    print('-> you run ', __file__, ' file in a main mode')
    a = ConvertRawToNormRaw()
    a.loadFiles()
    a.convertData()