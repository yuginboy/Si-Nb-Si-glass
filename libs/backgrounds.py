'''
Collections of the different BackGround calculations
'''
from numpy import array, linspace, arange, zeros, ceil, amax, amin, argmax, argmin, abs, trapz
from numpy import polyfit, polyval, seterr, trunc, mean
from numpy.linalg import norm
from scipy.interpolate import interp1d



DEBUG = False
OPTION = 2

def shirley_base(x, y, tol=1e-5, maxit=5):
    """ S = shirley_base(x,y, tol=1e-5, maxit=10)
    Calculate the best auto-Shirley background S for a dataset (x,y). Finds the biggest peak
    and then uses the minimum value either side of this peak as the terminal points of the
    Shirley background.
    The tolerance sets the convergence criterion, maxit sets the maximum number
    of iterations.
    https://github.com/kaneod/physics/tree/master/python
    """

    # Make sure we've been passed arrays and not lists.
    x = array(x)
    y = array(y)

    # Sanity check: Do we actually have data to process here?
    if not (x.any() and y.any()):
        print ("shirley_base: One of the arrays x or y is empty. Returning zero background.")
        return zeros(x.shape)

    # Next ensure the energy values are *decreasing* in the array,
    # if not, reverse them.
    if x[0] < x[-1]:
        is_reversed = True
        x = x[::-1]
        y = y[::-1]
    else:
        is_reversed = False

    # Locate the biggest peak.
    maxidx = abs(y - amax(y)).argmin()

    # It's possible that maxidx will be 0 or -1. If that is the case,
    # we can't use this algorithm, we return a zero background.
    if maxidx == 0 or maxidx >= len(y) - 1:
        print ("shirley_base: Boundaries too high for algorithm: returning a zero background.")
        return zeros(x.shape)

    # Locate the minima either side of maxidx.
    lmidx = abs(y[0:maxidx] - amin(y[0:maxidx])).argmin()
    rmidx = abs(y[maxidx:] - amin(y[maxidx:])).argmin() + maxidx
    xl = x[lmidx]
    yl = y[lmidx]
    xr = x[rmidx]
    yr = y[rmidx]

    # Max integration index
    imax = rmidx - 1

    # Initial value of the background shape B. The total background S = yr + B,
    # and B is equal to (yl - yr) below lmidx and initially zero above.
    B = zeros(x.shape)
    B[:lmidx] = yl - yr
    Bnew = B.copy()

    it = 0
    while it < maxit:
        if DEBUG:
            print ("Shirley iteration: ", it)
        # Calculate new k = (yl - yr) / (int_(xl)^(xr) J(x') - yr - B(x') dx')
        ksum = 0.0
        for i in range(lmidx, imax):
            ksum += (x[i] - x[i + 1]) * 0.5 * (y[i] + y[i + 1]
                                               - 2 * yr - B[i] - B[i + 1])
        k = (yl - yr) / ksum
        # Calculate new B
        for i in range(lmidx, rmidx):
            ysum = 0.0
            for j in range(i, imax):
                ysum += (x[j] - x[j + 1]) * 0.5 * (y[j] +
                                                   y[j + 1] - 2 * yr - B[j] - B[j + 1])
            Bnew[i] = k * ysum
        # If Bnew is close to B, exit.
        if norm(Bnew - B) < tol:
            B = Bnew.copy()
            break
        else:
            B = Bnew.copy()
        it += 1

    if it >= maxit:
        print ("shirley_base: Max iterations exceeded before convergence.")
    if is_reversed:
        return (yr + B)[::-1]
    else:
        return yr + B


def shirley_new(x, y_in, maxit=5, numpoints=3):
    '''
    :param x: array of X
    :param y: array of Intensity or Y
    :param maxit: max number of iterations. Default is 5
    :param numpoints: number of points to calculate the average value for Y shift
    :return: Backgraund (Shirley-type ) y-values
    '''
    # Make sure we've been passed arrays and not lists.
    x = array(x)
    y = y_in.copy() # to avoid changes in the source array
    y = array(y)

    # Sanity check: Do we actually have data to process here?
    if not (x.any() and y.any()):
        print ("shirley_new: One of the arrays x or y is empty. Returning zero background.")
        return zeros(x.shape)

    # Next ensure the energy values are *decreasing* in the array,
    # if not, reverse them.
    if x[0] < x[-1]:
        is_reversed = True
        x = x[::-1]
        y = y[::-1]
    else:
        is_reversed = False

    # Locate the biggest peak.
    maxidx = abs(y - amax(y)).argmin()

    # It's possible that maxidx will be 0 or -1. If that is the case,
    # we can't use this algorithm, we return a zero background.
    if maxidx == 0 or maxidx >= len(y) - 1:
        print ("shirley_base: Boundaries too high for algorithm: returning a zero background.")
        return zeros(x.shape)

    # Locate the minima either side of maxidx.
    lmidx = abs(y[0:maxidx] - amin(y[0:maxidx])).argmin()
    rmidx = abs(y[maxidx:] - amin(y[maxidx:])).argmin() + maxidx
    xl = x[lmidx]
    yl = y[lmidx]
    xr = x[rmidx]
    yr = y[rmidx]

    # Initial value of the background shape B. The total background S = yr + B,
    # and B is equal to (yl - yr) below lmidx and initially zero above.
    zz = B = zeros(x.shape)
    B[:lmidx] = yl - yr

    it = 0
    for it in range(maxit):
        for i in range(len(y)):
            zz = y - yr - B
            Integ_k = trapz(zz, x=x)
            zz[0:i] = 0
            Integ = trapz(zz, x=x)
            kn = (yl - yr)/Integ_k
            B[i] = kn * Integ


    # Calculate a Y shift:
    if (rmidx+numpoints) > len(y):
        delta = y[rmidx]
    else:
        delta = y[rmidx:rmidx+numpoints].mean()

    # output
    if is_reversed:
        #return (yr + B)[::-1]
        return (delta + B)[::-1]
    else:
        # return yr + B
        return delta + B



