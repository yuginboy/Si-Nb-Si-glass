'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-01-11
'''
import numpy as np
class SESSA_Step(object):
    # round to the 3 decimals
    def __init__(self, xmax=[1.1,1.1], xmin=[0.001,0.001], stepsize=0.5):
        self.stepsize = stepsize
        self.xmax = np.array(xmax)
        self.xmin = np.array(xmin)
    def __call__(self, x):
        """take a random step but ensure the new position is within the bounds"""
        while True:
            # this could be done in a much more clever way, but it will work for example purposes
            xnew = x + np.random.uniform(-self.stepsize, self.stepsize, np.shape(x))
            if np.all(xnew < self.xmax) and np.all(xnew > self.xmin):
                break
        return np.round(xnew, 3)

class BH_Bounds_for_SESSA(object):
    def __init__(self, xmax=[1.1,1.1], xmin=[0.001,0.001] ):
        self.xmax = np.array(xmax)
        self.xmin = np.array(xmin)
    def __call__(self, **kwargs):
        x = kwargs["x_new"]
        tmax = bool(np.all(x <= self.xmax))
        tmin = bool(np.all(x >= self.xmin))
        return tmax and tmin
if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')