#pragma once

#include <iostream>
#include <Eigen/Dense>

#if defined(__GNUC__) || defined(__clang__)
  #define FORCE_INLINE inline __attribute__((always_inline))
#elif defined(_MSC_VER)
  #define FORCE_INLINE __forceinline
#else
  #define FORCE_INLINE inline
#endif

FORCE_INLINE Eigen::Matrix3d skew(const Eigen::Vector3d &v){
    const double vx = v[0];
    const double vy = v[1];
    const double vz = v[2];

    Eigen::Matrix3d S;
    S(0,0) = 0.0; S(0,1) = -vz; S(0,2) =  vy;
    S(1,0) =  vz; S(1,1) = 0.0; S(1,2) = -vx;
    S(2,0) = -vy; S(2,1) =  vx; S(2,2) = 0.0;
    
    return S;
}

FORCE_INLINE Eigen::Matrix3d euler_zxz(double psi, double theta, double phi){
    Eigen::Matrix3d mat_psi, mat_theta, mat_phi, mat;

    mat_psi << cos(psi), -sin(psi), 0, sin(psi), cos(psi), 0, 0, 0, 1;
    mat_theta << 1, 0, 0, 0, cos(theta), -sin(theta), 0, sin(theta), cos(theta);
    mat_phi << cos(phi), -sin(phi), 0, sin(phi), cos(phi), 0, 0, 0, 1;

    mat = mat_psi*mat_theta*mat_phi;

    return mat;
}

FORCE_INLINE Eigen::Vector3d mat2rpy(const Eigen::Matrix3d &mat){
    double pitch = -asin(mat(2,0));
    double roll = atan2(mat(2,1), mat(2,2));
    double yaw = atan2(mat(1,0), mat(0,0));

    Eigen::Vector3d rpy(roll, pitch, yaw);
    return rpy;
}