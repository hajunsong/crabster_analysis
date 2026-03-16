#pragma once

#include <Eigen/Dense>
#include <iostream>
#include <fstream>
#include <vector>
#include <array>

#include "basebody.h"
#include "subsystem.h"

const int Y_SIZE = 21; // 3 + 4 + 3 + 3 + 4 + 4(r0, p0, dr0, w0, q, dq), 1/6 model
const int EQM_SIZE = 10; // 6 + 4, 1/6 model
const int N_SUB = 1;
const int N_BODY = 4;

class Simulation : public BaseBody{
public:
    Simulation();
    ~Simulation();
    void run();
private:
    double t_c, t_e, dt;
    int step;
    double g;

    SubsystemLeft FL;//, ML, RL;
    // SubsystemRight FR, MR, RR;
	std::vector<Subsystem> sub;

	std::vector<double> RSDA_K, RSDA_C;
	double contact_K, contact_C;
	double road_h, pen_z, pen_dz, contact_force;

	Vector<double, Y_SIZE> Y, Yp;

	Matrix<double, EQM_SIZE, EQM_SIZE> M;
	Vector<double, EQM_SIZE> Q, ddq;

	Vector<double, Y_SIZE> k1, k2, k3, k4;
	Vector<double, Y_SIZE> y2, y3, y4;

	Vector<double, Y_SIZE> Y_next;
	double t_next;

	std::vector<std::vector<double>> log;

    void define_Y_vector();

	Eigen::Vector<double, Y_SIZE> analysis(Eigen::Vector<double, Y_SIZE> Y);
	void Y2qdq(Eigen::Vector<double, Y_SIZE> Y);

	void base_position_analysis();
	void base_velocity_analysis();

	void sub_position_analysis(Subsystem &sub);
	void sub_velocity_analysis(Subsystem &sub);
	
	void sub_mass_force_analysis(Subsystem &sub);

	void base_mass_force_analysis();

	void EQM();

	void base_acceleration_analysis();

	void sub_acceleration_analysis(Subsystem &sub);

	Eigen::Vector<double, Y_SIZE> dqddq2Yp();

	inline void write_csv(const std::string& path, const std::vector<std::vector<double>>& rows)
	{
		std::ofstream ofs(path);
		for (const auto& r : rows) {
			for (size_t i = 0; i < r.size(); ++i) {
				ofs << r[i];
				if (i + 1 < r.size()) ofs << ",";
			}
			ofs << "\n";
		}
	}
};
