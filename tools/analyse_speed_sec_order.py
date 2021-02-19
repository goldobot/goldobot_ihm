import sys
from math import log
import numpy as np
import levmar

def double_invexp_fsck(p, t):
    Vmax  = p[0]
    tau1  = p[1]
    tau2  = p[2]
    #Toff  = p[3]
    Toff  = 0.06
    if not hasattr(t,"__len__"):
        if (t<Toff):
            return 0
    if (tau1-tau2)<1.0e-12:
        exp_Toff_tau1 = 10686474581524.463
        if (Toff/tau1 < 30.0):
            exp_Toff_tau1 = np.exp(Toff/tau1)
        #val = Vmax * (1.0 - ((tau1+(t-Toff))/tau1)*np.exp(-(t-Toff)/tau1))
        val = Vmax * (1.0 - ((tau1+(t-Toff))/tau1)*np.exp(-(t)/tau1)*exp_Toff_tau1)
        return val
    else:
        val = 0.0
        delta_tau_inv = 1.0/(tau1-tau2)
        exp_Toff_tau1 = 10686474581524.463
        if (Toff/tau1 < 30.0):
            exp_Toff_tau1 = np.exp(Toff/tau1)
        exp_Toff_tau2 = 10686474581524.463
        if (Toff/tau2 < 30.0):
            exp_Toff_tau2 = np.exp(Toff/tau2)
        #val = Vmax * (1.0 - tau1*delta_tau_inv*np.exp(-(t-Toff)/tau1) + tau2*delta_tau_inv*np.exp(-(t-Toff)/tau2))
        val = Vmax * (1.0 - tau1*delta_tau_inv*np.exp(-(t)/tau1)*exp_Toff_tau1 + tau2*delta_tau_inv*np.exp(-(t-Toff)/tau2)*exp_Toff_tau2)
        #if hasattr(t,"__len__"):
        #    dump_log = False
        #    if (np.isnan(val).any()):
        #        print ("ISNAN!")
        #        dump_log = True
        #    if (np.isinf(val).any()):
        #        print ("ISINF!")
        #        dump_log = True
        #    if dump_log:
        #        print (" Vmax = {:f}".format(Vmax))
        #        print (" tau1 = {:f}".format(tau1))
        #        print (" tau2 = {:f}".format(tau2))
        #        print (" Toff = {:f}".format(Toff))
        #        print (" val : ", val)
        return val

def double_invexp(p, t):
    Vmax  = p[0]
    tau1  = p[1]
    tau2  = p[2]
    Toff  = Toff_ini
    if not hasattr(t,"__len__"):
        if (t<Toff):
            return 0
    if (tau1-tau2)<1.0e-12:
        val = Vmax * (1.0 - ((tau1+(t-Toff))/tau1)*np.exp(-(t-Toff)/tau1))
        return val
    else:
        delta_tau_inv = 1.0/(tau1-tau2)
        val = Vmax * (1.0 - tau1*delta_tau_inv*np.exp(-(t-Toff)/tau1) + tau2*delta_tau_inv*np.exp(-(t-Toff)/tau2))
        return val


if __name__ == '__main__':
    fd=open(sys.argv[4])

    t=[]
    vl=[]
    vr=[]
    for li in fd:
        tok=li.split()
        t.append(float(tok[0]))
        v=float(tok[6])
        if v<0: v=-v
        vl.append(v)
        v=float(tok[7])
        if v<0: v=-v
        vr.append(v)
    vl[0]=0.0
    vr[0]=0.0

    sz=len(t)

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

    lim_Toff = 0.1

    # LEFT SIDE
    # Initial estimate
    Vmax_ini = float(sys.argv[1])
    tau1_ini = float(sys.argv[2])
    #tau2_ini = float(sys.argv[2])
    tau2_ini = 0.01
    Toff_ini = float(sys.argv[3])
    #p_ini = [Vmax_ini, tau1_ini, tau2_ini, Toff_ini]
    #bc = [(1.0e-8, None), (1.0e-8, None), (1.0e-8, None), (1.0e-8, lim_Toff)]
    p_ini = [Vmax_ini, tau1_ini, tau2_ini]
    bc = [(1.0e-8, None), (1.0e-3, None), (1.0e-3, None)]

    # Run the fitting routine - left side
    p_opt_l, p_cov_l, info_l = levmar.levmar_bc(double_invexp, p_ini, vl_mea, bc, args=(t_mea,))

    # Print the result - left side
    print("Estimate left:")
    #print("  {0[0]:9f} {0[1]:9f} {0[2]:9f} {0[3]:9f}".format(p_opt_l))
    print("  {0[0]:9f} {0[1]:9f} {0[2]:9f}".format(p_opt_l))
    print("")

    # RIGHT SIDE
    # Initial estimate
    #p_ini = [Vmax_ini, tau1_ini, tau2_ini, Toff_ini]
    #bc = [(1.0e-8, None), (1.0e-8, None), (1.0e-8, None), (1.0e-8, lim_Toff)]
    p_ini = [Vmax_ini, tau1_ini, tau2_ini]
    bc = [(1.0e-8, None), (1.0e-3, None), (1.0e-3, None)]

    # Run the fitting routine - right side
    p_opt_r, p_cov_r, info_r = levmar.levmar_bc(double_invexp, p_ini, vr_mea, bc, args=(t_mea,))
    
    # Print the result - right side
    print("Estimate right:")
    #print("  {0[0]:9f} {0[1]:9f} {0[2]:9f} {0[3]:9f}".format(p_opt_r))
    print("  {0[0]:9f} {0[1]:9f} {0[2]:9f}".format(p_opt_r))
    print("")

    if (len(sys.argv)>5):
        wfd=open(sys.argv[5],"wt")
        for i in range(0,sz):
            _t = t[i]-t0
            vl_mod = double_invexp (p_opt_l, _t)
            if vl_mod<0: vl_mod=0
            vr_mod = double_invexp (p_opt_r, _t)
            if vr_mod<0: vr_mod=0
            wfd.write ("{:6.3f} {:6.1f} {:6.1f}\n".format(_t,vl_mod,vr_mod))
