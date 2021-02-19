import sys
from math import log
import numpy as np
import levmar

def double_invexp(p, t):
    Vmax  = p[0]
    tau1  = p[1]
    tau2  = p[2]
    Toff  = p[3]
    if (tau1-tau2)<1.0e-12:
        return Vmax * (1.0 - ((tau1+(t-Toff))/tau1)*np.exp(-(t-Toff)/tau1))
    else:
        delta_tau_inv = 1.0/(tau1-tau2)
        return Vmax * (1.0 - tau1*delta_tau_inv*np.exp(-(t-Toff)/tau1) + tau2*delta_tau_inv*np.exp(-(t-Toff)/tau2))

if __name__ == '__main__':

    sz = 300

    x_mea = np.linspace(0, sz-1, sz)
    t = x_mea*0.01

    #p_ini = [3252.0, 0.35, 0.35, 0.0]
    p_ini = [3348.576741, 0.137321, 0.138420, 0.000001]

    for i in range(0,sz):
        _t = t[i]
        vl_mod = double_invexp (p_ini, _t)
        #if vl_mod<0: vl_mod=0
        print ("{:6.3f} {:6.1f}".format(_t,vl_mod))
