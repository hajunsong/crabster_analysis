import numpy as np
from utils import *
from body import subsystem

class FR(subsystem):
    def __init__(self):
        super().__init__()
        self.q = np.zeros(4, dtype=np.float64)
        self.q_init = np.zeros(4, dtype=np.float64)
        self.dq = np.zeros(4, dtype=np.float64)
        self.ddq = np.zeros(4, dtype=np.float64)

        self.m1 = 3.6
        self.J1p = np.array([
            [24217.36, 1.142, 4.718],
            [1.142, 22602.121, -3.656],
            [4.718, -3.656, 24383.284]], dtype=np.float64) * 1e-6
        self.rho1p = np.array([-19.41, 0, 0], dtype=np.float64) * 1e-3
        self.C11 = euler_zxz(np.pi, np.pi / 2.0, np.pi / 2.0)
        self.u_vec1 = np.array([0, 0, 1], dtype=np.float64)

        self.s12p = np.array([-120, 0, 0], dtype=np.float64) * 1e-3
        self.C12 = euler_zxz(-np.pi / 2.0, np.pi / 2.0, np.pi / 2.0)

        self.m2 = 12.9
        self.J2p = np.array([
            [101693.397, 54.639, 3.734],
            [54.639, 43784.882, -3156.796],
            [3.734, -3156.796, 101586.518]], dtype=np.float64) * 1e-6
        self.rho2p = np.array([0, 0, 101.13], dtype=np.float64) * 1e-3
        self.C22 = euler_zxz(np.pi, np.pi / 2.0, np.pi)
        self.u_vec2 = np.array([0, 0, 1], dtype=np.float64)

        self.s23p = np.array([0, 0, 121], dtype=np.float64) * 1e-3
        self.C23 = euler_zxz(np.pi, np.pi / 2.0, np.pi)

        self.m3 = 11.1
        self.J3p = np.array([
            [172022.706, 939.804, -39.970],
            [939.804, 67557.291, -151.395],
            [-39.970, -151.395, 155965.608]], dtype=np.float64) * 1e-6
        self.rho3p = np.array([0, -238.39, -1.08], dtype=np.float64) * 1e-3
        self.C33 = euler_zxz(0.0, 0.0, 0.0)
        self.u_vec3 = np.array([0, 0, 1], dtype=np.float64)

        self.s34p = np.array([0, -509, 0], dtype=np.float64) * 1e-3
        self.C34 = euler_zxz(np.pi / 2, np.pi / 2, 0)

        self.m4 = 11.5
        self.J4p = np.array([
            [686629.019, 10499.954, -1652.691],
            [10499.954, 44753.249, 23952.157],
            [-1652.691, 23952.157, 705784.865]], dtype=np.float64) * 1e-6
        self.rho4p = np.array([-322.25, 51.84, 0], dtype=np.float64) * 1e-3
        self.C44 = euler_zxz(np.pi, np.pi / 2.0, np.pi / 2.0)
        self.u_vec4 = np.array([0, 0, 1], dtype=np.float64)

        self.s4ep = np.array([-823.56, 0, 0], dtype=np.float64) * 1e-3
        self.C4e = euler_zxz(np.pi, np.pi / 2.0, np.pi / 2.0)