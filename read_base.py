import numpy as np
from utils import *
import sim_info as sim

# joint states
qi: float = 0.0
dqi: float = 0.0
ddqi: float = 0.0

# pose
ri: np.ndarray = np.zeros(3)
pi: np.ndarray = np.array([1,0,0,0])
Ai: np.ndarray = np.eye(3)
Ei: np.ndarray = np.zeros((3,4))
Gi: np.ndarray = np.zeros((3,4))
rpy: np.ndarray = np.zeros(3)

dri: np.ndarray = np.zeros(3)
wi: np.ndarray = np.zeros(3)

# params
mi: float = 582.59
Ixx, Ixy, Iyy, Iyz, Izz, Izx = 156890393.0, 0.0, 150169673.0, 0.0, 249303699.0, 0.0
Jip = np.array([[Ixx, Ixy, Izx],
                        [Ixy, Iyy, Iyz],
                        [Izx, Iyz, Izz]], dtype=float)*1e-6
rhoip: np.ndarray = np.zeros(3)
Cii: np.ndarray = np.eye(3)

# parent-child kinematic params
sijp: np.ndarray = np.zeros(3)
Cij: np.ndarray = np.eye(3)

# derived: COM
rhoi: np.ndarray = np.zeros(3)
ric: np.ndarray = np.zeros(3)

wit: np.ndarray = np.zeros((3,3))
rit: np.ndarray = np.zeros((3,3))
drit: np.ndarray = np.zeros((3,3))

Yih: np.ndarray = np.zeros(6)

fic: np.ndarray = np.zeros(3)
tic: np.ndarray = np.zeros(3)

Mih: np.ndarray = np.zeros((6,6))
Qih: np.ndarray = np.zeros(6)
Ki: np.ndarray = np.zeros((6,6))
Li: np.ndarray = np.zeros(6)

ddri: np.ndarray = np.zeros(3)
dwi: np.ndarray = np.zeros(3)
ddric: np.ndarray = np.zeros(3)

sijp_FL = np.array([520, 758, 0], dtype=float)*1e-3
sijp_ML = np.array([0, 858, 0], dtype=float)*1e-3
sijp_RL = np.array([-520, 758, 0], dtype=float)*1e-3
sijp_FR = np.array([520, -758, 0], dtype=float)*1e-3
sijp_MR = np.array([0, -858, 0], dtype=float)*1e-3
sijp_RR = np.array([-520, -758, 0], dtype=float)*1e-3

Cij_FL = ang2mat(np.pi/2, np.pi/2, 0)
Cij_ML = ang2mat(np.pi/2, np.pi/2, 0)
Cij_RL = ang2mat(np.pi/2, np.pi/2, 0)
Cij_FR = ang2mat(np.pi/2, np.pi/2, 0)
Cij_MR = ang2mat(np.pi/2, np.pi/2, 0)
Cij_RR = ang2mat(np.pi/2, np.pi/2, 0)

def position_analysis():
    global pi, Ei, Gi, Ai, rpy, rhoip, ric, rit, rict

    pi = pi/np.linalg.norm(pi)
    q0 = pi[0]
    qv = pi[1:4]
    Ei = np.column_stack((qv, skew(qv) + q0*np.eye(3)))
    Gi = np.column_stack((qv, -skew(qv) + q0*np.eye(3)))
    Ai = Ei@np.transpose(Gi)
    rpy = mat2rpy(Ai)

    rhoi = Ai@rhoip
    ric = ri + rhoi
    rit = skew(ri)
    rict = skew(ric)


def velocity_analysis():
    global Jic, wit, dric, drit, drict

    Ai_Cii = Ai*Cii
    Jic = Ai_Cii*Jip*np.transpose(Ai_Cii)
    wit = skew(wi)

    dric = dri + wit@rhoi
    drit = skew(dri)
    drict = skew(dric)
    
    Yih[0:3] = dri + drit@wi
    Yih[3:6] = wi


def mass_force_analysis():
    global fic, tic, Mih, Qih
    
    fic = np.zeros(3)
    fic[2] = mi*sim.g
    tic = np.zeros(3)

    Mih[0:3, 0:3] = mi*np.eye(3)
    Mih[0:3, 3:6] = -mi*rict
    Mih[3:6, 0:3] = mi*rict
    Mih[3:6, 3:6] = Jic - mi*rict@rict

    Qih[0:3] = fic + mi*drict@wi
    Qih[3:6] = tic + rict@fic + mi*rict@drict@wi - wit@Jic@wi
