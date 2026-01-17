import numpy as np
from utils import *
from body import subsystem
import read_FL

class ML(subsystem):
    def __init__(self):
        super().__init__()
        FL = read_FL.FL()
        self.q = np.zeros(4, dtype=np.float64)
        self.dq = np.zeros(4, dtype=np.float64)
        self.ddq = np.zeros(4, dtype=np.float64)

        self.m1 = FL.m1
        self.J1p = FL.J1p.copy()
        self.rho1p = FL.rho1p.copy()
        self.C11 = FL.C11.copy()
        self.u_vec1 = FL.u_vec1.copy()

        self.s12p = FL.s12p.copy()
        self.C12 = FL.C12.copy()

        self.m2 = FL.m2
        self.J2p = FL.J2p.copy()
        self.rho2p = FL.rho2p.copy()
        self.C22 = FL.C22.copy()
        self.u_vec2 = FL.u_vec2.copy()

        self.s23p = FL.s23p.copy()
        self.C23 = FL.C23.copy()

        self.m3 = FL.m3
        self.J3p = FL.J3p.copy()
        self.rho3p = FL.rho3p.copy()
        self.C33 = FL.C33.copy()
        self.u_vec3 = FL.u_vec3.copy()

        self.s34p = FL.s34p.copy()
        self.C34 = FL.C34.copy()

        self.m4 = FL.m4
        self.J4p = FL.J4p.copy()
        self.rho4p = FL.rho4p.copy()
        self.C44 = FL.C44.copy()
        self.u_vec4 = FL.u_vec4.copy()

        self.s4ep = FL.s4ep.copy()
        self.C4e = FL.C4e.copy()
