import read_base as base
import read_FL as FL
import read_ML as ML
import read_RL as RL
import read_FR as FR
import read_MR as MR
import read_RR as RR
from Y_vector import Y2qdq, dqddq2Yp
import sim_info as sim
from sub_analysis import sub_position_analysis, sub_velocity_analysis, sub_mass_force_analysis

import numpy as np

def analysis(t_c, Y):
    global FL, ML, RL, FR, MR, RR

    Y2qdq(Y)

    base.position_analysis()
    base.velocity_analysis()

    base.mass_force_analysis()

    FL = sub_position_analysis(FL)
    ML = sub_position_analysis(ML)
    RL = sub_position_analysis(RL)
    FR = sub_position_analysis(FR)
    MR = sub_position_analysis(MR)
    RR = sub_position_analysis(RR)

    FL = sub_velocity_analysis(FL)
    ML = sub_velocity_analysis(ML)
    RL = sub_velocity_analysis(RL)
    FR = sub_velocity_analysis(FR)
    MR = sub_velocity_analysis(MR)
    RR = sub_velocity_analysis(RR)

    FL = sub_mass_force_analysis(FL)
    print(FL.M)

    Yp = dqddq2Yp()