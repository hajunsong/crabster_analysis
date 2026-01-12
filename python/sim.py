import read_FL
import read_ML
import read_RL
import read_FR
import read_MR
import read_RR
from read_base import *

global t_c, dt, t_e, step, g
global L_q_init, R_q_init, K_RSDA, C_RSDA

t_c = 0
dt = 0
t_e = 0
step = 0

g = -9.80665

FL = read_FL.FL()
ML = read_ML.ML()
RL = read_RL.RL()
FR = read_FR.FR()
MR = read_MR.MR()
RR = read_RR.RR()

K_RSDA = np.array([15000000, 7000000, 7000000, 7000000], dtype=np.float64)*0.001
C_RSDA = np.array([1500000, 300000, 300000, 700000], dtype=np.float64)*0.001