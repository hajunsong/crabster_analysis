import numpy as np
from Y_vector import Y2qdq, dqddq2Yp

def analysis(t_c, Y, base, sub):
    base, sub = Y2qdq(Y, base, sub)

    base.position_analysis()
    base.velocity_analysis()

    base.mass_force_analysis()

    for s in sub:
        s.position_analysis(base)
        s.velocity_analysis(base)

    for s in sub:
        s.mass_force_analysis()

    Yp = dqddq2Yp(base, sub)

    return Yp, base, sub