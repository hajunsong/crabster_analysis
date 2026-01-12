#pragma once

#include <Eigen/Dense>
#include <iostream>
#include "utils.h"

using Vector6d = Eigen::Matrix<double, 6, 1>;
using Matrix6d = Eigen::Matrix<double, 6, 6>;

class BaseBody{
public:
    BaseBody();
    ~BaseBody();

    Eigen::Vector3d r0;
    Eigen::Matrix3d A0;
    Eigen::Vector4d p0;
    Eigen::Matrix<double, 3, 4> E0, G0;

    Eigen::Vector3d dr0, w0;
    Eigen::Matrix3d w0t;

    double m0;
    Eigen::Matrix3d J0p;
    Eigen::Vector3d rho0p;
    Eigen::Matrix3d C00;

    Eigen::Vector3d FL_s01p, ML_s01p, RL_s01p, FR_s01p, MR_s01p, RR_s01p;
    Eigen::Matrix3d FL_C01, ML_C01, RL_C01, FR_C01, MR_C01, RR_C01;

    Vector6d Y0h, dY0h, dY0b;

    Eigen::Vector4d dp0;
    Eigen::Vector3d ddr0, dw0;
};