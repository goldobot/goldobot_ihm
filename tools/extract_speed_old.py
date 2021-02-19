import sys

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

    #t0l=(t[1]*vl[2]-t[2]*vl[1])/(vl[2]-vl[1])
    #t0r=(t[1]*vr[2]-t[2]*vr[1])/(vr[2]-vr[1])
    #print("t0l={}".format(t0l))
    #print("t0r={}".format(t0r))

    #t0 = (t0l + t0r)/2
    t0 = t[0]

    for i in range(0,sz):
        print ("{:6.3f} {:6.1f} {:6.1f}".format(t[i]-t0,vl[i],vr[i]))

