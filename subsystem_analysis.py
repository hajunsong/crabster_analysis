from data_container import *
import read_base as base
from typing import List
import sim_info as sim

def sub_position_analysis(body: List[Body, Body, Body, Body]):
    for i in range(0, 4):
        body[i].Aijpp = [
            [np.cos(body[i].qi), -np.sin(body[i].qi), 0],
            [np.sin(body[i].qi),  np.sin(body[i].qi), 0],
            [0, 0, 1]
        ]

    body[0].Ai = base.Ai@body[0].Cij@body[0].Aijpp
    body[0].sij = base.Ai@body[0].sijp
    body[0].ri = base.ri + body[0].sij
    for i in range(1, 4):
        body[i].Ai = body[i-1].Ai@body[i].Cij@body[i].Aijpp
        body[i].sij = body[i-1]@body[i].sijp
        body[i].ri = body[i-1].ri + body[i].sij

    for i in range(0, 4):
        body[i].rhoi = body[i].Ai@body[i].rhoip
        body[i].ric = body[i].ri + body[i].rhoi

    body[3].se = body[3].Ai@body[3].sep
    body[3].re = body[3].ri + body[3].se
    body[3].Ae = body[3].Ai@body[3].Ce
    body[3].rpy = mat2rpy(body[3].Ae)

    return body


def sub_velocity_analysis(body: List[Body, Body, Body, Body]):
    body[0].Hi = base.Ai@body[0].Cij@body[0].u_vec
    body[0].wi = base.wi + body[0].Hi*body[0].dqi
    for i in range(1, 4):
        body[i].Hi = body[i-1].Ai@body[i].Cij@body[i].u_vec
        body[i].wi = body[i-1].wi + body[i].Hi*body[i].dqi

    for i in range(0, 4):
        body[i].wit = skew(body[i].wi)

    body[0].dri = base.dri + body[0].wit@body[0].sij
    for i in range(1, 4):
        body[i].dri = body[i-1].dri + body[i].wit@body[i].sij

    body[3].dre = body[3].dri + body[3].wit@body[3].re

    for i in range(0, 4):
        body[i].rit = skew(body[i].ri)
        body[i].Bi[0:3] = body[i].rit@body[i].Hi
        body[i].Bi[3:6] = body[i].Hi
        body[i].drit = skew(body[i].dri)
        body[i].dric = body[i].dri + body[i].wit*body[i].rhoi

    body[0].dHi = base.wit@body[0].Hi
    for i in range(1, 4):
        body[i].dHi = body[i-1].wit@body[i].Hi

    for i in range(0, 4):
        body[i].Di[0:3] = body[i].drit@body[i].Hi + body[i].rit@body[i].dHi
        body[i].Di[3:6] = body[i].dHi
        body[i].Di = body[i].Di*body[i].dqi

    body[0].Yih = base.Yih + body[0].Bi*body[0].dqi
    for i in range(1, 4):
        body[i].Yih = body[i-1].Yih + body[i].Bi*body[i].dqi
    
def sub_mass_force_analysis(body: List[Body, Body, Body, Body]):
    r_K = np.array([15000, 7000, 7000, 7000], dtype=float)
    r_C = np.array([1500, 300, 300, 700], dtype=float)

    road_h = -0.3
    c_K = 55000
    c_C = 5500

    for i in range(0, 4):
        Ai_Cii = body[i].Ai@body[i].Cii
        body[i].Jic = Ai_Cii@body[i].Jip@Ai_Cii.T
        body[i].rict = skew(body[i].ric)
        body[i].drict = skew(body[i].dric)

        body[i].fic = np.array([0, 0, body[i].mi*sim.g])
        body[i].tic = np.zeros(3)

        if i == 3:
            pen_z = road_h - body[i].re[2]
            pen_dz = -body[i].dre
            if pen_z > 0:
                f_c = pen_z*c_K + pen_dz*c_C
                body[i].f_c = np.array([0, 0, f_c])
            else:
                body[i].f_c = np.zeros(3)