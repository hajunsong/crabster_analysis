import numpy as np

def skew(v):
    vx, vy, vz = v
    return np.array([
        [0.0, -vz, vy],
        [vz, 0.0, -vx],
        [-vy, vx, 0.0]
    ], dtype=np.float64)

def euler_zxz(psi, theta, phi):

    mat_psi = np.array([[np.cos(psi), -np.sin(psi), 0], [np.sin(psi), np.cos(psi), 0], [0, 0, 1]])
    mat_theta = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)],  [0, np.sin(theta), np.cos(theta)]])
    mat_phi = np.array([[np.cos(phi), -np.sin(phi), 0], [np.sin(phi), np.cos(phi), 0], [0, 0, 1]])

    return mat_psi @ mat_theta @ mat_phi

def mat2rpy(mat):
    mat = np.asarray(mat, dtype=np.float64).reshape(3, 3)

    pitch = -np.asin(mat[2, 0])
    roll = np.atan2(mat[2, 1], mat[2,2])
    yaw = np.atan2(mat[1, 0], mat[0, 0])

    rpy = np.array([roll, pitch, yaw], dtype=np.float64)
    return rpy