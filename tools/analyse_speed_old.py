import sys
from math import log
import numpy as np
import levmar

def double_invexp(p, t):
    Vmax  = p[0]
    tau1  = p[1]
    tau2  = p[2]
    Toff  = p[3]
    return Vmax * (1.0 - 2.0*np.exp(-(t-Toff)/tau1) + 1.0*np.exp(-(t-Toff)/tau2))

def invexp(p, t):
    Vmax  = p[0]
    tau   = p[1]
    Toff  = p[2]
    return Vmax * (1.0 - np.exp(-(t-Toff)/tau))

def invexp_x(p, x):
    return invexp(p, x*0.1)


if __name__ == '__main__':
    fd=open(sys.argv[1])

    t=[]
    pl=[]
    pr=[]
    for li in fd:
        tok=li.split()
        t.append(float(tok[0]))
        p=float(tok[4])
        pl.append(p)
        p=float(tok[5])
        pr.append(p)

    sz=len(t)

    vl=[]
    vr=[]
    vl.append(0.0)
    vr.append(0.0)
    for i in range(1,sz):
        vl.append(abs(pl[i]-pl[i-1]))
        vr.append(abs(pr[i]-pr[i-1]))

    #######################
    # Levenberg-Marquardt #
    #######################

    # Create input data
    x_mea = np.linspace(1, sz-1, sz-1)
    t_mea = np.empty(shape = (sz-1,), dtype = np.float_)
    vl_mea = np.empty(shape = (sz-1,), dtype = np.float_)
    vr_mea = np.empty(shape = (sz-1,), dtype = np.float_)
    t0 = t[0]
    for i in range (0,sz-1):
        t_mea[i] = t[i+1] - t0
        vl_mea[i] = vl[i+1]
        vr_mea[i] = vr[i+1]

    # Initial estimate
    p_ini = [3000.0, 0.35, 0.01]
    bc = [(1.0e-6, None), (1.0e-1, None), (None, None)]

    # Run the fitting routine - left side
    p_opt_l, p_cov_l, info_l = levmar.levmar_bc(invexp, p_ini, vl_mea, bc, args=(t_mea,))

    # Print the result - left side
    print("Estimate left:")
    print("  {0[0]:9f} {0[1]:9f} {0[2]:9f}".format(p_opt_l))
    print("")

    # Run the fitting routine - right side
    p_opt_r, p_cov_r, info_r = levmar.levmar_bc(invexp, p_ini, vr_mea, bc, args=(t_mea,))
    
    # Print the result - right side
    print("Estimate right:")
    print("  {0[0]:9f} {0[1]:9f} {0[2]:9f}".format(p_opt_r))
    print("")

    if (len(sys.argv)>2):
        wfd=open(sys.argv[2],"wt")
        for i in range(0,sz):
            _t = t[i]-t0
            vl_mod = invexp (p_opt_l, _t)
            if vl_mod<0: vl_mod=0
            vr_mod = invexp (p_opt_r, _t)
            if vr_mod<0: vr_mod=0
            wfd.write ("{:6.3f} {:6.1f} {:6.1f}\n".format(_t,vl_mod,vr_mod))
