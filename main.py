import numpy as np
from BodyClass import BodyData, SubSystem, BaseBody
from Y_vector import define_Y_vector
from Analysis import analysis
import Simulation as sim
import pandas as pd

if __name__ == "__main__":
    sim.t_c = 0
    sim.dt = 0.001
    sim.t_e = 2
    sim.step = 0

    sim.g = -9.80665

    sim.motion_flag = False

    L_q_init = np.array([np.pi/4, 0, 0, -np.pi*3/4], dtype=float)
    R_q_init = np.array([-np.pi/4, 0, 0, np.pi*3/4], dtype=float)

    base = BaseBody()
    FL = SubSystem("L", sijp=base.sijp_FL, Cij=base.Cij_FL)
    ML = SubSystem("L", sijp=base.sijp_ML, Cij=base.Cij_ML)
    RL = SubSystem("L", sijp=base.sijp_RL, Cij=base.Cij_RL)
    FR = SubSystem("R", sijp=base.sijp_FR, Cij=base.Cij_FR)
    MR = SubSystem("R", sijp=base.sijp_MR, Cij=base.Cij_MR)
    RR = SubSystem("R", sijp=base.sijp_RR, Cij=base.Cij_RR)
    sub = [FL, ML, RL, FR, MR, RR]

    sub[0].q_init = L_q_init
    sub[1].q_init = L_q_init
    sub[2].q_init = L_q_init
    sub[3].q_init = R_q_init
    sub[4].q_init = R_q_init
    sub[5].q_init = R_q_init

    Y = define_Y_vector(base, sub)

    log = []

    while sim.t_c <= sim.t_e:
        Yp, base, sub = analysis(sim.t_c, Y, base, sub)

        log.append(np.hstack([
            sim.step, sim.t_c,
            sub[0].q, 0, 0, sub[0].dq, 0, 0, sub[0].ddq, 0, 0, sub[0].body[3].re*1000, sub[0].body[3].rpy,
            sub[1].q, 0, 0, sub[1].dq, 0, 0, sub[1].ddq, 0, 0, sub[1].body[3].re*1000, sub[1].body[3].rpy,
            sub[2].q, 0, 0, sub[2].dq, 0, 0, sub[2].ddq, 0, 0, sub[2].body[3].re*1000, sub[2].body[3].rpy,
            sub[3].q, 0, 0, sub[3].dq, 0, 0, sub[3].ddq, 0, 0, sub[3].body[3].re*1000, sub[3].body[3].rpy,
            sub[4].q, 0, 0, sub[4].dq, 0, 0, sub[4].ddq, 0, 0, sub[4].body[3].re*1000, sub[4].body[3].rpy,
            sub[5].q, 0, 0, sub[5].dq, 0, 0, sub[5].ddq, 0, 0, sub[5].body[3].re*1000, sub[5].body[3].rpy,
        ]))

        print(f"t_c : {sim.t_c}")

        sim.t_c += sim.dt
        sim.step += 1

    log = np.asarray(log, dtype=float)
    out_csv = "sim_data.csv"
    pd.DataFrame(log).to_csv(out_csv, index=False, header=False)

    print(f"[OK] saved: {out_csv}  shape={log.shape}")