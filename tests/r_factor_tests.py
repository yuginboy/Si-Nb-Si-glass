'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-02-24
'''
import numpy as np
import matplotlib.pyplot as plt

def get_R_factor(y_theor, y_exper):
    Rsq = np.power((y_theor-y_exper),2)
    Rsq_sum = np.sum(Rsq)
    Y_sq_exper = np.power(y_exper,2)
    Y_sq_exper_sum = np.sum(Y_sq_exper)
    R_0 = Rsq_sum/Y_sq_exper_sum
    R_1 = R_0/np.size(y_theor)
    return R_0, R_1

if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    Num_of_elem = 1000
    x = np.linspace(0, 10, Num_of_elem)
    y_exper = 0.1*np.sin(x)
    y_theor = y_exper*0.9
    plt.plot(x, y_exper, label='exper')
    plt.plot(x, y_theor, label='theor')
    plt.legend()
    txt = '$N=$ {0}, $R_1=$ {1:1.4f}, $R_2=$ {2:1.4f}'.format(Num_of_elem, get_R_factor(y_theor, y_exper)[0], get_R_factor(y_theor, y_exper)[1],)
    plt.title(txt)
    plt.show()