#include "basebody.h"

BaseBody::BaseBody(){
    base.ri.setZero();
    base.Ai.setIdentity();
	base.pi = Vector4d(1, 0, 0, 0);

    base.dri.setZero();
    base.wi.setZero();
    base.wit.setZero();

    base.mi = 582.59/6.0;
    base.Jip << 156890393.0, 0.0, 0.0,
            0.0, 150169673.0, 0.0,
            0.0, 0.0, 249303699.0;
    base.Jip *= 1e-6;
    base.Jip /= 6.0;

    base.rhoip.setZero();
    base.Cii = euler_zxz(0, 0, 0);

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

    base.Yih.setZero();
    base.dYih.setZero();
    base.dYib.setZero();
}

BaseBody::~BaseBody(){

}
