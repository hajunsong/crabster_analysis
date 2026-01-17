import numpy as np
from utils import *

global r0, A0, p0, dr0, w0, m0, J0p, rho0p, C00
global s01p_FL, C01_FL, s01p_ML, C01_ML, s01p_RL, C01_RL
global s01p_FR, C01_FR, s01p_MR, C01_MR, s01p_RR, C01_RR

r0 = np.zeros(3, dtype=np.float64)
A0 = np.eye(3, dtype=np.float64)
p0 = np.array([1, 0, 0, 0], dtype=np.float64)

dr0 = np.zeros(3, dtype=np.float64)
w0 = np.zeros(3, dtype=np.float64)
w0t = np.zeros((3,3), dtype=np.float64)

m0 = 582.59
Ixx = 156890393.0;  Ixy = 0
Iyy = 150169673.0;  Iyz = 0
Izz = 249303699.0;  Izx = 0
J0p = np.array([
    [156890393.0, 0.0, 0.0],
    [0.0, 150169673.0, 0.0],
    [0.0, 0.0, 249303699.0]], dtype=np.float64)*1e-6

rho0p = np.zeros(3, dtype=np.float64)
C00 = euler_zxz(0, 0, 0)

FL_s01p = np.array([520, 758, 0], dtype=np.float64)*1e-3
FL_C01 = euler_zxz(np.pi/2.0, np.pi/2.0, 0.0)
ML_s01p = np.array([0, 858, 0], dtype=np.float64)*1e-3
ML_C01 = euler_zxz(np.pi/2.0, np.pi/2.0, 0.0)
RL_s01p = np.array([-520, 758, 0], dtype=np.float64)*1e-3
RL_C01 = euler_zxz(np.pi/2.0, np.pi/2.0, 0.0)
FR_s01p = np.array([520, -758, 0], dtype=np.float64)*1e-3
FR_C01 = euler_zxz(np.pi/2.0, np.pi/2.0, 0.0)
MR_s01p = np.array([0, -858, 0], dtype=np.float64)*1e-3
MR_C01 = euler_zxz(np.pi/2.0, np.pi/2.0, 0.0)
RR_s01p = np.array([-520, -758, 0], dtype=np.float64)*1e-3
RR_C01 = euler_zxz(np.pi/2.0, np.pi/2.0, 0.0)

Y0h = np.zeros(6, dtype=np.float64)
dY0h = np.zeros(6, dtype=np.float64)
dY0b = np.zeros(6, dtype=np.float64)
