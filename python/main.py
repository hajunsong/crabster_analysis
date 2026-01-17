import numpy as np
import pandas as pd
from sim import *
from analysis import *

if __name__ == '__main__':
    global FL, ML, RL, FR, MR, RR
    t_c = 0
    dt = 0.001
    t_e = 2
    step = 0

    L_q_init = np.array([ np.pi / 4.0, 0, 0, -np.pi * 3 / 4.0], dtype=np.float64)
    R_q_init = np.array([-np.pi / 4.0, 0, 0,  np.pi * 3 / 4.0], dtype=np.float64)

    FL.q_init = L_q_init.copy()
    ML.q_init = L_q_init.copy()
    RL.q_init = L_q_init.copy()
    FR.q_init = R_q_init.copy()
    MR.q_init = R_q_init.copy()
    RR.q_init = R_q_init.copy()

    Y = np.zeros(61, dtype=np.float64)
    Y[0:13] = np.concatenate([r0, p0, dr0, w0])
    Y[13:21] = np.concatenate([FL.q_init, FL.dq])
    Y[21:29] = np.concatenate([ML.q_init, ML.dq])
    Y[29:37] = np.concatenate([RL.q_init, RL.dq])
    Y[37:45] = np.concatenate([FR.q_init, FR.dq])
    Y[45:53] = np.concatenate([MR.q_init, MR.dq])
    Y[53:61] = np.concatenate([RR.q_init, RR.dq])

    log = []

    while t_c <= t_e:
        Yp = analysis(Y)

        k1 = Yp.copy()
        y2 = Y + (dt / 2.0) * k1
        k2 = analysis(y2)
        y3 = Y + (dt / 2.0) * k2
        k3 = analysis(y3)
        y4 = Y + dt * k3
        k4 = analysis(y4)
        Y_next = Y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t_next = t_c + dt

        log.append(np.hstack([
            step, t_c,
            FL.q, 0, 0, FL.dq, 0, 0, FL.ddq, 0, 0, FL.re * 1000, FL.rpy,
            ML.q, 0, 0, ML.dq, 0, 0, ML.ddq, 0, 0, ML.re * 1000, ML.rpy,
            RL.q, 0, 0, RL.dq, 0, 0, RL.ddq, 0, 0, RL.re * 1000, RL.rpy,
            FR.q, 0, 0, FR.dq, 0, 0, FR.ddq, 0, 0, FR.re * 1000, FR.rpy,
            MR.q, 0, 0, MR.dq, 0, 0, MR.ddq, 0, 0, MR.re * 1000, MR.rpy,
            RR.q, 0, 0, RR.dq, 0, 0, RR.ddq, 0, 0, RR.re * 1000, RR.rpy,
        ]))

        print(f"t_c : {t_c}")

        t_c = t_next
        step += 1
        Y = Y_next.copy()

    log = np.asarray(log, dtype=float)
    out_csv = "sim_data.csv"
    pd.DataFrame(log).to_csv(out_csv, index=False, header=False)

    print(f"[OK] saved: {out_csv}  shape={log.shape}")

    import subprocess
    subprocess.run(["python", "result_plot.py"], check=True)