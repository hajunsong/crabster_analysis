#pragma once

#include <Eigen/Dense>
#include <iostream>
#include "utils.h"

using namespace Eigen;

using Vector6d = Matrix<double, 6, 1>;
using Matrix6d = Matrix<double, 6, 6>;

typedef struct BodyStruct{
	double mi;

	Vector4d pi;
	Matrix<double, 3, 4> Ei, Gi;
	Vector3d rpy;

	Matrix3d Cij, Aijpp, Ai, Jip, Cii, Ce;
	Vector3d sijp, sij, ri, u_vec, rhoip, rhoi, ric, sep, se;

	Vector3d Hi, wi, dri, dric, dHi;
	Matrix3d wit, rit, drit;
	Vector6d Bi, Di, Yih;

	Matrix3d Ai_Cii, Jic, rict, drict;
	Vector3d fic, tic;

	Matrix3d Mih_11, Mih_12, Mih_22;
	Matrix6d Mih, Ki;
	Vector6d Qih, Li, Qijh_RSDA, Qjih_RSDA, Qih_contact;
	Vector3d r4cp;
	Matrix3d r4cpt;
	double Ti_RSDA;

	Vector6d dYih, Ri, dYib;
	Matrix6d Ti, dTi;
	Vector3d ddri, dwi, ddric;
	Matrix3d dwit;
	Vector4d dpi;
} Body;

class BaseBody{
public:
    BaseBody();
    ~BaseBody();

	Body base;

	Vector3d FL_s01p, ML_s01p, RL_s01p, FR_s01p, MR_s01p, RR_s01p;
	Matrix3d FL_C01, ML_C01, RL_C01, FR_C01, MR_C01, RR_C01;
};
