import numpy as np
from utils import *
from body import subsystem
import read_FR

class MR(subsystem):
    def __init__(self):
        super().__init__()
        FR = read_FR.FR()
        self.q = np.zeros(4, dtype=np.float64)
        self.dq = np.zeros(4, dtype=np.float64)
        self.ddq = np.zeros(4, dtype=np.float64)

        self.m1 = FR.m1
        self.J1p = FR.J1p.copy()
        self.rho1p = FR.rho1p.copy()
        self.C11 = FR.C11.copy()
        self.u_vec1 = FR.u_vec1.copy()

        self.s12p = FR.s12p.copy()
        self.C12 = FR.C12.copy()

        self.m2 = FR.m2
        self.J2p = FR.J2p.copy()
        self.rho2p = FR.rho2p.copy()
        self.C22 = FR.C22.copy()
        self.u_vec2 = FR.u_vec2.copy()

        self.s23p = FR.s23p.copy()
        self.C23 = FR.C23.copy()

        self.m3 = FR.m3
        self.J3p = FR.J3p.copy()
        self.rho3p = FR.rho3p.copy()
        self.C33 = FR.C33.copy()
        self.u_vec3 = FR.u_vec3.copy()

        self.s34p = FR.s34p.copy()
        self.C34 = FR.C34.copy()

        self.m4 = FR.m4
        self.J4p = FR.J4p.copy()
        self.rho4p = FR.rho4p.copy()
        self.C44 = FR.C44.copy()
        self.u_vec4 = FR.u_vec4.copy()

        self.s4ep = FR.s4ep.copy()
        self.C4e = FR.C4e.copy()
