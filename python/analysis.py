from sim import *
from read_base import *
from sub_analysis import *

def analysis(Y):
    global FL, ML, RL, FR, MR, RR, g

    cuts = [3, 7, 10, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57]
    (r0, p0, dr0, w0,
     FL.q, FL.dq, ML.q, ML.dq, RL.q, RL.dq,
     FR.q, FR.dq, MR.q, MR.dq, RR.q, RR.dq) = np.split(Y, cuts)

    q0 = p0[0]
    qv = p0[1:4]
    E0 = np.column_stack([-qv, skew(qv) + q0 * np.eye(3, dtype=np.float64)])
    G0 = np.column_stack([-qv, -skew(qv) + q0 * np.eye(3, dtype=np.float64)])
    A0 = E0 @ G0.T
    rpy0 = mat2rpy(A0)

    A0_C00 = A0 @ C00
    J0c = A0_C00 @ J0p @ A0_C00.T
    rho0 = A0 @ rho0p
    r0c = r0 + rho0

    w0t = skew(w0)
    r0t = skew(r0)

    dr0c = dr0 + w0t @ rho0

    dr0t = skew(dr0)
    dr0ct = skew(dr0c)
    r0ct = skew(r0c)

    Y0h = np.concatenate([dr0 + dr0t @ w0, w0], dtype=np.float64)

    f0c = np.array([0, 0, m0 * g], dtype=np.float64)
    t0c = np.array([0, 0, 0], dtype=np.float64)

    M0h_11 = m0 * np.eye(3, dtype=np.float64)
    M0h_12 = -m0 * r0ct
    M0h_22 = J0c - m0 * r0ct @ r0ct
    M0h = np.vstack((np.column_stack((M0h_11, M0h_12)), np.column_stack((-M0h_12, M0h_22))))
    Q0h = np.concatenate([f0c + m0 * dr0ct @ w0, t0c + r0ct @ f0c + m0 * r0ct @ dr0ct @ w0 - w0t @ J0c @ w0])

    FL = sub_position_analysis(FL, FL_s01p, FL_C01)
    ML = sub_position_analysis(ML, ML_s01p, ML_C01)
    RL = sub_position_analysis(RL, RL_s01p, RL_C01)
    FR = sub_position_analysis(FR, FR_s01p, FR_C01)
    MR = sub_position_analysis(MR, MR_s01p, MR_C01)
    RR = sub_position_analysis(RR, RR_s01p, RR_C01)

    FL = sub_velocity_analysis(FL, FL_C01)
    ML = sub_velocity_analysis(ML, ML_C01)
    RL = sub_velocity_analysis(RL, RL_C01)
    FR = sub_velocity_analysis(FR, FR_C01)
    MR = sub_velocity_analysis(MR, MR_C01)
    RR = sub_velocity_analysis(RR, RR_C01)

    FL = sub_mass_force_analysis(FL)
    ML = sub_mass_force_analysis(ML)
    RL = sub_mass_force_analysis(RL)
    FR = sub_mass_force_analysis(FR)
    MR = sub_mass_force_analysis(MR)
    RR = sub_mass_force_analysis(RR)

    K0 = M0h + FL.K1 + ML.K1 + RL.K1 + FR.K1 + MR.K1 + RR.K1
    L0 = Q0h + (FL.L1 + ML.L1 + RL.L1 + FR.L1 + MR.L1 + RR.L1
                - (FL.K1 @ FL.D1 + ML.K1 @ ML.D1 + RL.K1 @ RL.D1 + FR.K1 @ FR.D1 + MR.K1 @ MR.D1 + RR.K1 @ RR.D1)
                # - (FL.Q1h_RSDA + ML.Q1h_RSDA + RL.Q1h_RSDA + FR.Q1h_RSDA + MR.Q1h_RSDA + RR.Q1h_RSDA)
                )

    M = np.zeros((30, 30), dtype=np.float64)
    M[0:6, 0:6] = np.eye(6, dtype=np.float64)
    M[6:10, 6:10] = FL.M
    M[10:14, 10:14] = ML.M
    M[14:18, 14:18] = RL.M
    M[18:22, 18:22] = FR.M
    M[22:26, 22:26] = MR.M
    M[26:30, 26:30] = RR.M

    Q = np.zeros(30, dtype=np.float64)
    Q[0:6] = np.zeros(6, dtype=np.float64)
    Q[6:30] = np.concatenate([FL.Q, ML.Q, RL.Q, FR.Q, MR.Q, RR.Q])

    ddq = np.linalg.solve(M, Q)
    cuts = [3, 6, 10, 14, 18, 22, 26]
    (ddr0, dw0, FL.ddq, ML.ddq, RL.ddq, FR.ddq, MR.ddq, RR.ddq) = np.split(ddq, cuts)
    dY0h = ddq[0:6]

    dp0 = 0.5 * E0.T @ w0

    T0 = np.vstack([
        np.column_stack([np.eye(3), -r0t]),
        np.column_stack([np.zeros((3, 3)), np.eye(3)])
    ])

    R0 = np.concatenate([dr0t @ w0, np.zeros(3)])
    dY0b = T0 @ dY0h - R0

    ddr0 = dY0b[0:3]
    dw0 = dY0b[3:6]
    dw0t = skew(dw0)
    ddr0c = ddr0 + dw0t @ rho0 + w0t @ w0t @ rho0

    FL = sub_acceleration_analysis(FL)
    ML = sub_acceleration_analysis(ML)
    RL = sub_acceleration_analysis(RL)
    FR = sub_acceleration_analysis(FR)
    MR = sub_acceleration_analysis(MR)
    RR = sub_acceleration_analysis(RR)

    Yp = np.zeros(61, dtype=np.float64)
    Yp[0:13] = np.concatenate([dr0, dp0, ddr0, dw0])
    Yp[13:21] = np.concatenate([FL.dq, FL.ddq])
    Yp[21:29] = np.concatenate([ML.dq, ML.ddq])
    Yp[29:37] = np.concatenate([RL.dq, RL.ddq])
    Yp[37:45] = np.concatenate([FR.dq, FR.ddq])
    Yp[45:53] = np.concatenate([MR.dq, MR.ddq])
    Yp[53:61] = np.concatenate([RR.dq, RR.ddq])

    return Yp