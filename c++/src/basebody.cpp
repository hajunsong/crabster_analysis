#include "basebody.h"

BaseBody::BaseBody(){
    r0.setZero();
    A0.setIdentity();
	p0 = Vector4d(1, 0, 0, 0);

    dr0.setZero();
    w0.setZero();
    w0t.setZero();

    m0 = 582.59;
    J0p << 156890393.0, 0.0, 0.0,
            0.0, 150169673.0, 0.0,
            0.0, 0.0, 249303699.0;
    J0p *= 1e-6;

    rho0p.setZero();
    C00 = euler_zxz(0, 0, 0);

	FL_s01p = Vector3d(520, 758, 0)*1e-3;
    FL_C01 = euler_zxz(M_PI_2, M_PI_2, 0.0);
	ML_s01p = Vector3d(0, 858, 0)*1e-3;
    ML_C01 = euler_zxz(M_PI_2, M_PI_2, 0.0);
	RL_s01p = Vector3d(-520, 758, 0)*1e-3;
    RL_C01 = euler_zxz(M_PI_2, M_PI_2, 0.0);
	FR_s01p = Vector3d(520, -758, 0)*1e-3;
    FR_C01 = euler_zxz(M_PI_2, M_PI_2, 0.0);
	MR_s01p = Vector3d(0, -858, 0)*1e-3;
    MR_C01 = euler_zxz(M_PI_2, M_PI_2, 0.0);
	RR_s01p = Vector3d(-520, -758, 0)*1e-3;
    RR_C01 = euler_zxz(M_PI_2, M_PI_2, 0.0);

    Y0h.setZero();
    dY0h.setZero();
    dY0b.setZero();
}

BaseBody::~BaseBody(){

}
