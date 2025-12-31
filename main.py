import read_base as base
import read_FL as FL
import read_ML as ML
import read_RL as RL
import read_FR as FR
import read_MR as MR
import read_RR as RR
from analysis import analysis
from Y_vector import define_Y_vector
import sim_info as sim

import numpy as np

def main():

    sim.t_c = 0
    sim.dt = 0.001
    sim.t_e = 2
    sim.g = -9.80665
    sim.step = 0
    sim.motion_flag = 0

    L_q_init = [np.pi/4, 0, 0, -np.pi*3/4]
    R_q_init = [-np.pi/4, 0, 0, np.pi*3/4]

    for i in range(0, 4):
        FL.body[i].qi_init = L_q_init[i]
        ML.body[i].qi_init = L_q_init[i]
        RL.body[i].qi_init = L_q_init[i]
        FR.body[i].qi_init = R_q_init[i]
        MR.body[i].qi_init = R_q_init[i]
        RR.body[i].qi_init = R_q_init[i]

    Y = define_Y_vector()

    # while sim.t_c <= sim.t_e:
    Yp = analysis(sim.t_c, Y)



if __name__ == '__main__':
    main()