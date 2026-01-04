import numpy as np
from dataclasses import dataclass, field
from Utils import euler_zxz, skew, mat2rpy
import Simulation as sim
from typing import Literal

@dataclass
class BodyData:
    ri: np.ndarray = field(default_factory=lambda: np.zeros(3))
    pi: np.ndarray = field(default_factory=lambda: np.array([1, 0, 0, 0]))
    Ai: np.ndarray = field(default_factory=lambda: np.eye(3))
    rpy: np.ndarray = field(default_factory=lambda: np.zeros(3))

    dri: np.ndarray = field(default_factory=lambda: np.zeros(3))
    wi: np.ndarray = field(default_factory=lambda: np.zeros(3))

    mi: float = 1.0
    Jip: np.ndarray = field(default_factory=lambda: np.eye(3))
    rhoip: np.ndarray = field(default_factory=lambda: np.zeros(3))
    Cii: np.ndarray = field(default_factory=lambda: np.eye(3))

    sijp: np.ndarray = field(default_factory=lambda: np.zeros(3))
    Cij: np.ndarray = field(default_factory=lambda: np.eye(3))
    sij: np.ndarray = field(default_factory=lambda: np.zeros(3))

    rhoi: np.ndarray = field(default_factory=lambda: np.zeros(3))
    ric: np.ndarray = field(default_factory=lambda: np.zeros(3))
    rict: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))

    Aijpp: np.ndarray = field(default_factory=lambda: np.eye(3))
    u_vec: np.ndarray = field(default_factory=lambda: np.array([0, 0, 1]))
    Hi: np.ndarray = field(default_factory=lambda: np.zeros(3))
    dHi: np.ndarray = field(default_factory=lambda: np.zeros(3))
    Di: np.ndarray = field(default_factory=lambda: np.zeros(6))
    Bi: np.ndarray = field(default_factory=lambda: np.zeros(6))

    wit: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))
    rit: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))
    drit: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))
    dric: np.ndarray = field(default_factory=lambda: np.zeros(3))
    drict: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))

    Jic: np.ndarray = field(default_factory=lambda: np.eye(3))

    fic: np.ndarray = field(default_factory=lambda: np.zeros(3))
    tic: np.ndarray = field(default_factory=lambda: np.zeros(3))

    Mih: np.ndarray = field(default_factory=lambda: np.zeros((6, 6)))
    Qih: np.ndarray = field(default_factory=lambda: np.zeros(6))
    Ki: np.ndarray = field(default_factory=lambda: np.zeros((6, 6)))
    Li: np.ndarray = field(default_factory=lambda: np.zeros(6))

    ddri: np.ndarray = field(default_factory=lambda: np.zeros(3))
    dwi: np.ndarray = field(default_factory=lambda: np.zeros(3))
    ddric: np.ndarray = field(default_factory=lambda: np.zeros(3))
    dpi: np.ndarray = field(default_factory=lambda: np.array([0,0,0,0]))

    # end-effector (only link4 has se, Ce)
    sep: np.ndarray | None = None
    se: np.ndarray | None = None
    Ce: np.ndarray | None = None
    re: np.ndarray | None = None
    Ae: np.ndarray | None = None
    dre: np.ndarray | None = None

    Qih_RSDA: np.ndarray = field(default_factory=lambda: np.zeros(6))
    Qjh_RSDA: np.ndarray = field(default_factory=lambda: np.zeros(6))

@dataclass
class SubData:
    body1: BodyData = field(default_factory=BodyData)
    body2: BodyData = field(default_factory=BodyData)
    body3: BodyData = field(default_factory=BodyData)
    body4: BodyData = field(default_factory=BodyData)

def L_body1(sijp, Cij):
    body = BodyData()
    body.sijp = np.asarray(sijp, float).reshape(3)
    body.Cij = np.asarray(Cij, float).reshape(3,3)
    body.mi = 3.6
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 24217.363, 1.142, 22602.121, 3.656, 24383.284, -4.718
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([19.41,0,0], dtype=float)*1e-3
    body.Cii = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    return body

def L_body2():
    body = BodyData()
    body.sijp = np.array([120,0,0], dtype=float)*1e-3
    body.Cij = euler_zxz(-np.pi/2, np.pi/2, np.pi/2)
    body.mi = 12.9
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 101693.397, -54.639, 43784.882, 3156.796, 101586.518, -3.734
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([0,0,-101.13], dtype=float)*1e-3
    body.Cii = np.array([[1,0,0],[0,0,1],[0,-1,0]], dtype=float)
    return body

def L_body3():
    body = BodyData()
    body.sijp = np.array([0,0,-121], dtype=float)*1e-3
    body.Cij = euler_zxz(np.pi, np.pi/2, np.pi)
    body.mi = 11.1
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 172022.706, 939.804, 67557.291, 151.395, 155965.608, 39.970
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([0,238.39,-1.08], dtype=float)*1e-3
    body.Cii = np.eye(3)
    return body

def L_body4():
    body = BodyData()
    body.sijp = np.array([0,509,0], dtype=float)*1e-3
    body.Cij = euler_zxz(np.pi/2, np.pi/2, 0)
    body.mi = 11.5
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 686629.019, 10499.954, 44753.249, -23952.157, 705784.865, 1652.691
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([322.25,51.84,0], dtype=float)*1e-3
    body.Cii = euler_zxz(np.pi, np.pi/2, np.pi/2)
    body.sep = np.array([823.56,0,0], dtype=float)*1e-3
    body.Ce = euler_zxz(np.pi, np.pi/2, np.pi/2)
    return body

def R_body1(sijp, Cij):
    body = BodyData()
    body.sijp = np.asarray(sijp, float).reshape(3)
    body.Cij = np.asarray(Cij, float).reshape(3,3)
    body.mi = 3.6
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 24217.363, 1.142, 22602.121, -3.656, 24383.284, 4.718
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([-19.41,0,0], dtype=float)*1e-3
    body.Cii = euler_zxz(np.pi, np.pi/2, np.pi/2)
    return body

def R_body2():
    body = BodyData()
    body.sijp = np.array([-120,0,0], dtype=float)*1e-3
    body.Cij = euler_zxz(-np.pi/2, np.pi/2, np.pi/2)
    body.mi = 12.9
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 101693.397, 54.639, 43784.882, -3156.796, 101586.518, 3.734
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([0,0,101.13], dtype=float)*1e-3
    body.Cii = euler_zxz(np.pi, np.pi/2, np.pi)
    return body

def R_body3():
    body = BodyData()
    body.sijp = np.array([0,0,121], dtype=float)*1e-3
    body.Cij = euler_zxz(np.pi, np.pi/2, np.pi)
    body.mi = 11.1
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 172022.706, 939.804, 67557.291, -151.395, 155965.608, -39.970
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([0,-238.39,-1.08], dtype=float)*1e-3
    body.Cii = np.eye(3)
    return body

def R_body4():
    body = BodyData()
    body.sijp = np.array([0,-509,0], dtype=float)*1e-3
    body.Cij = euler_zxz(np.pi/2, np.pi/2, 0)
    body.mi = 11.5
    Ixx, Ixy, Iyy, Iyz, Izz, Izx = 686629.019, 10499.954, 44753.249, 23952.157, 705784.865, -1652.691
    body.Jip = np.array([[Ixx,Ixy,Izx],[Ixy,Iyy,Iyz],[Izx,Iyz,Izz]], dtype=float)*1e-6
    body.rhoip = np.array([-322.25,51.84,0], dtype=float)*1e-3
    body.Cii = euler_zxz(np.pi, np.pi/2, np.pi/2)
    body.sep = np.array([-823.56,0,0], dtype=float)*1e-3
    body.Ce = euler_zxz(np.pi, np.pi/2, np.pi/2)
    return body

class BaseBody(BodyData):
    def __init__(self):
        super().__init__()
        self.mi = 582.59
        Ixx, Ixy, Iyy, Iyz, Izz, Izx = 156890393.0, 0.0, 150169673.0, 0.0, 249303699.0, 0.0
        self.Jip = np.array([
            [Ixx, Ixy, Izx],
            [Ixy, Iyy, Iyz],
            [Izx, Iyz, Izz],
        ])

        self.sijp_FL = np.array([520, 758, 0], dtype=float) * 1e-3
        self.sijp_ML = np.array([0, 858, 0], dtype=float) * 1e-3
        self.sijp_RL = np.array([-520, 758, 0], dtype=float) * 1e-3
        self.sijp_FR = np.array([520, -758, 0], dtype=float) * 1e-3
        self.sijp_MR = np.array([0, -858, 0], dtype=float) * 1e-3
        self.sijp_RR = np.array([-520, -758, 0], dtype=float) * 1e-3

        self.Cij_FL = euler_zxz(np.pi / 2, np.pi / 2, 0)
        self.Cij_ML = euler_zxz(np.pi / 2, np.pi / 2, 0)
        self.Cij_RL = euler_zxz(np.pi / 2, np.pi / 2, 0)
        self.Cij_FR = euler_zxz(np.pi / 2, np.pi / 2, 0)
        self.Cij_MR = euler_zxz(np.pi / 2, np.pi / 2, 0)
        self.Cij_RR = euler_zxz(np.pi / 2, np.pi / 2, 0)

        self.Ei = np.zeros((3,4), dtype=float)
        self.Gi = np.zeros((3,4), dtype=float)

        self.Yih = np.zeros(6, dtype=float)

    def position_analysis(self):
        self.pi = self.pi / np.linalg.norm(self.pi)
        q0 = self.pi[0]
        qv = self.pi[1:4]
        self.Ei = np.column_stack((qv, skew(qv) + q0 * np.eye(3)))
        self.Gi = np.column_stack((qv, -skew(qv) + q0 * np.eye(3)))
        self.Ai = self.Ei @ self.Gi.T
        self.rpy = mat2rpy(self.Ai)

        self.rhoi = self.Ai@self.rhoip
        self.ric = self.ri + self.rhoi
        self.rit = skew(self.ri)
        self.rict = skew(self.ric)

    def velocity_analysis(self):
        Ai_Cii = self.Ai@self.Cii
        self.Jic = Ai_Cii@self.Jip@Ai_Cii.T
        self.wit = skew(self.wi)

        self.dric = self.dri + self.wit@self.rhoi
        self.drit = skew(self.dri)
        self.drict = skew(self.dric)

        self.Yih[0:3] = self.dri + self.drit@self.wi
        self.Yih[3:6] = self.wi

    def mass_force_analysis(self):
        self.fic = np.array([0,0,self.mi*sim.g])
        self.tic = np.array([0,0,0])

        self.Mih[0:3, 0:3] = self.mi*np.eye(3)
        self.Mih[0:3, 3:6] = -self.mi*self.rict
        self.Mih[3:6, 0:3] = self.mi*self.rict
        self.Mih[3:6, 3:6] = self.Jic - self.mi*self.rict@self.rict

        self.Qih[0:3] = self.fic + self.mi*self.drict@self.wi
        self.Qih[3:6] = (self.tic + self.rict@self.fic + self.mi*self.rict@self.drict@self.wi
                         - self.wit@self.Jic@self.wi)

class SubSystem(SubData):
    def __init__(self, side: str, sijp=None, Cij=None):
        super().__init__()
        if sijp is None:
            sijp = np.zeros(3)
        if Cij is None:
            Cij = np.eye(3)

        sijp = np.asarray(sijp, float).reshape(3)
        Cij = np.asarray(Cij, float).reshape(3, 3)

        if side == "L":
            self.body = [L_body1(sijp, Cij), L_body2(), L_body3(), L_body4()]
        elif side == "R":
            self.body = [R_body1(sijp, Cij), R_body2(), R_body3(), R_body4()]
        else:
            raise ValueError(f"side must be 'L' or 'R', got {side!r}")

        self.r_K = np.array([15000, 7000, 7000, 7000], dtype=float)
        self.r_C = np.array([1500, 300, 300, 700], dtype=float)

        self.road_h = -0.3
        self.c_K = 55000
        self.c_C = 5500
        self.f_contact = np.zeros(3)
        self.Qih_CONT = np.zeros(6)

        self.M = np.zeros((4, 4))
        self.Q = np.zeros(4)
        self.Myq = np.zeros((6, 4))

        self.q = np.zeros(4)
        self.q_init = np.zeros(4)
        self.dq = np.zeros(4)
        self.ddq = np.zeros(4)

    def position_analysis(self, base: "BaseBody"):
        for body, q in zip(self.body, self.q):
            body.Aijpp = np.array([
                [np.cos(q), -np.sin(q), 0],[np.sin(q), np.cos(q), 0],[0, 0, 1]
            ], dtype=float)

        prev = base
        for body in self.body:
            body.Ai = prev.Ai@body.Cij@body.Aijpp
            body.sij = prev.Ai@body.sijp
            body.ri = prev.ri + body.sij

            body.rhoi = body.Ai@body.rhoip
            body.ric = body.ri + body.rhoi

            prev = body

        ee = self.body[-1]
        ee.se = ee.Ai @ ee.sep
        ee.re = ee.ri + ee.se
        ee.Ae = ee.Ai @ ee.Ce
        ee.rpy = mat2rpy(ee.Ae)

    def velocity_analysis(self, base: "BaseBody"):
        prev = base
        for body, dq in zip(self.body, self.dq):
            body.Hi = prev.Ai@body.Cij@body.u_vec
            body.wi = prev.wi + body.Hi*dq
            body.wit= skew(body.wi)
            body.dri = prev.dri + body.wit@body.sij

            body.rit = skew(body.ri)
            body.Bi[0:3] = body.rit@body.Hi
            body.Bi[3:6] = body.Hi
            body.drit = skew(body.dri)
            body.dric = body.dri + body.wit@body.rhoi
            body.dHi = prev.wit@body.Hi

            body.Di[0:3] = body.drit@body.Hi + body.rit@body.dHi
            body.Di[3:6] = body.dHi
            body.Di = body.Di*dq

            body.Yih = prev.Yih + body.Bi*dq

            prev = body

        ee = self.body[-1]
        ee.dre = ee.dri + ee.wit@ee.re

    def mass_force_analysis(self):
        for body in self.body:
            Ai_Cii = body.Ai@body.Cii
            body.Jic = Ai_Cii@body.Jip@Ai_Cii.T
            body.rict = skew(body.ric)
            body.drict = skew(body.dric)

            body.fic = np.array([0,0,body.mi*sim.g], dtype=float)
            body.tic = np.array([0,0,0], dtype=float)

            body.Mih[0:3, 0:3] = body.mi*np.eye(3)
            body.Mih[0:3, 3:6] = -body.mi*body.rict
            body.Mih[3:6, 0:3] = body.mi*body.rict
            body.Mih[3:6, 3:6] = body.Jic - body.mi*body.rict@body.rict

            body.Qih[0:3] = body.fic + body.mi*body.drict@body.wi
            body.Qih[3:6] = (body.tic + body.rict@body.fic + body.mi*body.rict@body.drict@body.wi
                             - body.wit@body.Jic@body.wi)

        # ee = self.body[-1]
        # pen_z = self.road_h - ee.re[2]
        # pen_dz = -ee.dre
        # if pen_z > 0:
        #     f_c = pen_z * self.c_K + pen_dz * self.c_C
        #     self.f_contact = np.array([0, 0, f_c])
        # else:
        #     self.f_contact = np.zeros(3)
        # rec = ee.re - ee.ric
        # rect = skew(rec)
        # self.Qih_CONT[0:3] = self.f_contact
        # self.Qih_CONT[3:6] = rect@self.f_contact
        #
        # ee.Qih += self.Qih_CONT

        self.body[3].Ki = self.body[3].Mih
        self.body[2].Ki = self.body[2].Mih + self.body[3].Ki
        self.body[1].Ki = self.body[1].Mih + self.body[2].Ki
        self.body[0].Ki = self.body[0].Mih + self.body[1].Ki

        self.body[3].Li = self.body[3].Qih
        self.body[2].Li = self.body[2].Qih + self.body[3].Li - self.body[3].Ki @ self.body[3].Di + self.body[3].Qjh_RSDA
        self.body[1].Li = self.body[1].Qih + self.body[2].Li - self.body[2].Ki @ self.body[2].Di + self.body[2].Qjh_RSDA
        self.body[0].Li = self.body[0].Qih + self.body[1].Li - self.body[1].Ki @ self.body[1].Di + self.body[1].Qjh_RSDA

        self.M[0, 0] = self.body[0].Bi.T @ self.body[0].Ki @ self.body[0].Bi
        self.M[0, 1] = self.body[0].Bi.T @ self.body[1].Ki @ self.body[1].Bi
        self.M[0, 2] = self.body[0].Bi.T @ self.body[2].Ki @ self.body[2].Bi
        self.M[0, 3] = self.body[0].Bi.T @ self.body[3].Ki @ self.body[3].Bi

        self.M[1, 0] = self.body[1].Bi.T @ self.body[1].Ki @ self.body[0].Bi
        self.M[1, 1] = self.body[1].Bi.T @ self.body[1].Ki @ self.body[1].Bi
        self.M[1, 2] = self.body[1].Bi.T @ self.body[2].Ki @ self.body[2].Bi
        self.M[1, 3] = self.body[1].Bi.T @ self.body[3].Ki @ self.body[3].Bi

        self.M[2, 0] = self.body[2].Bi.T @ self.body[2].Ki @ self.body[0].Bi
        self.M[2, 1] = self.body[2].Bi.T @ self.body[2].Ki @ self.body[1].Bi
        self.M[2, 2] = self.body[2].Bi.T @ self.body[2].Ki @ self.body[2].Bi
        self.M[2, 3] = self.body[2].Bi.T @ self.body[3].Ki @ self.body[3].Bi

        self.M[3, 0] = self.body[3].Bi.T @ self.body[3].Ki @ self.body[0].Bi
        self.M[3, 1] = self.body[3].Bi.T @ self.body[3].Ki @ self.body[1].Bi
        self.M[3, 2] = self.body[3].Bi.T @ self.body[3].Ki @ self.body[2].Bi
        self.M[3, 3] = self.body[3].Bi.T @ self.body[3].Ki @ self.body[3].Bi

        self.Myq[:,0] = self.body[0].Ki @ self.body[0].Bi
        self.Myq[:,1] = self.body[1].Ki @ self.body[1].Bi
        self.Myq[:,2] = self.body[2].Ki @ self.body[2].Bi
        self.Myq[:,3] = self.body[3].Ki @ self.body[3].Bi

        self.Q[0] = self.body[0].Bi.T@(self.body[0].Li - self.body[0].Ki@(self.body[0].Di))
        self.Q[1] = self.body[1].Bi.T@(self.body[1].Li - self.body[1].Ki@(self.body[0].Di + self.body[1].Di))
        self.Q[2] = self.body[2].Bi.T@(self.body[2].Li - self.body[2].Ki@(self.body[0].Di + self.body[1].Di + self.body[2].Di))
        self.Q[3] = self.body[3].Bi.T@(self.body[3].Li - self.body[3].Ki@(self.body[0].Di + self.body[1].Di + self.body[2].Di + self.body[3].Di))
