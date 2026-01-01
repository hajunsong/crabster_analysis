from data_con import *
from utils import *

def read_L_body1(sijp, Cij):
    body = Body()
    body.sijp = np.asarray(sijp, float).reshape(3)
    body.Cij = np.asarray(Cij, float).reshape(3,3)
    body.mi = 3.6
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 24217.363, 1.142, 22602.121, 3.656, 24383.284, -4.718
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([19.41,0,0], dtype=float)*1e-3
    body.Cii = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    return body

def read_L_body2():
    body = Body()
    body.sijp = np.array([120,0,0], dtype=float)*1e-3
    body.Cij = ang2mat(-np.pi/2, np.pi/2, np.pi/2)
    body.mi = 12.9
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 101693.397, -54.639, 43784.882, 3156.796, 101586.518, -3.734
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([0,0,-101.13], dtype=float)*1e-3
    body.Cii = np.array([[1,0,0],[0,0,1],[0,-1,0]], dtype=float)
    return body

def read_L_body3():
    body = Body()
    body.sijp = np.array([0,0,-121], dtype=float)*1e-3
    body.Cij = ang2mat(np.pi, np.pi/2, np.pi)
    body.mi = 11.1
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 172022.706, 939.804, 67557.291, 151.395, 155965.608, 39.970
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([0,238.39,-1.08], dtype=float)*1e-3
    body.Cii = np.eye(3)
    return body

def read_L_body4():
    body = Body()
    body.sijp = np.array([0,509,0], dtype=float)*1e-3
    body.Cij = ang2mat(np.pi/2, np.pi/2, 0)
    body.mi = 11.5
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 686629.019, 10499.954, 44753.249, -23952.157, 705784.865, 1652.691
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([322.25,51.84,0], dtype=float)*1e-3
    body.Cii = ang2mat(np.pi, np.pi/2, np.pi/2)
    body.sep = np.array([823.56,0,0], dtype=float)*1e-3
    body.Ce = ang2mat(np.pi, np.pi/2, np.pi/2)
    return body

def read_R_body1(sijp, Cij):
    body = Body()
    body.sijp = np.asarray(sijp, float).reshape(3)
    body.Cij = np.asarray(Cij, float).reshape(3,3)
    body.mi = 3.6
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 24217.363, 1.142, 22602.121, -3.656, 24383.284, 4.718
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([-19.41,0,0], dtype=float)*1e-3
    body.Cii = ang2mat(np.pi, np.pi/2, np.pi/2)
    return body

def read_R_body2():
    body = Body()
    body.sijp = np.array([-120,0,0], dtype=float)*1e-3
    body.Cij = ang2mat(-np.pi/2, np.pi/2, np.pi/2)
    body.mi = 12.9
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 101693.397, 54.639, 43784.882, -3156.796, 101586.518, 3.734
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([0,0,101.13], dtype=float)*1e-3
    body.Cii = ang2mat(np.pi, np.pi/2, np.pi)
    return body

def read_R_body3():
    body = Body()
    body.sijp = np.array([0,0,121], dtype=float)*1e-3
    body.Cij = ang2mat(np.pi, np.pi/2, np.pi)
    body.mi = 11.1
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 172022.706, 939.804, 67557.291, -151.395, 155965.608, -39.970
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([0,-238.39,-1.08], dtype=float)*1e-3
    body.Cii = np.eye(3)
    return body

def read_R_body4():
    body = Body()
    body.sijp = np.array([0,-509,0], dtype=float)*1e-3
    body.Cij = ang2mat(np.pi/2, np.pi/2, 0)
    body.mi = 11.5
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 686629.019, 10499.954, 44753.249, 23952.157, 705784.865, -1652.691
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([-322.25,51.84,0], dtype=float)*1e-3
    body.Cii = ang2mat(np.pi, np.pi/2, np.pi/2)
    body.sep = np.array([-823.56,0,0], dtype=float)*1e-3
    body.Ce = ang2mat(np.pi, np.pi/2, np.pi/2)
    return body
