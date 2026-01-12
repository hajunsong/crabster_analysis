#pragma once

#include <Eigen/Dense>
#include <iostream>
#include "utils.h"

using namespace Eigen;

using Vector6d = Matrix<double, 6, 1>;
using Matrix6d = Matrix<double, 6, 6>;

class BaseBody{
public:
    BaseBody();
    ~BaseBody();

	Vector3d r0;
	Matrix3d A0;
	Vector4d p0;
	Matrix<double, 3, 4> E0, G0;
	Vector3d rpy0;
	Vector3d rho0p;
	Vector3d rho0, r0c;

	Vector3d dr0, w0;
	Matrix3d w0t;
	Matrix3d r0t;
	Matrix3d dr0t;
	Vector3d dr0c;

    double m0;
	Matrix3d J0p;
	Matrix3d C00;

	Vector3d FL_s01p, ML_s01p, RL_s01p, FR_s01p, MR_s01p, RR_s01p;
	Matrix3d FL_C01, ML_C01, RL_C01, FR_C01, MR_C01, RR_C01;

	Vector6d Y0h, dY0h, dY0b;

	Matrix3d A0_C00, J0c;
	Matrix3d r0ct, dr0ct;
	Vector3d f0c, t0c;
	Matrix3d M0h_11, M0h_12, M0h_22;
	Matrix6d M0h;
	Vector6d Q0h;

	Matrix6d K0;
	Vector6d L0;

	Vector4d dp0;
	Vector3d ddr0, dw0;
	Matrix3d dw0t;

	Matrix6d T0;
	Vector6d R0;

	Vector3d ddr0c;
};
