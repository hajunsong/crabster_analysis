import read_base as base
import read_FL as FL
import read_ML as ML
import read_RL as RL
import read_FR as FR
import read_MR as MR
import read_RR as RR
from Y_vector import Y2qdq, dqddq2Yp
import sim_info as sim
from subsystem_analysis import sub_position_analysis, sub_velocity_analysis, sub_mass_force_analysis

import numpy as np

def analysis(t_c, Y):
    global FL, ML, RL, FR, MR, RR

    Y2qdq(Y)

    base.position_analysis()
    base.velocity_analysis()

    base.mass_force_analysis()

    FL.body = sub_position_analysis(FL.body)
    ML.body = sub_position_analysis(ML.body)
    RL.body = sub_position_analysis(RL.body)
    FR.body = sub_position_analysis(FR.body)
    MR.body = sub_position_analysis(MR.body)
    RR.body = sub_position_analysis(RR.body)

    FL.body = sub_velocity_analysis(FL.body)
    ML.body = sub_velocity_analysis(ML.body)
    RL.body = sub_velocity_analysis(RL.body)
    FR.body = sub_velocity_analysis(FR.body)
    MR.body = sub_velocity_analysis(MR.body)
    RR.body = sub_velocity_analysis(RR.body)

    FL.body = sub_mass_force_analysis(FL.body)

    Yp = dqddq2Yp()