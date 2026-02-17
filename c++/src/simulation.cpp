#include "simulation.h"

Simulation::Simulation() : FL(FL_s01p, FL_C01)
{
	Y = VectorXd::Zero(Y_SIZE);
	Yp = VectorXd::Zero(Y_SIZE);

	sub.push_back(FL);
}

Simulation::~Simulation(){
}

void Simulation::define_Y_vector(){
    // Y << r0, p0, dr0, w0,
    //     FL.q_init, FL.dq, ML.q_init, ML.dq, RL.q_init, RL.dq,
    //     FR.q_init, FR.dq, MR.q_init, MR.dq, RR.q_init, RR.dq;
	Y << base.ri, base.pi, base.dri, base.wi, sub[0].q_init, sub[0].dq;
}

void Simulation::Y2qdq(Eigen::Vector<double, Y_SIZE> Y)
{
    base.ri = Y.segment<3>(0);
    base.pi = Y.segment<4>(3);
    base.dri = Y.segment<3>(7);
    base.wi = Y.segment<3>(10);

    sub[0].q = Y.segment<4>(13);
    sub[0].dq = Y.segment<4>(17);
    // ML.q = Y.segment<4>(21);
    // ML.dq = Y.segment<4>(25);
    // RL.q = Y.segment<4>(29);
    // RL.dq = Y.segment<4>(33);
    
    // FR.q = Y.segment<4>(37);
    // FR.dq = Y.segment<4>(41);
    // MR.q = Y.segment<4>(45);
    // MR.dq = Y.segment<4>(49);
    // RR.q = Y.segment<4>(53);
    // RR.dq = Y.segment<4>(57);
}

Eigen::Vector<double, Y_SIZE> Simulation::dqddq2Yp()
{
    // Yp << dr0, dp0, ddr0, dw0,
    //     FL.dq, FL.ddq, ML.dq, ML.ddq, RL.dq, RL.ddq,
    //     FR.dq, FR.ddq, MR.dq, MR.ddq, RR.dq, RR.ddq;
	Yp << base.dri, base.dpi, base.ddri, base.dwi,
			sub[0].dq, sub[0].ddq;

	return Yp;
}

void Simulation::run(){
    t_c = 0;
    t_e = 2;
    dt = 0.001;
	step = 0;

    g = -9.80665;

	Vector4d L_q_init(M_PI_4, 0, 0, -M_PI_4*3);
	// Vector4d R_q_init(-M_PI_4, 0, 0,  M_PI_4*3);

    sub[0].q_init = L_q_init;
    // ML.q_init = L_q_init;
    // RL.q_init = L_q_init;
    // FR.q_init = R_q_init;
    // MR.q_init = R_q_init;
    // RR.q_init = R_q_init;

	RSDA_K.push_back(15000);
	RSDA_K.push_back(7000);
	RSDA_K.push_back(7000);
	RSDA_K.push_back(7000);

	RSDA_C.push_back(1500);
	RSDA_C.push_back(300);
	RSDA_C.push_back(300);
	RSDA_C.push_back(700);

    define_Y_vector();

	log.reserve(static_cast<size_t>(t_c/dt) + 10);

	while(t_c <= t_e)
    {
		Yp = analysis(Y);

		k1 = Yp;
		y2 = Y + (dt/2.0)*k1;
		k2 = analysis(y2);
		y3 = Y + (dt/2.0)*k2;
		k3 = analysis(y3);
		y4 = Y + dt*k3;
		k4 = analysis(y4);
		Y_next = Y + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4);
		t_next = t_c + dt;

		std::vector<double> row;

		row.push_back(static_cast<double>(step));
		row.push_back(t_c);

		row.insert(row.end(), sub[0].re.data(), sub[0].re.data() + 3);
		row.insert(row.end(), sub[0].rpy.data(), sub[0].rpy.data() + 3);
		row.insert(row.end(), {sub[0].q[0], sub[0].q[1], sub[0].q[2], sub[0].q[3]});
		row.insert(row.end(), {sub[0].dq[0], sub[0].dq[1], sub[0].dq[2], sub[0].dq[3]});
		row.insert(row.end(), {sub[0].ddq[0], sub[0].ddq[1], sub[0].ddq[2], sub[0].ddq[3]});

		log.push_back(std::move(row));

		std::cout << "t_c : " << t_c << std::endl;

		t_c = t_next;
		step++;
		Y = Y_next;
    }

	const std::string out_csv = "data/sim_data.csv";
	write_csv(out_csv, log);
	std::cout << "[OK] saved: " << out_csv << "  rows=" << log.size() << "\n";
}

Eigen::Vector<double, Y_SIZE> Simulation::analysis(Eigen::Vector<double, Y_SIZE> Y)
{
	Y2qdq(Y);

    base_position_analysis();
    base_velocity_analysis();

	for(Subsystem &s : sub){
		sub_position_analysis(s);
		sub_velocity_analysis(s);
	}

	// for(int i = 0; i < N_SUB; i++){
	// 	sub_position_analysis(&sub[i]);
	// 	sub_velocity_analysis(&sub[i]);
	// }

	for(Subsystem &s : sub){
		sub_mass_force_analysis(s);
	}

	// for(int i = 0; i < N_SUB; i++){
	// 	sub_mass_force_analysis(&sub[i]);
	// }
    
    base_mass_force_analysis();

    EQM();

    base_acceleration_analysis();

	for(Subsystem &s : sub){
		sub_acceleration_analysis(s);
	}
	// for(int i = 0; i < N_SUB; i++){
	// 	sub_acceleration_analysis(&sub[i]);
	// }

	Yp = dqddq2Yp();

	return Yp;
}

void Simulation::base_position_analysis()
{
    double q = base.pi[0];
	Vector3d qv = base.pi.segment<3>(1);
	Matrix3d S = skew(qv);
	Matrix3d I = Eigen::Matrix3d::Identity();

    // E0 = [-qv, S + q0*I]
    base.Ei.col(0) = -qv;
    base.Ei.block<3,3>(0,1) = S + q*I;

    // G0 = [-qv, -S + q0*I]
    base.Gi.col(0) = -qv;
    base.Gi.block<3,3>(0,1) = -S + q*I;

	base.Ai = base.Ei*base.Gi.transpose();
	base.rpy = mat2rpy(base.Ai);

	base.rhoi = base.Ai*base.rhoip;
	base.ric = base.ri + base.rhoi;
}

void Simulation::base_velocity_analysis()
{
	base.wit = skew(base.wi);
	base.rit = skew(base.ri);
	base.drit = skew(base.dri);
	base.dric = base.dri + base.wit*base.rhoi;

	base.Yih << base.dri + base.drit*base.wi, base.wi;
}

void Simulation::sub_position_analysis(Subsystem &sub)
{
	int i = 0;
	for(Body &b : sub.body){
		b.Aijpp << cos(sub.q[i]), -sin(sub.q[i]), 0, sin(sub.q[i]), cos(sub.q[i]), 0, 0, 0, 1;
		i++;
	}

	Body *prev = &base;
	for(Body &body : sub.body){
		body.Ai = prev->Ai*body.Cij*body.Aijpp;
		body.sij = prev->Ai*body.sijp;
		body.ri = prev->ri + body.sij;
		body.rhoi = body.Ai*body.rhoip;
		body.ric = body.ri + body.rhoi;
		prev = &body;
	}

	sub.body[3].se = sub.body[3].Ai*sub.body[3].sep;
	sub.re = sub.body[3].ri + sub.body[3].se;
	sub.Ae = sub.body[3].Ai*sub.body[3].Ce;
	sub.rpy = mat2rpy(sub.Ae);
}

void Simulation::sub_velocity_analysis(Subsystem &sub)
{
	int i = 0;
	Body *prev = &base;
	for(Body &body : sub.body){
		body.Hi = prev->Ai*body.Cij*body.u_vec;
		body.wi = prev->wi + body.Hi*sub.dq[i];
		body.wit = skew(body.wi);
		body.dri = prev->dri + prev->wit*body.sij;
		body.rit = skew(body.ri);

		body.Bi << body.rit*body.Hi, body.Hi;
		body.drit = skew(body.dri);
		body.dric = body.dri + body.wit*body.rhoi;
		body.dHi = prev->wit*body.Hi;
		body.Di << body.drit*body.Hi + body.rit*body.dHi, body.dHi;
		body.Di *= sub.dq[i];
		body.Yih = prev->Yih + body.Bi*sub.dq[i];

		prev = &body;
		i++;
	}

	sub.dre = sub.body[3].dri + sub.body[3].wit*sub.body[3].ri;
}

void Simulation::sub_mass_force_analysis(Subsystem &sub)
{
	for(Body &body : sub.body){
		body.Ai_Cii = body.Ai*body.Cii;
		body.Jic = body.Ai_Cii*body.Jip*body.Ai_Cii.transpose();
		body.rict = skew(body.ric);
		body.drict = skew(body.dric);
		
		body.fic = Vector3d(0, 0, body.mi*g);
		body.tic = Vector3d(0, 0, 0);

		body.Mih_11 = body.mi*Matrix3d::Identity();
		body.Mih_12 = -body.mi*body.rict;
		body.Mih_22 = body.Jic - body.mi*body.rict*body.rict;

		body.Mih.block<3, 3>(0, 0) = body.Mih_11;
		body.Mih.block<3, 3>(0, 3) = body.Mih_12;
		body.Mih.block<3, 3>(3, 0) = -body.Mih_12;
		body.Mih.block<3, 3>(3, 3) = body.Mih_22;

		body.Qih << body.fic + body.mi*body.drict*body.wi,
				body.tic + body.rict*body.fic + body.mi*body.rict*body.drict*body.wi - body.wit*body.Jic*body.wi;
	}
		
	// RSDA Force
	for(int i = 0; i < N_BODY; i++){
		sub.body[i].Ti_RSDA = RSDA_K[i]*(sub.q_init[i] - sub.q[i]) - RSDA_C[i]*sub.dq[i];
		sub.body[i].Qijh_RSDA << Vector3d::Zero(), sub.body[i].Ti_RSDA*sub.body[i].Hi;
		sub.body[i].Qjih_RSDA = -sub.body[i].Qijh_RSDA;
		sub.body[i].Qih += sub.body[i].Qijh_RSDA;
	}

	// Contact Force

	// Applied Force

	sub.body[3].Ki = sub.body[3].Mih;
	sub.body[3].Li = sub.body[3].Qih;
	for(int i = 2; i >= 0; --i){
		sub.body[i].Ki = sub.body[i].Mih + sub.body[i + 1].Ki;
		sub.body[i].Li = sub.body[i].Qih + sub.body[i + 1].Li - sub.body[i + 1].Ki*sub.body[i + 1].Di + sub.body[i + 1].Qjih_RSDA;
	}

	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++){
			int k = i > j ? i : j;
			sub.M(i, j) = sub.body[i].Bi.transpose()*sub.body[k].Ki*sub.body[j].Bi;
		}
	}
	Vector6d D_sum = Vector6d::Zero();
	for(int i = 0; i < 4; i++){
		D_sum += sub.body[i].Di;
		sub.Q(i) = sub.body[i].Bi.transpose()*(sub.body[i].Li - sub.body[i].Ki*D_sum);
	}

	for(int i = 0; i < 4; i++){
		sub.Myq.col(i) = sub.body[i].Ki*sub.body[i].Bi;
	}
}

void Simulation::base_mass_force_analysis()
{
	base.Ai_Cii = base.Ai*base.Cii;
	base.Jic = base.Ai_Cii*base.Jip*base.Ai_Cii.transpose();

	base.rict = skew(base.ric);
	base.drict = skew(base.dric);

	base.fic = Vector3d(0, 0, base.mi*g);
	base.tic = Vector3d(0, 0, 0);

	base.Mih_11 = base.mi*Matrix3d::Identity();
	base.Mih_12 = -base.mi*base.rict;
	base.Mih_22 = base.Jic - base.mi*base.rict*base.rict;
	base.Mih.block<3,3>(0,0) = base.Mih_11;
	base.Mih.block<3,3>(0,3) = base.Mih_12;
	base.Mih.block<3,3>(3,0) = -base.Mih_12;
	base.Mih.block<3,3>(3,3) = base.Mih_22;

	base.Qih << base.fic + base.mi*base.drict*base.wi,
			base.tic + base.rict*base.fic + base.mi*base.drict*base.wi - base.wit*base.Jic*base.wi;

	// K0 = M0h + FL.K1 + ML.K1 + RL.K1 + FR.K1 + MR.K1 + RR.K1;
	// L0 = Q0h + FL.L1 + ML.L1 + RL.L1 + FR.L1 + MR.L1 + RR.L1
	// 		- (FL.K1*FL.D1 + ML.K1*ML.D1 + RL.K1*RL.D1 + FR.K1*FR.D1 + MR.K1*MR.D1 + RR.K1*RR.D1);

	base.Ki = base.Mih + sub[0].body[0].Ki;
	base.Li = base.Qih + sub[0].body[0].Li - sub[0].body[0].Ki*sub[0].body[0].Di;
}

void Simulation::EQM()
{
	M.setZero();
	M.block<6,6>(0,0) = Matrix6d::Identity();
	M.block<4,4>(6,6) = sub[0].M;
	// M.block<4,4>(10,10) = ML.M;
	// M.block<4,4>(14,14) = RL.M;
	// M.block<4,4>(18,18) = FR.M;
	// M.block<4,4>(22,22) = MR.M;
	// M.block<4,4>(26,26) = RR.M;

	Q.setZero();
	Q << Vector6d::Zero(), sub[0].Q;//, ML.Q, RL.Q, FR.Q, MR.Q, RR.Q;

	ddq = M.ldlt().solve(Q);
	// ddq = M.llt().solve(Q);

	base.dYih = ddq.segment<6>(0);
	sub[0].ddq = ddq.segment<4>(6);
	// ML.ddq = ddq.segment<4>(10);
	// RL.ddq = ddq.segment<4>(14);
	// FR.ddq = ddq.segment<4>(18);
	// MR.ddq = ddq.segment<4>(22);
	// RR.ddq = ddq.segment<4>(26);
}

void Simulation::base_acceleration_analysis()
{
	base.dpi = 0.5*base.Ei.transpose()*base.wi;

	base.Ti.block<3,3>(0,0) = Matrix3d::Identity();
	base.Ti.block<3,3>(0,3) = -base.rit;
	base.Ti.block<3,3>(3,0) = Matrix3d::Zero();
	base.Ti.block<3,3>(3,3) = Matrix3d::Identity();

	base.Ri << base.drit*base.wi, Vector3d::Zero();
	base.dYib = base.Ti*base.dYih - base.Ri;

	base.ddri = base.dYib.segment<3>(0);
	base.dwi = base.dYib.segment<3>(3);

	base.dwit = skew(base.dwi);
	base.ddric = base.ddri + base.dwit*base.rhoi + base.wit*base.wit*base.rhoi;
}

void Simulation::sub_acceleration_analysis(Subsystem &sub)
{
	Body *prev = &base;
	int i = 0;
	for(Body &body : sub.body){
		body.dYih = prev->dYih + body.Bi*sub.ddq[i] + body.Di;
		body.Ti.setIdentity();
		body.Ti.block<3, 3>(0, 3) = -body.rit;
		body.dTi.setZero();
		body.dTi.block<3, 3>(0, 3) = -body.drit;
		body.Ri << body.drit*body.wi, Vector3d::Zero();
		body.dYib = body.dTi*body.Yih + body.Ti*body.dYih;
		body.ddri = body.dYib.segment<3>(0);
		body.dwi = body.dYib.segment<3>(3);
		body.ddric = body.ddri + body.dwit*body.rhoi + body.wit*body.wit*body.rhoi;
		i++;
		prev = &body;
	}
}
