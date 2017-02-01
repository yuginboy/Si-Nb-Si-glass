"""
Simple demo with multiple subplots.
"""
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# x1 = np.linspace(0.0, 5.0)
# x2 = np.linspace(0.0, 2.0)
#
# y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
# y2 = np.cos(2 * np.pi * x2)
#
# plt.subplot(2, 1, 1)
# plt.plot(x1, y1, 'ko-')
# plt.title('A tale of 2 subplots')
# plt.ylabel('Damped oscillation')
#
# plt.subplot(2, 1, 2)
# plt.plot(x2, y2, 'r.-')
# plt.xlabel('time (s)')
# plt.ylabel('Undamped')
#
# plt.show()
#
# import matplotlib.pyplot as plt
# import warnings
#
# import random
# fontsizes = [8, 16, 24, 32]
#
#
# def example_plot(ax):
#     ax.plot([1, 2])
#     ax.set_xlabel('x-label', fontsize=random.choice(fontsizes))
#     ax.set_ylabel('y-label', fontsize=random.choice(fontsizes))
#     ax.set_title('Title', fontsize=random.choice(fontsizes))

# fig, ax = plt.subplots()
# example_plot(ax)
# plt.tight_layout()
#
# fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
# example_plot(ax1)
# example_plot(ax2)
# example_plot(ax3)
# example_plot(ax4)
# plt.tight_layout()
#
# fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
# example_plot(ax1)
# example_plot(ax2)
# plt.tight_layout()
#
# fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
# example_plot(ax1)
# example_plot(ax2)
# plt.tight_layout()
#
# fig, axes = plt.subplots(nrows=3, ncols=3)
# for row in axes:
#     for ax in row:
#         example_plot(ax)
# plt.tight_layout()
#
#
# fig = plt.figure()
#
# ax1 = plt.subplot(221)
# ax2 = plt.subplot(223)
# ax3 = plt.subplot(122)
#
# # ax1 = plt.subplot(325)
# # ax2 = plt.subplot(326)
# # # ax3 = plt.subplot(121)
# # # ax4 = plt.subplot(122)
# plt.show()
# plt.show()

# example_plot(ax1)
# example_plot(ax2)
# example_plot(ax3)
#
# plt.tight_layout()
#
#
# fig = plt.figure()
#
# ax1 = plt.subplot2grid((3, 3), (0, 0))
# ax2 = plt.subplot2grid((3, 3), (0, 1), colspan=2)
# ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=2)
# ax4 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
#
# example_plot(ax1)
# example_plot(ax2)
# example_plot(ax3)
# example_plot(ax4)
#
# plt.tight_layout()




# fig = plt.figure()
#
# import matplotlib.gridspec as gridspec
#
# gs1 = gridspec.GridSpec(3, 1)
# ax1 = fig.add_subplot(gs1[0])
# ax2 = fig.add_subplot(gs1[1])
# ax3 = fig.add_subplot(gs1[2])
#
# example_plot(ax1)
# example_plot(ax2)
# example_plot(ax3)
#
# with warnings.catch_warnings():
#     warnings.simplefilter("ignore", UserWarning)
#     # This raises warnings since tight layout cannot
#     # handle gridspec automatically. We are going to
#     # do that manually so we can filter the warning.
#     gs1.tight_layout(fig, rect=[None, None, 0.45, None])
#
# gs2 = gridspec.GridSpec(2, 1)
# ax4 = fig.add_subplot(gs2[0])
# ax5 = fig.add_subplot(gs2[1])
#
# example_plot(ax4)
# example_plot(ax5)
#
# with warnings.catch_warnings():
#     # This raises warnings since tight layout cannot
#     # handle gridspec automatically. We are going to
#     # do that manually so we can filter the warning.
#     warnings.simplefilter("ignore", UserWarning)
#     gs2.tight_layout(fig, rect=[0.45, None, None, None])
#
# # now match the top and bottom of two gridspecs.
# top = min(gs1.top, gs2.top)
# bottom = max(gs1.bottom, gs2.bottom)
#
# gs1.update(top=top, bottom=bottom)
# gs2.update(top=top, bottom=bottom)
#
# plt.show()
# import scipy as sp
# import matplotlib as mpl
# from matplotlib import pyplot as plt
# from matplotlib.gridspec import GridSpec
#
# x = sp.linspace(-3,3,128) # arbitary x data
# y = sp.linspace(-3,3,128) # arbitary y data
# xx, yy = sp.meshgrid(x,y)
# z = sp.exp(-(xx)**2)*sp.exp(-(yy)**2)# arbitary z data
#
# fig1 = plt.figure(figsize=[4,3])
# gs = GridSpec(100,100,bottom=0.15,left=0.15,right=0.95)
#
# axT = fig1.add_subplot(gs[0:15,0:78])
# axColor = fig1.add_subplot(gs[22:,0:78])
# axR = fig1.add_subplot(gs[22:,85:99])
#
# pcObject = axColor.pcolormesh(x,y,z)
# lineT = axT.plot(x,sp.sum(z,0),linewidth=2,
#         color=[68.0/255,78.0/255,154.0/255])
#
# lineR = axR.plot(sp.sum(z,1),y,linewidth=2,
#         color=[68.0/255,78.0/255,154.0/255])
#
# axColor.tick_params(axis='both',color='w',length=3,width=1.5)
#
# axR.set_xticks([0,50])
# axR.set_xticklabels(['0','50'])
# axR.set_yticklabels('',visible=False)
# axR.tick_params(axis='both',length=3,width=1.5)
#
# axT.set_yticks([0,50])
# axT.set_yticklabels(['0','50'])
# axT.set_xticklabels('',visible=False)
# axT.tick_params(axis='both',length=3,width=1.5)
#
# axColor.set_xlabel('x data')
# axColor.set_ylabel('y data')
#
# plt.show()
#
# class MyClass:
#         i = 5435
#         def __init__(self):
#                 self.txt = 'fuhwreuifv'
#         def r(self):
#                 self.i+=234
#         def f(self):
#                 self.r()
#                 print('Hello World ' + self.txt + ' {}'.format(self.i))
# class Class_1():
#         def __init__(self):
#                 self.a = 1
#                 self.b = MyClass()
#         def get_I_number(self):
#                 self.a = MyClass.i
#         def set_I_number(self):
#                 MyClass.i = self.a
#
#
#
# a = MyClass()
# a.f()
# a.txt = '85748'
# a.f()
#
# A = Class_1()
# A.a = 23
# B = Class_1()
# B.a = 43
# print(A.b.i)
# print(B.b.i)
# B.set_I_number()
# print(A.b.i)
# print(B.b.i)

# import numpy as np
# import matplotlib.pyplot as plt
#
# plt.switch_backend('QT5Agg')
# # Example data
# t = np.arange(0.0, 1.0 + 0.01, 0.01)
# s = np.cos(4 * np.pi * t) + 2
#
# plt.rc('text', usetex=True)
# plt.rc('font', family='serif')
# plt.plot(t, s)
#
# plt.xlabel(r'\textbf{time} (s)')
# plt.ylabel(r'\textit{voltage} (mV)',fontsize=16)
# plt.title(r"\TeX\ is Number "
#           r"$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!",
#           fontsize=16, color='gray')
# # Make room for the ridiculously large title.
# plt.subplots_adjust(top=0.8)
#
# # plt.savefig('tex_demo')
# plt.show()
# print('')

#
#
# import lmfit
# import numpy as np
# import matplotlib
# # matplotlib.use('WXAgg')
#
# import matplotlib.pyplot as plt
#
# x = np.linspace(1, 5, 250)
# np.random.seed(0)
# y = 3.0*np.exp(-x/2) -5.0*np.exp(-(x-0.1)/10.) + 0.1*np.random.randn(len(x))
#
# p = lmfit.Parameters()
# p.add_many(('a1', 4.), ('a2', 4.), ('t1', 3.), ('t2', 3.))
#
# def residual(p):
#    return p['a1']*np.exp(-x/p['t1']) + p['a2']*np.exp(-(x-0.1)/p['t2'])-y
#
# # create Minimizer
# mini = lmfit.Minimizer(residual, p)
#
# # first solve with Nelder-Mead
# out1 = mini.minimize(method='Nelder')
#
# # then solve with Levenberg-Marquardt using the
# # Nelder-Mead solution as a starting point
# out2 = mini.minimize(method='leastsq', params=out1.params)
#
# lmfit.report_fit(out2.params, min_correl=0.5)
#
# ci, trace = lmfit.conf_interval(mini, out2, sigmas=[0.68,0.95],
#                                 trace=True, verbose=False)
# lmfit.printfuncs.report_ci(ci)
#
# plot_type = 2
# if plot_type == 0:
#     plt.plot(x, y)
#     plt.plot(x, residual(out2.params)+y )
#
# elif plot_type == 1:
#     cx, cy, grid = lmfit.conf_interval2d(mini, out2, 'a2','t2',30,30)
#     plt.contourf(cx, cy, grid, np.linspace(0,1,11))
#     plt.xlabel('a2')
#     plt.colorbar()
#     plt.ylabel('t2')
#
# elif plot_type == 2:
#     cx, cy, grid = lmfit.conf_interval2d(mini, out2, 'a1','t2',30,30)
#     plt.contourf(cx, cy, grid, np.linspace(0,1,11))
#     plt.xlabel('a1')
#     plt.colorbar()
#     plt.ylabel('t2')
#
#
# elif plot_type == 3:
#     cx1, cy1, prob = trace['a1']['a1'], trace['a1']['t2'],trace['a1']['prob']
#     cx2, cy2, prob2 = trace['t2']['t2'], trace['t2']['a1'],trace['t2']['prob']
#     plt.scatter(cx1, cy1, c=prob, s=30)
#     plt.scatter(cx2, cy2, c=prob2, s=30)
#     plt.gca().set_xlim((2.5, 3.5))
#     plt.gca().set_ylim((11, 13))
#     plt.xlabel('a1')
#     plt.ylabel('t2')
#
# if plot_type > 0:
#     plt.show()
#
#
#!/usr/bin/env python
#<examples/doc_nistgauss.py>
import numpy as np
from lmfit.models import GaussianModel, ExponentialModel
import sys
import matplotlib.pyplot as plt

dat = np.loadtxt('NIST_Gauss2.dat')
x = dat[:, 1]
y = dat[:, 0]

exp_mod = ExponentialModel(prefix='exp_')
pars = exp_mod.guess(y, x=x)

gauss1  = GaussianModel(prefix='g1_')
pars.update( gauss1.make_params())

pars['g1_center'].set(105, min=75, max=125)
pars['g1_sigma'].set(15, min=3)
pars['g1_amplitude'].set(2000, min=10)

gauss2  = GaussianModel(prefix='g2_')

pars.update(gauss2.make_params())

pars['g2_center'].set(155, min=125, max=175)
pars['g2_sigma'].set(15, min=3)
pars['g2_amplitude'].set(2000, min=10)

mod = gauss1 + gauss2 + exp_mod


init = mod.eval(pars, x=x)
plt.plot(x, y)
plt.plot(x, init, 'k--')

out = mod.fit(y, pars, x=x)

print(out.fit_report(min_correl=0.5))

plt.plot(x, out.best_fit, 'r-')
plt.show()
#<end examples/doc_nistgauss.py>