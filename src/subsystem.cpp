#pragma once

#include "subsystem.h"

SubsystemLeft::SubsystemLeft(const Eigen::Vector3d &s01p, const Eigen::Matrix3d &C01){
    q.setZero();
    dq.setZero();
    ddq.setZero();
    q_init.setZero();

    body[0].sijp = s01p;
    body[0].Cij = C01;

    body[0].mi = 3.6;
    body[0].Jip << 24217.363, 1.142, -4.718,
           1.142, 22602.121, 3.656,
           -4.718, 3.656, 24383.284;
    body[0].Jip *= 1e-6;
    body[0].rhoip = Eigen::Vector3d(19.41, 0, 0)*1e-3;
    body[0].Cii = euler_zxz(M_PI, M_PI_2, M_PI_2);
    body[0].u_vec = Eigen::Vector3d::UnitZ();

    body[1].sijp = Eigen::Vector3d(120, 0, 0)*1e-3;
    body[1].Cij = euler_zxz(-M_PI_2, M_PI_2, M_PI_2);

    body[1].mi = 12.9;
    body[1].Jip << 101693.397, -54.639, -3.734,
           -54.639, 43784.882, 3156.796,
           -3.734, 3156.796, 101586.518;
    body[1].Jip *= 1e-6;
    body[1].rhoip = Eigen::Vector3d(0, 0, -101.13)*1e-3;
    body[1].Cii = euler_zxz(M_PI, M_PI_2, M_PI);
    body[1].u_vec = Eigen::Vector3d::UnitZ();

    body[2].sijp = Eigen::Vector3d(0, 0, -121)*1e-3;
    body[2].Cij = euler_zxz(M_PI, M_PI_2, M_PI);

    body[2].mi = 11.1;
    body[2].Jip << 172022.706, 939.804, 39.970,
           939.804, 67557.291, 151.395,
           39.970, 151.395, 155965.608;
    body[2].Jip *= 1e-6;
    body[2].rhoip = Eigen::Vector3d(0, 238.39, -1.08)*1e-3;
    body[2].Cii = euler_zxz(0, 0, 0);
    body[2].u_vec = Eigen::Vector3d::UnitZ();

    body[3].sijp = Eigen::Vector3d(0, 509, 0)*1e-3;
    body[3].Cij = euler_zxz(M_PI_2, M_PI_2, 0);

    body[3].mi = 11.5;
    body[3].Jip << 686629.019, 10499.954, 1652.691,
           10499.954, 44753.249, -23952.157,
           1652.691, -23952.157, 705784.865;
    body[3].Jip *= 1e-6;
    body[3].rhoip = Eigen::Vector3d(322.25, 51.84, 0)*1e-3;
    body[3].Cii = euler_zxz(M_PI, M_PI_2, M_PI_2);
    body[3].u_vec = Eigen::Vector3d::UnitZ();

    body[3].sep = Eigen::Vector3d(823.56, 0, 0)*1e-3;
    body[3].Ce = euler_zxz(M_PI, M_PI_2, M_PI_2);
}

SubsystemRight::SubsystemRight(const Eigen::Vector3d &s01p, const Eigen::Matrix3d &C01){
    q.setZero();
    dq.setZero();
    ddq.setZero();
    q_init.setZero();

    this->body[0].sijp = s01p;
    this->body[0].Cij = C01;

    body[0].mi = 3.6;
    body[0].Jip << 24217.36, 1.142, 4.718,
           1.142, 22602.121, -3.656,
           4.718, -3.656, 24383.284;
    body[0].Jip *= 1e-6;
    body[0].rhoip = Eigen::Vector3d(-19.41, 0, 0)*1e-3;
    body[0].Cii = euler_zxz(M_PI, M_PI_2, M_PI_2);
    body[0].u_vec = Eigen::Vector3d::UnitZ();

    body[1].sijp = Eigen::Vector3d(-120, 0, 0)*1e-3;
    body[1].Cij = euler_zxz(-M_PI_2, M_PI_2, M_PI_2);

    body[1].mi = 12.9;
    body[1].Jip << 101693.397, 54.639, 3.734,
           54.639, 43784.882, -3156.796,
           3.734, -3156.796, 101586.518;
    body[1].Jip *= 1e-6;
    body[1].rhoip = Eigen::Vector3d(0, 0, 101.13)*1e-3;
    body[1].Cii = euler_zxz(M_PI, M_PI_2, M_PI);
    body[1].u_vec = Eigen::Vector3d::UnitZ();

    body[2].sijp = Eigen::Vector3d(0, 0, 121)*1e-3;
    body[2].Cij = euler_zxz(M_PI, M_PI_2, M_PI);

    body[2].mi = 11.1;
    body[2].Jip << 172022.706, 939.804, -39.970,
           939.804, 67557.291, -151.395,
           -39.970, -151.395, 155965.608;
    body[2].Jip *= 1e-6;
    body[2].rhoip = Eigen::Vector3d(0, -238.39, -1.08)*1e-3;
    body[2].Cii = euler_zxz(0, 0, 0);
    body[2].u_vec = Eigen::Vector3d::UnitZ();

    body[3].sijp = Eigen::Vector3d(0, -509, 0)*1e-3;
    body[3].Cij = euler_zxz(M_PI_2, M_PI_2, 0);

    body[3].mi = 11.5;
    body[3].Jip << 686629.019, 10499.954, -1652.691,
           10499.954, 44753.249, 23952.157,
           -1652.691, 23952.157, 705784.865;
    body[3].Jip *= 1e-6;
    body[3].rhoip = Eigen::Vector3d(-322.25, 51.84, 0)*1e-3;
    body[3].Cii = euler_zxz(M_PI, M_PI_2, M_PI_2);
    body[3].u_vec = Eigen::Vector3d::UnitZ();

    body[3].sep = Eigen::Vector3d(-823.56, 0, 0)*1e-3;
    body[3].Ce = euler_zxz(M_PI, M_PI_2, M_PI_2);
}
