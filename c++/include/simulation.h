#pragma once

#include <Eigen/Dense>
#include <iostream>
#include <memory>

#include "basebody.h"
#include "subsystem.h"

class Simulation : public BaseBody{
public:
    Simulation();
    ~Simulation();
    void run();
private:
    double t_c, t_e, dt;
    int step;
    double g;

    SubsystemLeft FL, ML, RL;
    SubsystemRight FR, MR, RR;

    Eigen::VectorXd Y, Yp;

    void define_Y_vector();

    void anlaysis();
        void Y2qdq();

        void base_position_analysis();
        void base_velocity_analysis();
        
        void sub_position_analysis();
        void sub_velocity_analysis();
        void sub_mass_force_analysis();
        
        void base_mass_force_analysis();

        void EQM();

        void base_acceleration_analysis();

        void sub_acceleration_analysis();

        void dqddq2Yp();
};