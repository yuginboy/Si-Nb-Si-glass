#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import wofz
from scipy import integrate

inpfile = r'NORMCOAB.SDA'

data = np.loadtxt(inpfile,float, skiprows = 1)
hv = data[:,0] # incoming energy
AbsP = data[:,1] # coef. absorption +
AbsM = data[:,2] # coef. absorption -

def G(x, alpha):
    # Return Gaussian line shape at x with HWHM alpha """
    return np.sqrt(np.log(2) / np.pi) / alpha\
                             * np.exp(-(x / alpha)**2 * np.log(2))

def L(x, gamma):
    # Return Lorentzian line shape at x with HWHM gamma
    return gamma / np.pi / (x**2 + gamma**2)

def V(x, alpha, gamma):
    # Return the Voigt line shape at x with Lorentzian component HWHM gamma
    # and Gaussian component HWHM alpha.
    sigma = alpha / np.sqrt(2 * np.log(2))
    return np.real(wofz((x + 1j*gamma)/sigma/np.sqrt(2))) / sigma/np.sqrt(2*np.pi)

def TwoStepFunc (x, E3, E2, h, h2):
    step = h2 + ((2/3)*(h-h2)) / (1 + np.exp(E3-x)) + ((1/3)*(h-h2)/(1 + np.exp(E2-x))) # +++
    return step
    
def integr_intens (x,y):
    int = integrate.cumtrapz(x,y, initial = 0)
    return (int)

def str_l(x1, x2, y):
    ns = x1[0] / x2[0]
    ne =  x1[-1] / x2[-1]
    b = (ne - ns)/(y[-1] - y[0])
    line = ns + hv*b
    return (line)


def int_aver (data, arr, a, b):
      x1 = a                        # for XAS to be starting from zero point intensity (intensity of removed line func)
      hvll = arr.tolist()
      x2 = hvll.index(arr[x1] + b)
      aver_int = np.average(data[x1:x2])
      return (aver_int)

def int_aver2 (data, arr, a, b):
      x1 = a                        # for XAS to be starting from zero point intensity (intensity of removed line func)
      hvll = arr.tolist()
      x2 = hvll.index(arr[x1] - b)
      aver_int = np.average(data[x2:x1])
      return (aver_int)

      
def Vweigt(values, window = 15):
    f = np.r_[values[window-1:0:-1],values,values[-1:-window:-1]]
    weigts = np.linspace(-1,1, window)
    weigts = V(weigts, alpha, gamma)
    # weigts /= weigts.sum()
    
    a = np.convolve(weigts/weigts.sum(),f,mode='valid')
    return a [(window/2):-(window/2)]

def Lweigt(values, window = 15):
    f = np.r_[values[window-1:0:-1],values,values[-1:-window:-1]]
    weigts = np.linspace(-1,1, window)
    weigts = L(weigts, gamma)
    # weigts /= weigts.sum()
    
    a = np.convolve(weigts/weigts.sum(),f,mode='valid')
    return a [(window/2):-(window/2)]

    
def Gweigt(values, window = 15):
    f = np.r_[values[window-1:0:-1],values,values[-1:-window:-1]]
    weigts = np.linspace(-1,1, window)
    weigts = G(weigts, alpha)
    # weigts /= weigts.sum()
    
    a = np.convolve(weigts/weigts.sum(),f,mode='valid')
    return a [(window/2):-(window/2)]


# ft = str_l (AbsP, AbsM, hv)
# AbsP = (AbsP*ft)
# AbsM = (AbsM*ft)
# AbsP = AbsP - (int_aver (AbsP, hv, 0, 5))
# AbsM = AbsM - (int_aver (AbsM, hv, 0, 5))

XMCD = AbsP - AbsM
XAS = AbsP + AbsM

I = int_aver2(XAS, hv, -1, 15)
I2 = int_aver(XAS, hv, 0, 5)
    
# alpha = float(input('(Gaussian energy resolution broadening), alpha value = '))   #input sigma value (Gaussian energy resolution broadening)
alpha = 0.5
# gamma = float(input('(Lorentzian life-time broadening), gamma value = '))   #input gamma value (Lorentzian life-time broadening)
gamma = 0.43
# EL3 = float(input('E L3 value (eV) = '))   #input peak posititon value
EL3 = 778
# EL2 = float(input('E L2 value (eV) = '))   #input peak posititon value
EL2 = 793

bkg = TwoStepFunc(hv, EL3, EL2, I, I2)

bkg1 = []
for l in hv:
    if EL3 <= l:
        a = (2/3)*I
        bkg1.append(a)
    else:
        a = I2/2
        bkg1.append(a)
bkg1 = np.asarray(bkg1)

bkg2 = []
for k in hv:
    if EL2 <= k:
        a = (1/3)*I
        bkg2.append(a)
    else:
        a = I2/2
        bkg2.append(a)
bkg2 = np.asarray(bkg2)

bkgTSF = bkg1 + bkg2
bkgGL = Gweigt(Lweigt(bkgTSF))

r = XAS - bkgGL
int_r = integr_intens(r, hv) #intagrated intensity calculation
int_XMCD = integr_intens(XMCD, hv) #intagrated intensity calculation

"""Ploting"""

plt.figure('XMCD "+" and "-"', dpi = 96)
plt.grid(True)
plt.ylabel('Absorption')
plt.xlabel('Energy, [eV]')
p1 = plt.plot(hv, AbsP, ls = '-', color = 'b', lw = 0.8)
p2 = plt.plot(hv, AbsM, ls = '-', color = 'r', lw = 0.8)
plt.show()

plt.figure('XMCD', dpi = 96)
plt.ylabel('MCD')
plt.xlabel('Energy, [eV]')
plt.grid(True)
p3 = plt.plot(hv, XMCD, ls = '-', color = 'k', lw = 1.5)
p4 = plt.twinx()
p4 = plt.plot(hv, int_XMCD, ls = '-', color = 'r', lw = 1.0)
plt.ylabel('MCD Integration', color='r')
align_yaxis(ax1, 0, ax2, 0)
plt.show()

plt.figure('XMCD', dpi = 96)   #figsize=(8,8),
plt.ylabel('XAS')
plt.xlabel('Energy, [eV]')
plt.grid(True)
p5 = plt.plot(hv, XAS, ls = '-', color = 'k', lw = 1.5)
# plt.yticks()
p6 = plt.plot(hv, bkgGL, ls = '--', color = 'r', lw = 1.0)
# p7 = plt.plot(hv, conv, ls = '-.', color = 'k', lw = 1)
p8 = plt.twinx()
p8 = plt.plot(hv, int_r, ls = '-', color = 'b', lw = 1.0)
plt.ylabel('XAS Integration', color='b')
plt.show()
# plt.savefig('myfig')

# """Calculation (by Sum Rul)"""
#
# print ('--'*20)
# # m_orbital and m_spin calculation using sum rules
# p = float(input('p value = '))   #input p value
# q = float(input('q value = '))   #input q value
# r = float(input('r value = '))   #input r value
# N3d = float(input('N3d value = '))   #input N3d value - 3d electron occupation
#
#
# m_orbit = (-4*q*(10 - N3d))/(3*r)
# m_spin = -(6*p-4*q)*(10 - N3d)/r
# ratio = m_orbit/m_spin
# print('=='*20)
# print (' m_orbit = ',m_orbit,'\n','m_spin = ',m_spin,'\n','m_orbit/m_spin = ', ratio)

print("DONE")