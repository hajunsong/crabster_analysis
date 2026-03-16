#pragma once

#include <Eigen/Dense>
#include <iostream>
#include "utils.h"
#include "basebody.h"

using namespace Eigen;

using Vector6d = Matrix<double, 6, 1>;
using Matrix6d = Matrix<double, 6, 6>;

class Subsystem
{
public:
	Vector4d q, dq, ddq, q_init;

	Body body[4];

	Vector3d re, rpy, dre;
	Matrix3d Ae;

	Matrix4d M;
	Vector4d Q;
	Matrix<double, 6, 4> Myq;
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
