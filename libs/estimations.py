import numpy as np
import scipy as sp
import numpy as np
import math  as mh


def std_residual(xA, yAin, xB, yBin, region=None):
    '''

    :param xA: x-values for numpy.vector A
    :param yA: y-values for numpy.vector A
    :param xB: x-values for numpy.vector B
    :param yB: y-values for numpy.vector B
    :param region:  vector of two values: left and right side of the region for calculation of standard
    deviation between two vectors of the selected points.
                if region=None then will be calculating all points in two vectors
    :return:
    '''
    # to avoid changes in the source array
    yA = yAin.copy()
    yB = yBin.copy()
    if region == None:
        C = (yA - yB) ** 2
        return mh.sqrt(C.sum()) / C.size
    else:
        if len(region) < 2:
            C = (yA - yB) ** 2
            return mh.sqrt(C.sum()) / C.size
        else:
            region.sort()
            a = region[0]
            b = region[1]
            #  set elements outside the region zeroed out
            # yA[np.nonzero(xA <= a and xA >= b)[0]] = 0
            yA[xA <= a] = 0
            yA[xA >= b] = 0
            # yA[xA <= a and xA >= b] = 0

            yB[xB <= a] = 0
            yB[xB >= b] = 0
            # yB[np.nonzero(xB <= a and xB >= b)[0]] = 0
            # yB[xB <= a and xB >= b] = 0

            # print ('in region')
            C = (yB - yA) ** 2
            return mh.sqrt(C.sum()) / yB[yB != 0].size

def y_in_region(x, y_in, region=None):
    '''
    function return y=0 for that points, which are placed outside the region
    :param x: x - values of vector
    :param y: y - values of vector
    :param region:  [a,b] -
    :return:
    '''
    y = y_in.copy() # to avoid changes in the source array

    if region == None:
        return y
    else:
        if len(region) < 2:

            return y
        else:
            region.sort()
            a = region[0]
            b = region[1]
            #  set elements outside the region zeroed out
            y[x <= a] = 0
            y[x >= b] = 0

            return y

def get_integral_from_vector (x, y_in, region=None):
    '''

    :param x:
    :param y_in: must be a 1 dim array
    :param region:
    :return:
    '''
    y = y_in.copy() # to avoid changes in the source array
    return   np.trapz ( y_in_region(x, y, region), x = x )

def get_integral_in_region (x, y_in, region=None):
    '''

    :param x: must be a vector
    :param y_in:
    :param region:
    :return:
    '''
    y = y_in.copy() # to avoid changes in the source array
    if len(x.shape) > 1:
        print('x - values must be a vector, not a matrix')
        out = None
        return out

    if len(y.shape) == 2:
        n = y.shape[1]
        out = np.zeros(n)
        # calc a matrix:
        for i in range(n):
            out[i] = get_integral_from_vector (x, y_in[:,i], region)
        return out
    elif len(y.shape)==1:
        # calc a vector:
        out = get_integral_from_vector (x, y_in, region)
        return out
    else:
        print('cant calculate the integral' )
        out = None
        return out

if __name__ == "__main__":
    print ('in region')