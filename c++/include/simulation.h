#pragma once

#include <Eigen/Dense>
#include <iostream>
#include <fstream>
#include <vector>
#include <array>

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

	VectorXd Y, Yp;

	Matrix<double, 30, 30> M;
	Vector<double, 30> Q, ddq;

	Vector<double, 61> k1, k2, k3, k4;
	Vector<double, 61> y2, y3, y4;

	Vector<double, 61> Y_next;
	double t_next;

	std::vector<std::vector<double>> log;

    void define_Y_vector();

	Eigen::Vector<double, 61> analysis(Eigen::Vector<double, 61> Y);
	void Y2qdq(Eigen::Vector<double, 61> Y);

	void base_position_analysis();
	void base_velocity_analysis();

	void sub_position_analysis(Subsystem &sub);
	void sub_velocity_analysis(Subsystem &sub);
	void sub_mass_force_analysis(Subsystem &sub);

	void base_mass_force_analysis();

	void EQM();

	void base_acceleration_analysis();

	void sub_acceleration_analysis(Subsystem &sub);

	Eigen::Vector<double, 61> dqddq2Yp();

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
