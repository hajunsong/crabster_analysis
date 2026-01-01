from data_con import *
import read_base as base
import sim_info as sim

def sub_position_analysis(sub: SubSystem):
    for i in range(0, 4):
        sub.body[i].Aijpp = [
            [np.cos(sub.body[i].qi), -np.sin(sub.body[i].qi), 0],
            [np.sin(sub.body[i].qi), np.sin(sub.body[i].qi), 0],
            [0, 0, 1]
        ]

    sub.body[0].Ai = base.Ai @ sub.body[0].Cij @ sub.body[0].Aijpp
    sub.body[0].sij = base.Ai @ sub.body[0].sijp
    sub.body[0].ri = base.ri + sub.body[0].sij
    for i in range(1, 4):
        sub.body[i].Ai = sub.body[i - 1].Ai @ sub.body[i].Cij @ sub.body[i].Aijpp
        sub.body[i].sij = sub.body[i - 1].Ai @ sub.body[i].sijp
        sub.body[i].ri = sub.body[i - 1].ri + sub.body[i].sij

    for i in range(0, 4):
        sub.body[i].rhoi = sub.body[i].Ai @ sub.body[i].rhoip
        sub.body[i].ric = sub.body[i].ri + sub.body[i].rhoi

    sub.body[3].se = sub.body[3].Ai @ sub.body[3].sep
    sub.body[3].re = sub.body[3].ri + sub.body[3].se
    sub.body[3].Ae = sub.body[3].Ai @ sub.body[3].Ce
    sub.body[3].rpy = mat2rpy(sub.body[3].Ae)

    return sub

def sub_velocity_analysis(sub: SubSystem):
    sub.body[0].Hi = base.Ai @ sub.body[0].Cij @ sub.body[0].u_vec
    sub.body[0].wi = base.wi + sub.body[0].Hi * sub.body[0].dqi
    for i in range(1, 4):
        sub.body[i].Hi = sub.body[i - 1].Ai @ sub.body[i].Cij @ sub.body[i].u_vec
        sub.body[i].wi = sub.body[i - 1].wi + sub.body[i].Hi * sub.body[i].dqi

    for i in range(0, 4):
        sub.body[i].wit = skew(sub.body[i].wi)

    sub.body[0].dri = base.dri + sub.body[0].wit @ sub.body[0].sij
    for i in range(1, 4):
        sub.body[i].dri = sub.body[i - 1].dri + sub.body[i].wit @ sub.body[i].sij

    sub.body[3].dre = sub.body[3].dri + sub.body[3].wit @ sub.body[3].re

    for i in range(0, 4):
        sub.body[i].rit = skew(sub.body[i].ri)
        sub.body[i].Bi[0:3] = sub.body[i].rit @ sub.body[i].Hi
        sub.body[i].Bi[3:6] = sub.body[i].Hi
        sub.body[i].drit = skew(sub.body[i].dri)
        sub.body[i].dric = sub.body[i].dri + sub.body[i].wit @ sub.body[i].rhoi

    sub.body[0].dHi = base.wit @ sub.body[0].Hi
    for i in range(1, 4):
        sub.body[i].dHi = sub.body[i - 1].wit @ sub.body[i].Hi

    for i in range(0, 4):
        sub.body[i].Di[0:3] = sub.body[i].drit @ sub.body[i].Hi + sub.body[i].rit @ sub.body[i].dHi
        sub.body[i].Di[3:6] = sub.body[i].dHi
        sub.body[i].Di = sub.body[i].Di * sub.body[i].dqi

    sub.body[0].Yih = base.Yih + sub.body[0].Bi * sub.body[0].dqi
    for i in range(1, 4):
        sub.body[i].Yih = sub.body[i - 1].Yih + sub.body[i].Bi * sub.body[i].dqi

    return sub

def sub_mass_force_analysis(sub: SubSystem):
    r_K = np.array([15000, 7000, 7000, 7000], dtype=float)
    r_C = np.array([1500, 300, 300, 700], dtype=float)

    road_h = -0.3
    c_K = 55000
    c_C = 5500

    for i in range(0, 4):
        Ai_Cii = sub.body[i].Ai @ sub.body[i].Cii
        sub.body[i].Jic = Ai_Cii @ sub.body[i].Jip @ Ai_Cii.T
        sub.body[i].rict = skew(sub.body[i].ric)
        sub.body[i].drict = skew(sub.body[i].dric)

        sub.body[i].fic = np.array([0, 0, sub.body[i].mi * sim.g])
        sub.body[i].tic = np.zeros(3)

        if i == 3:
            pen_z = road_h - sub.body[i].re[2]
            pen_dz = -sub.body[i].dre
            if pen_z > 0:
                f_c = pen_z * c_K + pen_dz * c_C
                sub.body[i].f_c = np.array([0, 0, f_c])
            else:
                sub.body[i].f_c = np.zeros(3)
            rec = sub.body[i].re - sub.body[i].ric
            rect = skew(rec)
            sub.body[i].fic = sub.body[i].fic + sub.body[i].f_c
            sub.body[i].tic = sub.body[i].tic + rect @ sub.body[i].f_c

        sub.body[i].Mih[0:3, 0:3] = sub.body[i].mi * np.eye(3)
        sub.body[i].Mih[0:3, 3:6] = -sub.body[i].mi * sub.body[i].rict
        sub.body[i].Mih[3:6, 0:3] = sub.body[i].mi * sub.body[i].rict
        sub.body[i].Mih[3:6, 3:6] = sub.body[i].Jic - sub.body[i].mi * sub.body[i].rict @ sub.body[i].rict

        sub.body[i].Qih[0:3] = sub.body[i].fic + sub.body[i].mi * sub.body[i].drict @ sub.body[i].wi
        sub.body[i].Qih[3:6] = (
                    sub.body[i].tic + sub.body[i].rict @ sub.body[i].fic + sub.body[i].mi * sub.body[i].rict @ sub.body[
                i].drict @ sub.body[i].wi
                    - sub.body[i].wit @ sub.body[i].Jic @ sub.body[i].wi)

        if sim.motion_flag == 1:
            sub.body[i].Ti_RSDA = 0
            sub.body[i].Qih_RSDA = np.zeros(6)
            sub.body[i].Qjh_RSDA = np.zeros(6)
        else:
            sub.body[i].Ti_RSDA = (sub.body[i].qi_init - sub.body[i].qi) * r_K[i] - sub.body[i].dqi * r_C[i]
            sub.body[i].Qih_RSDA[0:3] = np.zeros(3)
            sub.body[i].Qih_RSDA[3:6] = sub.body[i].Ti_RSDA * sub.body[i].Hi
            sub.body[i].Qjh_RSDA = -sub.body[i].Qih_RSDA
            sub.body[i].Qih = sub.body[i].Qih + sub.body[i].Qih_RSDA

    sub.body[3].Ki = sub.body[3].Mih
    sub.body[2].Ki = sub.body[2].Mih + sub.body[3].Ki
    sub.body[1].Ki = sub.body[1].Mih + sub.body[2].Ki
    sub.body[0].Ki = sub.body[0].Mih + sub.body[1].Ki

    sub.body[3].Li = sub.body[3].Qih
    sub.body[2].Li = sub.body[2].Qih + sub.body[3].Li - sub.body[3].Ki @ sub.body[3].Di + sub.body[3].Qjh_RSDA
    sub.body[1].Li = sub.body[1].Qih + sub.body[2].Li - sub.body[2].Ki @ sub.body[2].Di + sub.body[2].Qjh_RSDA
    sub.body[0].Li = sub.body[0].Qih + sub.body[1].Li - sub.body[1].Ki @ sub.body[1].Di + sub.body[1].Qjh_RSDA

    sub.M[0, 0] = sub.body[0].Bi.T @ sub.body[0].Ki @ sub.body[0].Bi
    sub.M[0, 1] = sub.body[0].Bi.T @ sub.body[1].Ki @ sub.body[1].Bi
    sub.M[0, 2] = sub.body[0].Bi.T @ sub.body[2].Ki @ sub.body[2].Bi
    sub.M[0, 3] = sub.body[0].Bi.T @ sub.body[3].Ki @ sub.body[3].Bi

    sub.M[1, 0] = sub.body[1].Bi.T @ sub.body[1].Ki @ sub.body[0].Bi
    sub.M[1, 1] = sub.body[1].Bi.T @ sub.body[1].Ki @ sub.body[1].Bi
    sub.M[1, 2] = sub.body[1].Bi.T @ sub.body[2].Ki @ sub.body[2].Bi
    sub.M[1, 3] = sub.body[1].Bi.T @ sub.body[3].Ki @ sub.body[3].Bi

    sub.M[2, 0] = sub.body[2].Bi.T @ sub.body[2].Ki @ sub.body[0].Bi
    sub.M[2, 1] = sub.body[2].Bi.T @ sub.body[2].Ki @ sub.body[1].Bi
    sub.M[2, 2] = sub.body[2].Bi.T @ sub.body[2].Ki @ sub.body[2].Bi
    sub.M[2, 3] = sub.body[2].Bi.T @ sub.body[3].Ki @ sub.body[3].Bi

    sub.M[3, 0] = sub.body[3].Bi.T @ sub.body[3].Ki @ sub.body[0].Bi
    sub.M[3, 1] = sub.body[3].Bi.T @ sub.body[3].Ki @ sub.body[1].Bi
    sub.M[3, 2] = sub.body[3].Bi.T @ sub.body[3].Ki @ sub.body[2].Bi
    sub.M[3, 3] = sub.body[3].Bi.T @ sub.body[3].Ki @ sub.body[3].Bi

    sub.Myq[:, 0] = sub.body[0].Ki @ sub.body[0].Bi

    return sub