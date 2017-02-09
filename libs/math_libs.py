'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-02-09
'''
import numpy as np
def approx_jacobian(x,func,epsilon=1e-3,*args):
    """Approximate the Jacobian matrix of callable function func

       * Parameters
         x       - The state vector at which the Jacobian matrix is
desired
         func    - A vector-valued function of the form f(x,*args)
         epsilon - The peturbation used to determine the partial derivatives
         *args   - Additional arguments passed to func

       * Returns
         An array of dimensions (lenf, lenx) where lenf is the length
         of the outputs of func, and lenx is the number of

       * Notes
         The approximation is done using forward differences
         from: https://mail.scipy.org/pipermail/scipy-user/2008-November/018725.html

    """
    x0 = np.asfarray(x)
    f0 = func(*((x0,)+args))
    jac = np.zeros([np.size(x0), np.size(f0)])
    dx = np.zeros(len(x0))
    for i in range(len(x0)):
       dx[i] = epsilon
       jac[i] = (func(*((x0+dx,)+args)) - f0)/epsilon
       dx[i] = 0.0
    return jac.transpose()
