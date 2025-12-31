import read_base as base
import read_FL as FL
import read_ML as ML
import read_RL as RL
import read_FR as FR
import read_MR as MR
import read_RR as RR

import numpy as np

def define_Y_vector():
    Y = np.zeros(61, dtype=float)
    
    Y[0:3] = base.ri
    Y[3:7] = base.pi
    Y[7:10] = base.dri
    Y[10:13] = base.dwi

    Y[13:17] = [FL.body[0].qi_init, FL.body[1].qi_init, FL.body[2].qi_init, FL.body[3].qi_init]
    Y[17:21] = [FL.body[0].dqi, FL.body[1].dqi, FL.body[2].dqi, FL.body[3].dqi]

    Y[21:25] = [ML.body[0].qi_init, ML.body[1].qi_init, ML.body[2].qi_init, ML.body[3].qi_init]
    Y[25:29] = [ML.body[0].dqi, ML.body[1].dqi, ML.body[2].dqi, ML.body[3].dqi]

    Y[29:33] = [RL.body[0].qi_init, RL.body[1].qi_init, RL.body[2].qi_init, RL.body[3].qi_init]
    Y[33:37] = [RL.body[0].dqi, RL.body[1].dqi, RL.body[2].dqi, RL.body[3].dqi]

    Y[37:41] = [FR.body[0].qi_init, FR.body[1].qi_init, FR.body[2].qi_init, FR.body[3].qi_init]
    Y[41:45] = [FR.body[0].dqi, FR.body[1].dqi, FR.body[2].dqi, FR.body[3].dqi]

    Y[45:49] = [MR.body[0].qi_init, MR.body[1].qi_init, MR.body[2].qi_init, MR.body[3].qi_init]
    Y[49:53] = [MR.body[0].dqi, MR.body[1].dqi, MR.body[2].dqi, MR.body[3].dqi]

    Y[53:57] = [RR.body[0].qi_init, RR.body[1].qi_init, RR.body[2].qi_init, RR.body[3].qi_init]
    Y[57:61] = [RR.body[0].dqi, RR.body[1].dqi, RR.body[2].dqi, RR.body[3].dqi]

    return Y

def Y2qdq(Y):
    base.ri = Y[0:3]
    base.pi = Y[3:7]
    base.dri = Y[7:10]
    base.dwi = Y[10:13]

    FL.body[0].qi, FL.body[1].qi, FL.body[2].qi, FL.body[3].qi = Y[13:17]
    FL.body[0].dqi, FL.body[1].dqi, FL.body[2].dqi, FL.body[3].dqi = Y[17:21]

    ML.body[0].qi, ML.body[1].qi, ML.body[2].qi, ML.body[3].qi = Y[21:25]
    ML.body[0].dqi, ML.body[1].dqi, ML.body[2].dqi, ML.body[3].dqi = Y[25:29]

    RL.body[0].qi, RL.body[1].qi, RL.body[2].qi, RL.body[3].qi = Y[29:33]
    RL.body[0].dqi, RL.body[1].dqi, RL.body[2].dqi, RL.body[3].dqi = Y[33:37]

    FR.body[0].qi, FR.body[1].qi, FR.body[2].qi, FR.body[3].qi = Y[37:41]
    FR.body[0].dqi, FR.body[1].dqi, FR.body[2].dqi, FR.body[3].dqi = Y[41:45]

    MR.body[0].qi, MR.body[1].qi, MR.body[2].qi, MR.body[3].qi = Y[45:49]
    MR.body[0].dqi, MR.body[1].dqi, MR.body[2].dqi, MR.body[3].dqi = Y[49:53]

    RR.body[0].qi, RR.body[1].qi, RR.body[2].qi, RR.body[3].qi = Y[53:57]
    RR.body[0].dqi, RR.body[1].dqi, RR.body[2].dqi, RR.body[3].dqi = Y[57:61]

def dqddq2Yp():
    Yp = np.zeros(61, dtype=float)

    Yp[0:3] = base.ri
    Yp[3:7] = base.pi
    Yp[7:10] = base.dri
    Yp[10:13] = base.dwi

    Yp[13:17] = [FL.body[0].dqi, FL.body[1].dqi, FL.body[2].dqi, FL.body[3].dqi]
    Yp[17:21] = [FL.body[0].ddqi, FL.body[1].ddqi, FL.body[2].ddqi, FL.body[3].ddqi]

    Yp[21:25] = [ML.body[0].dqi, ML.body[1].dqi, ML.body[2].dqi, ML.body[3].dqi]
    Yp[25:29] = [ML.body[0].ddqi, ML.body[1].ddqi, ML.body[2].ddqi, ML.body[3].ddqi]

    Yp[29:33] = [RL.body[0].dqi, RL.body[1].dqi, RL.body[2].dqi, RL.body[3].dqi]
    Yp[33:37] = [RL.body[0].ddqi, RL.body[1].ddqi, RL.body[2].ddqi, RL.body[3].ddqi]

    Yp[37:41] = [FR.body[0].dqi, FR.body[1].dqi, FR.body[2].dqi, FR.body[3].dqi]
    Yp[41:45] = [FR.body[0].ddqi, FR.body[1].ddqi, FR.body[2].ddqi, FR.body[3].ddqi]

    Yp[45:49] = [MR.body[0].dqi, MR.body[1].dqi, MR.body[2].dqi, MR.body[3].dqi]
    Yp[49:53] = [MR.body[0].ddqi, MR.body[1].ddqi, MR.body[2].ddqi, MR.body[3].ddqi]

    Yp[53:57] = [RR.body[0].dqi, RR.body[1].dqi, RR.body[2].dqi, RR.body[3].dqi]
    Yp[57:61] = [RR.body[0].ddqi, RR.body[1].ddqi, RR.body[2].ddqi, RR.body[3].ddqi]

    return Yp