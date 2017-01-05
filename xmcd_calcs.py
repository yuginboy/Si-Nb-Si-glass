#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.special import wofz
from scipy import integrate
from libs.backgrounds import shirley_base, shirley_new
from libs.filtering import smooth_by_window

import os


inpfile = 'NORMCOAB.SDA'

cd_path = os.path.dirname(os.path.realpath(__file__))
path_to_file = os.path.join(cd_path,'data',inpfile)

data = np.loadtxt(path_to_file,float, skiprows = 1)
hv = data[:,0] # incoming energy
AbsP = data[:,1] # coef. absorption +
AbsM = data[:,2] # coef. absorption -


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

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    adjust_yaxis(ax2,(y1-y2)/2,v2)
    adjust_yaxis(ax1,(y2-y1)/2,v1)

def adjust_yaxis(ax,ydif,v):
    """shift axis ax by ydiff, maintaining point v at the same location"""
    inv = ax.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, ydif))
    miny, maxy = ax.get_ylim()
    miny, maxy = miny - v, maxy - v
    if -miny>maxy or (-miny==maxy and dy > 0):
        nminy = miny
        nmaxy = miny*(maxy+dy)/(miny+dy)
    else:
        nmaxy = maxy
        nminy = maxy*(miny+dy)/(maxy+dy)
    ax.set_ylim(nminy+v, nmaxy+v)


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

# bkg1 = []
# for l in hv:
#     if EL3 <= l:
#         a = (2/3)*I
#         bkg1.append(a)
#     else:
#         a = I2/2
#         bkg1.append(a)
# bkg1 = np.asarray(bkg1)
bkg1 = np.zeros((len(hv)))
bkg1[hv < EL3] = I2/2
bkg1[hv >= EL3] = (2/3)*I


# bkg2 = []
# for k in hv:
#     if EL2 <= k:
#         a = (1/3)*I
#         bkg2.append(a)
#     else:
#         a = I2/2
#         bkg2.append(a)
# bkg2 = np.asarray(bkg2)
bkg2 = np.zeros((len(hv)))
bkg2[hv < EL2] = I2/2
bkg2[hv >= EL2] = (1/3)*I



bkgTSF = bkg1 + bkg2
bkgGL = smooth_by_window(bkgTSF, window_len=15, window='voigt')

r = XAS - bkgGL
int_r = integr_intens(r, hv) #intagrated intensity calculation
int_XMCD = integr_intens(XMCD, hv) #intagrated intensity calculation



plt.close('all')
### for 'Qt4Agg' backend maximize figure
plt.switch_backend('QT4Agg')


# """Ploting"""
#
# plt.figure('XMCD "+" and "-"', dpi = 96)
# plt.grid(True)
# plt.ylabel('Absorption')
# plt.xlabel('Energy, [eV]')
# p1 = plt.plot(hv, AbsP, ls = '-', color = 'b', lw = 0.8)
# p2 = plt.plot(hv, AbsM, ls = '-', color = 'r', lw = 0.8)
# plt.show()



fig = plt.figure()
# gs1 = gridspec.GridSpec(1, 2)
fig.show()
# fig.set_tight_layout(True)
figManager = plt.get_current_fig_manager()
DPI = fig.get_dpi()
fig.set_size_inches(1024.0 / DPI, 768.0 / DPI, dpi=DPI)
figManager.window.setGeometry(10, 20, 1034, 788)

gs = gridspec.GridSpec(1,2)

axes1 = fig.add_subplot(gs[0,0])
axes1tw = axes1.twinx()
# plot the graphs:
axes1.plot(hv, XMCD, ls = '-', color = 'b', label='XMCD', lw = 2)
axes1tw.plot(hv, int_XMCD, ls = '-', color = 'r', label='int XMCD', lw = 1)
# axes1.plot(hv, bkg, ls = '-', color = 'g', label='Fermi-like TSF', lw = 1)

axes1.set_title('XMCD', fontsize=20)
axes1.legend(shadow=True, fancybox=True, loc='best')
axes1.set_ylabel('MCD', fontsize=16, fontweight='bold', color='b')
axes1tw.set_ylabel('MCD integration', fontsize=16, fontweight='bold', color='r')
axes1.set_xlabel('Energy (eV)', fontsize=16, fontweight='bold')
axes1.set_xlim([hv.min(), hv.max()])
axes1.tick_params(axis='both', which='major', labelsize=14)
axes1.tick_params(axis='both', which='minor', labelsize=12)
axes1.grid(True)
axes1.axvline(x=EL2,linewidth=1, linestyle=':', color='black')
axes1.axvline(x=EL3,linewidth=1, linestyle=':', color='black')

fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
align_yaxis(axes1, 0, axes1tw, 0)
plt.draw()

axes1.grid(True)



axes2 = fig.add_subplot(gs[0,1])
axes2tw = axes2.twinx()
axes2.plot(hv, XAS , ls = '-', color = 'b', label='XAS', lw = 1.5)
axes2.plot(hv, bkgGL, ls = '-', color = 'r', label='bg', lw = 1)
axes2tw.plot(hv, int_r, ls = '-', color = 'k', label='int R', lw = 1)
axes2.set_title('XAS', fontsize=20)
axes2.legend(shadow=True, fancybox=True, loc='lower right')
axes2.set_ylabel('XAS', fontsize=16, fontweight='bold', color='b')
axes2tw.set_ylabel('XAS Integration', fontsize=16, fontweight='bold', color='k')
axes2.set_xlabel('Energy (eV)', fontsize=16, fontweight='bold')
axes2.set_xlim([hv.min(), hv.max()])
axes2.tick_params(axis='both', which='major', labelsize=14)
axes2.tick_params(axis='both', which='minor', labelsize=12)
axes2.grid(True)
axes2.axvline(x=EL2,linewidth=1, linestyle=':', color='black')
axes2.axvline(x=EL3,linewidth=1, linestyle=':', color='black')
align_yaxis(axes2, 0, axes2tw, 0)
fig.tight_layout(rect=[0.03, 0.03, 1, 0.95], w_pad=1.1)
plt.draw()

axes2.grid(True)
plt.show()

"""Ploting"""
"""
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
plt.show()

plt.figure('XMCD', dpi = 96)   #figsize=(8,8),
plt.ylabel('XAS')
plt.xlabel('Energy, [eV]')
plt.grid(True)
p5 = plt.plot(hv, XAS, ls = '-', color = 'k', lw = 1.5)
# plt.yticks()
p6 = plt.plot(hv, bkg, ls = '--', color = 'r', lw = 1.0)
# p7 = plt.plot(hv, conv, ls = '-.', color = 'k', lw = 1)
p8 = plt.twinx()
p8 = plt.plot(hv, int_r, ls = '-', color = 'b', lw = 1.0)
plt.ylabel('XAS Integration', color='b')
plt.show()
# plt.savefig('myfig')
"""

"""Calculation (by Sum Rul)"""
"""
print ('--'*20)
# m_orbital and m_spin calculation using sum rules
p = float(input('p value = '))   #input p value
q = float(input('q value = '))   #input q value
r = float(input('r value = '))   #input r value
N3d = float(input('N3d value = '))   #input N3d value - 3d electron occupation 


m_orbit = (-4*q*(10 - N3d))/(3*r)
m_spin = -(6*p-4*q)*(10 - N3d)/r
ratio = m_orbit/m_spin
print('=='*20)
print (' m_orbit = ',m_orbit,'\n','m_spin = ',m_spin,'\n','m_orbit/m_spin = ', ratio)
""" 
print("DONE")