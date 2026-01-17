#pragma once

#include <Eigen/Dense>
#include <iostream>
#include "utils.h"

using namespace Eigen;

using Vector6d = Matrix<double, 6, 1>;
using Matrix6d = Matrix<double, 6, 6>;

class Subsystem
{
public:
	Vector4d q, dq, ddq, q_init;
	double m1, m2, m3, m4;

	Matrix3d J1p, J2p, J3p, J4p;
	Vector3d rho1p, rho2p, rho3p, rho4p;
	Matrix3d C11, C22, C33, C44;
	Vector3d u_vec1, u_vec2, u_vec3, u_vec4;
	Vector3d s01p, s12p, s23p, s34p, s4ep;
	Matrix3d C01, C12, C23, C34, C4e;

	Matrix3d A01pp, A12pp, A23pp, A34pp;
	Matrix3d A1, A2, A3, A4, Ae;
	Vector3d s01, s12, s23, s34;
	Vector3d r1, r2, r3, r4;
	Vector3d rho1, rho2, rho3, rho4;
	Vector3d r1c, r2c, r3c, r4c;
	Vector3d s4e, re, rpy;

	Vector3d H1, H2, H3, H4;
	Vector3d w1, w2, w3, w4;
	Matrix3d w1t, w2t, w3t, w4t;
	Vector3d dr1, dr2, dr3, dr4, dre;
	Matrix3d r1t, r2t, r3t, r4t;
	Vector6d B1, B2, B3, B4;
	Matrix3d dr1t, dr2t, dr3t, dr4t;
	Vector3d dr1c, dr2c, dr3c, dr4c;
	Vector3d dH1, dH2, dH3, dH4;
	Vector6d D1, D2, D3, D4;
	Vector6d Y1h, Y2h, Y3h, Y4h;

	Matrix3d A1_C11, A2_C22, A3_C33, A4_C44;
	Matrix3d J1c, J2c, J3c, J4c;
	Matrix3d r1ct, r2ct, r3ct, r4ct;
	Matrix3d dr1ct, dr2ct, dr3ct, dr4ct;
	Vector3d f1c, f2c, f3c, f4c, t1c, t2c, t3c, t4c;
	Matrix3d M1h_11, M1h_12, M1h_22;
	Matrix3d M2h_11, M2h_12, M2h_22;
	Matrix3d M3h_11, M3h_12, M3h_22;
	Matrix3d M4h_11, M4h_12, M4h_22;
	Matrix6d M1h, M2h, M3h, M4h;
	Vector6d Q1h, Q2h, Q3h, Q4h;
	Matrix6d K1, K2, K3, K4;
	Vector6d L1, L2, L3, L4;
	Matrix4d M;
	Vector4d Q;
	Matrix<double, 6, 4> Myq;

	Vector6d dY1h, dY2h, dY3h, dY4h;
	Matrix6d T1, T2, T3, T4;
	Matrix6d dT1, dT2, dT3, dT4;
	Vector6d R1, R2, R3, R4;
	Vector6d dY1b, dY2b, dY3b, dY4b;
	Vector3d ddr1, ddr2, ddr3, ddr4;
	Vector3d dw1, dw2, dw3, dw4;
	Matrix3d dw1t, dw2t, dw3t, dw4t;
	Vector3d ddr1c, ddr2c, ddr3c, ddr4c;
};

class SubsystemLeft : public Subsystem
{
public:
	SubsystemLeft(const Vector3d &s01p, const Matrix3d &C01);
	virtual ~SubsystemLeft() = default;
};

class SubsystemRight : public Subsystem
{
public:
	SubsystemRight(const Vector3d &s01p, const Matrix3d &C01);
	virtual ~SubsystemRight() = default;
};
