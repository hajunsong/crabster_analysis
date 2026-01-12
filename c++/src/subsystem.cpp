#pragma once

#include "subsystem.h"

SubsystemLeft::SubsystemLeft(const Eigen::Vector3d &s01p, const Eigen::Matrix3d &C01){
    q.setZero();
    dq.setZero();
    ddq.setZero();
    q_init.setZero();

    this->s01p = s01p;
    this->C01 = C01;

    m1 = 3.6;
    J1p << 24217.363, 1.142, -4.718,
           1.142, 22602.121, 3.656,
           -4.718, 3.656, 24383.284;
    J1p *= 1e-6;
    rho1p = Eigen::Vector3d(19.41, 0, 0)*1e-3;
    C11 = euler_zxz(M_PI, M_PI_2, M_PI_2);
    u_vec1 = Eigen::Vector3d::UnitZ();

    s12p = Eigen::Vector3d(120, 0, 0)*1e-3;
    C12 = euler_zxz(-M_PI_2, M_PI_2, M_PI_2);

    m2 = 12.9;
    J2p << 101693.397, -54.639, -3.734,
           -54.639, 43784.882, 3156.796,
           -3.734, 3156.796, 101586.518;
    J2p *= 1e-6;
    rho2p = Eigen::Vector3d(0, 0, -101.13)*1e-3;
    C22 = euler_zxz(M_PI, M_PI_2, M_PI);
    u_vec2 = Eigen::Vector3d::UnitZ();

    s23p = Eigen::Vector3d(0, 0, -121)*1e-3;
    C23 = euler_zxz(M_PI, M_PI_2, M_PI);

    m3 = 11.1;
    J3p << 172022.706, 939.804, 39.970,
           939.804, 67557.291, 151.395,
           39.970, 151.395, 155965.608;
    J3p *= 1e-6;
	rho3p = Eigen::Vector3d(0, 238.39, -1.08)*1e-3;
    C33 = euler_zxz(0, 0, 0);
    u_vec3 = Eigen::Vector3d::UnitZ();

    s34p = Eigen::Vector3d(0, 509, 0)*1e-3;
    C34 = euler_zxz(M_PI_2, M_PI_2, 0);

    m4 = 11.5;
    J4p << 686629.019, 10499.954, 1652.691,
           10499.954, 44753.249, -23952.157,
           1652.691, -23952.157, 705784.865;
    J4p *= 1e-6;
    rho4p = Eigen::Vector3d(322.25, 51.84, 0)*1e-3;
    C44 = euler_zxz(M_PI, M_PI_2, M_PI_2);
    u_vec4 = Eigen::Vector3d::UnitZ();

    s4ep = Eigen::Vector3d(823.56, 0, 0)*1e-3;
    C4e = euler_zxz(M_PI, M_PI_2, M_PI_2);
}

SubsystemRight::SubsystemRight(const Eigen::Vector3d &s01p, const Eigen::Matrix3d &C01){
    q.setZero();
    dq.setZero();
    ddq.setZero();
    q_init.setZero();

    this->s01p = s01p;
    this->C01 = C01;

    m1 = 3.6;
    J1p << 24217.36, 1.142, 4.718,
           1.142, 22602.121, -3.656,
           4.718, -3.656, 24383.284;
    J1p *= 1e-6;
    rho1p = Eigen::Vector3d(-19.41, 0, 0)*1e-3;
    C11 = euler_zxz(M_PI, M_PI_2, M_PI_2);
    u_vec1 = Eigen::Vector3d::UnitZ();

    s12p = Eigen::Vector3d(-120, 0, 0)*1e-3;
    C12 = euler_zxz(-M_PI_2, M_PI_2, M_PI_2);

    m2 = 12.9;
    J2p << 101693.397, 54.639, 3.734,
           54.639, 43784.882, -3156.796,
           3.734, -3156.796, 101586.518;
    J2p *= 1e-6;
    rho2p = Eigen::Vector3d(0, 0, 101.13)*1e-3;
    C22 = euler_zxz(M_PI, M_PI_2, M_PI);
    u_vec2 = Eigen::Vector3d::UnitZ();

    s23p = Eigen::Vector3d(0, 0, 121)*1e-3;
    C23 = euler_zxz(M_PI, M_PI_2, M_PI);

    m3 = 11.1;
    J3p << 172022.706, 939.804, -39.970,
           939.804, 67557.291, -151.395,
           -39.970, -151.395, 155965.608;
    J3p *= 1e-6;
	rho3p = Eigen::Vector3d(0, -238.39, -1.08)*1e-3;
    C33 = euler_zxz(0, 0, 0);
    u_vec3 = Eigen::Vector3d::UnitZ();

    s34p = Eigen::Vector3d(0, -509, 0)*1e-3;
    C34 = euler_zxz(M_PI_2, M_PI_2, 0);

    m4 = 11.5;
    J4p << 686629.019, 10499.954, -1652.691,
           10499.954, 44753.249, 23952.157,
           -1652.691, 23952.157, 705784.865;
    J4p *= 1e-6;
    rho4p = Eigen::Vector3d(-322.25, 51.84, 0)*1e-3;
    C44 = euler_zxz(M_PI, M_PI_2, M_PI_2);
    u_vec4 = Eigen::Vector3d::UnitZ();

    s4ep = Eigen::Vector3d(-823.56, 0, 0)*1e-3;
    C4e = euler_zxz(M_PI, M_PI_2, M_PI_2);
}
