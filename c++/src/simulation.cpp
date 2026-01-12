#include "simulation.h"

Simulation::Simulation() : 
            FL(FL_s01p, FL_C01), ML(ML_s01p, ML_C01), RL(RL_s01p, RL_C01),
            FR(FR_s01p, FR_C01), MR(MR_s01p, MR_C01), RR(RR_s01p, RR_C01)
{
    Y = Eigen::VectorXd::Zero(61);
    Yp = Eigen::VectorXd::Zero(61);
}

Simulation::~Simulation(){
}

void Simulation::define_Y_vector(){
    Y << r0, p0, dr0, w0,
        FL.q_init, FL.dq, ML.q_init, ML.dq, RL.q_init, RL.dq,
        FR.q_init, FR.dq, MR.q_init, MR.dq, RR.q_init, RR.dq;
}

void Simulation::Y2qdq()
{
    r0 = Y.segment<3>(0);
    p0 = Y.segment<4>(3);
    dr0 = Y.segment<3>(7);
    w0 = Y.segment<3>(10);

    FL.q = Y.segment<4>(13);
    FL.dq = Y.segment<4>(17);
    ML.q = Y.segment<4>(21);
    ML.dq = Y.segment<4>(25);
    RL.q = Y.segment<4>(29);
    RL.dq = Y.segment<4>(33);
    
    FR.q = Y.segment<4>(37);
    FR.dq = Y.segment<4>(41);
    MR.q = Y.segment<4>(45);
    MR.dq = Y.segment<4>(49);
    RR.q = Y.segment<4>(53);
    RR.dq = Y.segment<4>(57);
}

void Simulation::dqddq2Yp()
{
    Yp << dr0, dp0, ddr0, dw0,
        FL.dq, FL.ddq, ML.dq, ML.ddq, RL.dq, RL.ddq,
        FR.dq, FR.ddq, MR.dq, MR.ddq, RR.dq, RR.ddq;
}

void Simulation::run(){
    t_c = 0;
    t_e = 2;
    dt = 0.001;

    g = -9.80665;

    Eigen::Vector4d L_q_init(M_PI_4, 0, 0, -M_PI_4*3);
    Eigen::Vector4d R_q_init(-M_PI_4, 0, 0,  M_PI_4*3);

    FL.q_init = L_q_init;
    ML.q_init = L_q_init;
    RL.q_init = L_q_init;
    FR.q_init = R_q_init;
    MR.q_init = R_q_init;
    RR.q_init = R_q_init;

    define_Y_vector();

    // while(t_c <= t_e)
    {
        anlaysis();
    }
}

void Simulation::anlaysis()
{
    Y2qdq();

    void base_position_analysis();
    void base_velocity_analysis();
    
    void sub_position_analysis();
    void sub_velocity_analysis();
    void sub_mass_force_analysis();
    
    void base_mass_force_analysis();

    void EQM();

    void base_acceleration_analysis();

    void sub_acceleration_analysis();

    dqddq2Yp();
}

void Simulation::base_position_analysis()
{
    double q0 = p0[0];
    Eigen::Vector3d qv = p0.segment<3>(1);
    Eigen::Matrix3d S = skew(qv);
    Eigen::Matrix3d I = Eigen::Matrix3d::Identity();

    E0.col(0) = -qv;
    E0.block<3,3>(0,1) = S + q0*I;
}

void Simulation::base_velocity_analysis()
{
}

void Simulation::sub_position_analysis()
{
}

void Simulation::sub_velocity_analysis()
{
}

void Simulation::sub_mass_force_analysis()
{
}

void Simulation::base_mass_force_analysis()
{
}

void Simulation::EQM()
{
}

void Simulation::base_acceleration_analysis()
{
}

void Simulation::sub_acceleration_analysis()
{
}
