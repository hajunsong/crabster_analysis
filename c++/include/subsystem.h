#pragma once

#include <Eigen/Dense>
#include <iostream>
#include "utils.h"

using Vector6d = Eigen::Matrix<double, 6, 1>;
using Matrix6d = Eigen::Matrix<double, 6, 6>;

class SubsystemLeft
{
public:
    SubsystemLeft(const Eigen::Vector3d &s01p, const Eigen::Matrix3d &C01);
    virtual ~SubsystemLeft() = default;
    // double q[4], dq[4], ddq[4], q_init[4];
    Eigen::Vector4d q, dq, ddq, q_init;
    double m1, m2, m3, m4;

    Eigen::Matrix3d J1p, J2p, J3p, J4p;
    Eigen::Vector3d rho1p, rho2p, rho3p, rho4p;
    Eigen::Matrix3d C11, C22, C33, C44;
    Eigen::Vector3d u_vec1, u_vec2, u_vec3, u_vec4;
    Eigen::Vector3d s01p, s12p, s23p, s34p, s4ep;
    Eigen::Matrix3d C01, C12, C23, C34, C4e;
};

class SubsystemRight
{
public:
    SubsystemRight(const Eigen::Vector3d &s01p, const Eigen::Matrix3d &C01);
    virtual ~SubsystemRight() = default;
    // double q[4], dq[4], ddq[4], q_init[4];
    Eigen::Vector4d q, dq, ddq, q_init;
    double m1, m2, m3, m4;

    Eigen::Matrix3d J1p, J2p, J3p, J4p;
    Eigen::Vector3d rho1p, rho2p, rho3p, rho4p;
    Eigen::Matrix3d C11, C22, C33, C44;
    Eigen::Vector3d u_vec1, u_vec2, u_vec3, u_vec4;
    Eigen::Vector3d s01p, s12p, s23p, s34p, s4ep;
    Eigen::Matrix3d C01, C12, C23, C34, C4e;
};