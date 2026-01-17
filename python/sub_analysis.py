import numpy as np
from sim import *

def sub_position_analysis(sub, s01p, C01):
    sub.A01pp = np.array([[np.cos(sub.q[0]), -np.sin(sub.q[0]), 0], [np.sin(sub.q[0]), np.cos(sub.q[0]), 0], [0, 0, 1]], dtype=np.float64)
    sub.A12pp = np.array([[np.cos(sub.q[1]), -np.sin(sub.q[1]), 0], [np.sin(sub.q[1]), np.cos(sub.q[1]), 0], [0, 0, 1]], dtype=np.float64)
    sub.A23pp = np.array([[np.cos(sub.q[2]), -np.sin(sub.q[2]), 0], [np.sin(sub.q[2]), np.cos(sub.q[2]), 0], [0, 0, 1]], dtype=np.float64)
    sub.A34pp = np.array([[np.cos(sub.q[3]), -np.sin(sub.q[3]), 0], [np.sin(sub.q[3]), np.cos(sub.q[3]), 0], [0, 0, 1]], dtype=np.float64)

    sub.A1 = A0 @ C01 @ sub.A01pp;         sub.s01 = A0 @ s01p;         sub.r1 = r0 + sub.s01
    sub.A2 = sub.A1 @ sub.C12 @ sub.A12pp; sub.s12 = sub.A1 @ sub.s12p; sub.r2 = sub.r1 + sub.s12
    sub.A3 = sub.A2 @ sub.C23 @ sub.A23pp; sub.s23 = sub.A2 @ sub.s23p; sub.r3 = sub.r2 + sub.s23
    sub.A4 = sub.A3 @ sub.C34 @ sub.A34pp; sub.s34 = sub.A3 @ sub.s34p; sub.r4 = sub.r3 + sub.s34

    sub.rho1 = sub.A1 @ sub.rho1p; sub.r1c = sub.r1 + sub.rho1
    sub.rho2 = sub.A2 @ sub.rho2p; sub.r2c = sub.r2 + sub.rho2
    sub.rho3 = sub.A3 @ sub.rho3p; sub.r3c = sub.r3 + sub.rho3
    sub.rho4 = sub.A4 @ sub.rho4p; sub.r4c = sub.r4 + sub.rho4

    sub.s4e = sub.A4 @ sub.s4ep
    sub.re = sub.r4 + sub.s4e
    sub.Ae = sub.A4 @ sub.C4e
    sub.rpy = mat2rpy(sub.Ae)

    return sub

def sub_velocity_analysis(sub, C01):
    sub.H1 = A0 @ C01 @ sub.u_vec1;         sub.w1 = w0 + sub.H1 * sub.dq[0];     sub.w1t = skew(sub.w1)
    sub.H2 = sub.A1 @ sub.C12 @ sub.u_vec2; sub.w2 = sub.w1 + sub.H2 * sub.dq[1]; sub.w2t = skew(sub.w2)
    sub.H3 = sub.A2 @ sub.C23 @ sub.u_vec3; sub.w3 = sub.w2 + sub.H3 * sub.dq[2]; sub.w3t = skew(sub.w3)
    sub.H4 = sub.A3 @ sub.C34 @ sub.u_vec4; sub.w4 = sub.w3 + sub.H4 * sub.dq[3]; sub.w4t = skew(sub.w4)

    sub.dr1 = dr0 + w0t @ sub.s01;         sub.r1t = skew(sub.r1)
    sub.dr2 = sub.dr1 + sub.w1t @ sub.s12; sub.r2t = skew(sub.r2)
    sub.dr3 = sub.dr2 + sub.w2t @ sub.s23; sub.r3t = skew(sub.r3)
    sub.dr4 = sub.dr3 + sub.w3t @ sub.s34; sub.r4t = skew(sub.r4)

    sub.dre = sub.dr4 + sub.w4t @ sub.r4

    sub.B1 = np.concatenate((sub.r1t @ sub.H1, sub.H1))
    sub.B2 = np.concatenate((sub.r2t @ sub.H2, sub.H2))
    sub.B3 = np.concatenate((sub.r3t @ sub.H3, sub.H3))
    sub.B4 = np.concatenate((sub.r4t @ sub.H4, sub.H4))

    sub.dr1t = skew(sub.dr1); sub.dr1c = sub.dr1 + sub.w1t @ sub.rho1; sub.dH1 = w0t @ sub.H1
    sub.dr2t = skew(sub.dr2); sub.dr2c = sub.dr2 + sub.w2t @ sub.rho2; sub.dH2 = sub.w1t @ sub.H2
    sub.dr3t = skew(sub.dr3); sub.dr3c = sub.dr3 + sub.w3t @ sub.rho3; sub.dH3 = sub.w2t @ sub.H3
    sub.dr4t = skew(sub.dr4); sub.dr4c = sub.dr4 + sub.w4t @ sub.rho4; sub.dH4 = sub.w3t @ sub.H4

    sub.D1 = np.concatenate((sub.dr1t @ sub.H1 + sub.r1t @ sub.dH1, sub.dH1)) * sub.dq[0]
    sub.D2 = np.concatenate((sub.dr2t @ sub.H2 + sub.r2t @ sub.dH2, sub.dH2)) * sub.dq[1]
    sub.D3 = np.concatenate((sub.dr3t @ sub.H3 + sub.r3t @ sub.dH3, sub.dH3)) * sub.dq[2]
    sub.D4 = np.concatenate((sub.dr4t @ sub.H4 + sub.r4t @ sub.dH4, sub.dH4)) * sub.dq[3]

    sub.Y1h = Y0h + sub.B1 * sub.dq[0]
    sub.Y2h = sub.Y1h + sub.B2 * sub.dq[1]
    sub.Y3h = sub.Y2h + sub.B3 * sub.dq[2]
    sub.Y4h = sub.Y3h + sub.B4 * sub.dq[3]

    return sub

def sub_mass_force_analysis(sub):
    A1_C11 = sub.A1 @ sub.C11; sub.J1c = A1_C11 @ sub.J1p @ A1_C11.T
    A2_C22 = sub.A2 @ sub.C22; sub.J2c = A2_C22 @ sub.J2p @ A2_C22.T
    A3_C33 = sub.A3 @ sub.C33; sub.J3c = A3_C33 @ sub.J3p @ A3_C33.T
    A4_C44 = sub.A4 @ sub.C44; sub.J4c = A4_C44 @ sub.J4p @ A4_C44.T

    sub.r1ct = skew(sub.r1c); sub.dr1ct = skew(sub.dr1c)
    sub.r2ct = skew(sub.r2c); sub.dr2ct = skew(sub.dr2c)
    sub.r3ct = skew(sub.r3c); sub.dr3ct = skew(sub.dr3c)
    sub.r4ct = skew(sub.r4c); sub.dr4ct = skew(sub.dr4c)

    f1c = np.array([0, 0, sub.m1 * g], dtype=np.float64); t1c = np.zeros(3, dtype=np.float64)
    f2c = np.array([0, 0, sub.m2 * g], dtype=np.float64); t2c = np.zeros(3, dtype=np.float64)
    f3c = np.array([0, 0, sub.m3 * g], dtype=np.float64); t3c = np.zeros(3, dtype=np.float64)
    f4c = np.array([0, 0, sub.m4 * g], dtype=np.float64); t4c = np.zeros(3, dtype=np.float64)

    M1h_11 = sub.m1 * np.eye(3, dtype=np.float64); M1h_12 = -sub.m1 * sub.r1ct
    M1h_22 = sub.J1c - sub.m1 * sub.r1ct @ sub.r1ct
    M2h_11 = sub.m2 * np.eye(3, dtype=np.float64); M2h_12 = -sub.m2 * sub.r2ct
    M2h_22 = sub.J2c - sub.m2 * sub.r2ct @ sub.r2ct
    M3h_11 = sub.m3 * np.eye(3, dtype=np.float64); M3h_12 = -sub.m3 * sub.r3ct
    M3h_22 = sub.J3c - sub.m3 * sub.r3ct @ sub.r3ct
    M4h_11 = sub.m4 * np.eye(3, dtype=np.float64); M4h_12 = -sub.m4 * sub.r4ct
    M4h_22 = sub.J4c - sub.m4 * sub.r4ct @ sub.r4ct

    sub.M1h = np.vstack((np.column_stack((M1h_11, M1h_12)), np.column_stack((-M1h_12, M1h_22))))
    sub.M2h = np.vstack((np.column_stack((M2h_11, M2h_12)), np.column_stack((-M2h_12, M2h_22))))
    sub.M3h = np.vstack((np.column_stack((M3h_11, M3h_12)), np.column_stack((-M3h_12, M3h_22))))
    sub.M4h = np.vstack((np.column_stack((M4h_11, M4h_12)), np.column_stack((-M4h_12, M4h_22))))

    sub.Q1h = np.concatenate([f1c + sub.m1 * sub.dr1ct @ sub.w1,
                              t1c + sub.r1ct @ f1c + sub.m1 * sub.r1ct @ sub.dr1ct @ sub.w1 - sub.w1t @ sub.J1c @ sub.w1])
    sub.Q2h = np.concatenate([f2c + sub.m2 * sub.dr2ct @ sub.w2,
                              t2c + sub.r2ct @ f2c + sub.m2 * sub.r2ct @ sub.dr2ct @ sub.w2 - sub.w2t @ sub.J2c @ sub.w2])
    sub.Q3h = np.concatenate([f3c + sub.m3 * sub.dr3ct @ sub.w3,
                              t3c + sub.r3ct @ f3c + sub.m3 * sub.r3ct @ sub.dr3ct @ sub.w3 - sub.w3t @ sub.J3c @ sub.w3])
    sub.Q4h = np.concatenate([f4c + sub.m4 * sub.dr4ct @ sub.w4,
                              t4c + sub.r4ct @ f4c + sub.m4 * sub.r4ct @ sub.dr4ct @ sub.w4 - sub.w4t @ sub.J4c @ sub.w4])
    
    sub.T1_RSDA = (sub.q_init[0] - sub.q[0])*K_RSDA[0] - sub.dq[0]*C_RSDA[0]
    sub.T2_RSDA = (sub.q_init[1] - sub.q[1])*K_RSDA[1] - sub.dq[1]*C_RSDA[1]
    sub.T3_RSDA = (sub.q_init[2] - sub.q[2])*K_RSDA[2] - sub.dq[2]*C_RSDA[2]
    sub.T4_RSDA = (sub.q_init[3] - sub.q[3])*K_RSDA[3] - sub.dq[3]*C_RSDA[3]

    sub.Q1h_RSDA = np.concatenate([np.zeros(3), np.array([0, 0, sub.T1_RSDA])])
    sub.Q2h_RSDA = np.concatenate([np.zeros(3), np.array([0, 0, sub.T2_RSDA])])
    sub.Q3h_RSDA = np.concatenate([np.zeros(3), np.array([0, 0, sub.T3_RSDA])])
    sub.Q4h_RSDA = np.concatenate([np.zeros(3), np.array([0, 0, sub.T4_RSDA])])

    # sub.Q1h += sub.Q1h_RSDA
    # sub.Q2h += sub.Q2h_RSDA
    # sub.Q3h += sub.Q3h_RSDA
    # sub.Q4h += sub.Q4h_RSDA

    sub.K4 = sub.M4h
    sub.K3 = sub.M3h + sub.K4
    sub.K2 = sub.M2h + sub.K3
    sub.K1 = sub.M1h + sub.K2

    sub.L4 = sub.Q4h
    sub.L3 = sub.Q3h + sub.L4 - sub.K4 @ sub.D4 # - sub.Q4h_RSDA
    sub.L2 = sub.Q2h + sub.L3 - sub.K3 @ sub.D3 # - sub.Q3h_RSDA
    sub.L1 = sub.Q1h + sub.L2 - sub.K2 @ sub.D2 # - sub.Q2h_RSDA

    M_1 = np.column_stack([sub.B1.T @ sub.K1 @ sub.B1, sub.B1.T @ sub.K2 @ sub.B2, sub.B1.T @ sub.K3 @ sub.B3, sub.B1.T @ sub.K4 @ sub.B4])
    M_2 = np.column_stack([sub.B2.T @ sub.K2 @ sub.B1, sub.B2.T @ sub.K2 @ sub.B2, sub.B2.T @ sub.K3 @ sub.B3, sub.B2.T @ sub.K4 @ sub.B4])
    M_3 = np.column_stack([sub.B3.T @ sub.K3 @ sub.B1, sub.B3.T @ sub.K3 @ sub.B2, sub.B3.T @ sub.K3 @ sub.B3, sub.B3.T @ sub.K4 @ sub.B4])
    M_4 = np.column_stack([sub.B4.T @ sub.K4 @ sub.B1, sub.B4.T @ sub.K4 @ sub.B2, sub.B4.T @ sub.K4 @ sub.B3, sub.B4.T @ sub.K4 @ sub.B4])
    sub.M = np.vstack([M_1, M_2, M_3, M_4])

    sub.Myq = np.column_stack([sub.K1 @ sub.B1, sub.K2 @ sub.B2, sub.K3 @ sub.B3, sub.K4 @ sub.B4])

    Q_1 = sub.B1.T @ (sub.L1 - sub.K1 @ (sub.D1))
    Q_2 = sub.B2.T @ (sub.L2 - sub.K2 @ (sub.D1 + sub.D2))
    Q_3 = sub.B3.T @ (sub.L3 - sub.K3 @ (sub.D1 + sub.D2 + sub.D3))
    Q_4 = sub.B4.T @ (sub.L4 - sub.K4 @ (sub.D1 + sub.D2 + sub.D3 + sub.D4))
    sub.Q = np.array([Q_1, Q_2, Q_3, Q_4])

    return sub

def sub_acceleration_analysis(sub):
    sub.dY1h = dY0h + sub.B1 * sub.ddq[0] + sub.D1
    sub.dY2h = sub.dY1h + sub.B2 * sub.ddq[1] + sub.D2
    sub.dY3h = sub.dY2h + sub.B3 * sub.ddq[2] + sub.D3
    sub.dY4h = sub.dY3h + sub.B4 * sub.ddq[3] + sub.D4

    T1 = np.vstack([np.column_stack([np.eye(3), -sub.r1t]), np.column_stack([np.zeros((3, 3)), np.eye(3)])])
    T2 = np.vstack([np.column_stack([np.eye(3), -sub.r2t]), np.column_stack([np.zeros((3, 3)), np.eye(3)])])
    T3 = np.vstack([np.column_stack([np.eye(3), -sub.r3t]), np.column_stack([np.zeros((3, 3)), np.eye(3)])])
    T4 = np.vstack([np.column_stack([np.eye(3), -sub.r4t]), np.column_stack([np.zeros((3, 3)), np.eye(3)])])

    dT1 = np.vstack([np.column_stack([np.zeros((3,3)), -sub.dr1t]), np.zeros((3, 6))])
    dT2 = np.vstack([np.column_stack([np.zeros((3,3)), -sub.dr2t]), np.zeros((3, 6))])
    dT3 = np.vstack([np.column_stack([np.zeros((3,3)), -sub.dr3t]), np.zeros((3, 6))])
    dT4 = np.vstack([np.column_stack([np.zeros((3,3)), -sub.dr4t]), np.zeros((3, 6))])

    sub.R1 = np.concatenate([sub.dr1t @ sub.w1, np.zeros(3)])
    sub.R2 = np.concatenate([sub.dr2t @ sub.w2, np.zeros(3)])
    sub.R3 = np.concatenate([sub.dr3t @ sub.w3, np.zeros(3)])
    sub.R4 = np.concatenate([sub.dr4t @ sub.w4, np.zeros(3)])

    sub.dY1b = dT1 @ sub.Y1h + T1 @ sub.dY1h
    sub.dY2b = dT2 @ sub.Y2h + T2 @ sub.dY2h
    sub.dY3b = dT3 @ sub.Y3h + T3 @ sub.dY3h
    sub.dY4b = dT4 @ sub.Y4h + T4 @ sub.dY4h

    sub.ddr1 = sub.dY1b[0:3]; sub.dw1 = sub.dY1b[3:6]; sub.dw1t = skew(sub.dw1)
    sub.ddr2 = sub.dY2b[0:3]; sub.dw2 = sub.dY2b[3:6]; sub.dw2t = skew(sub.dw2)
    sub.ddr3 = sub.dY3b[0:3]; sub.dw3 = sub.dY3b[3:6]; sub.dw3t = skew(sub.dw3)
    sub.ddr4 = sub.dY4b[0:3]; sub.dw4 = sub.dY4b[3:6]; sub.dw4t = skew(sub.dw4)

    sub.ddr1c = sub.ddr1 + sub.dw1t @ sub.rho1 + sub.w1t @ sub.w1t @ sub.rho1
    sub.ddr2c = sub.ddr2 + sub.dw2t @ sub.rho2 + sub.w2t @ sub.w2t @ sub.rho2
    sub.ddr3c = sub.ddr3 + sub.dw3t @ sub.rho3 + sub.w3t @ sub.w3t @ sub.rho3
    sub.ddr4c = sub.ddr4 + sub.dw4t @ sub.rho4 + sub.w4t @ sub.w4t @ sub.rho4
    
    return sub