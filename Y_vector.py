import numpy as np

def define_Y_vector(base, sub):
    Y = np.zeros(61, dtype=float)

    Y[0:3] = base.ri
    Y[3:7] = base.pi
    Y[7:10] = base.dri
    Y[10:13] = base.wi

    indx = 13
    for s in sub:
        Y[indx:indx+4] = s.q_init
        Y[indx+4:indx+8] = s.dq
        indx += 8

    return Y

def Y2qdq(Y, base, sub):
    base.ri = Y[0:3]
    base.pi = Y[3:7]
    base.dri = Y[7:10]
    base.dwi = Y[10:13]

    indx = 13
    for s in sub:
        s.q = Y[indx:indx+4]
        s.dq = Y[indx+4:indx+8]
        indx += 8

    return base, sub

def dqddq2Yp(base, sub):
    Yp = np.zeros(61, dtype=float)

    Yp[0:3] = base.dri
    Yp[3:7] = base.dpi
    Yp[7:10] = base.ddri
    Yp[10:13] = base.dwi

    indx = 13
    for s in sub:
        Yp[indx:indx+4] = s.dq
        Yp[indx+4:indx+8] = s.ddq
        indx += 8

    return Yp