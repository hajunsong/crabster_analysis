#include "simulation.h"

Simulation::Simulation() : 
            FL(FL_s01p, FL_C01), ML(ML_s01p, ML_C01), RL(RL_s01p, RL_C01),
            FR(FR_s01p, FR_C01), MR(MR_s01p, MR_C01), RR(RR_s01p, RR_C01)
{
	Y = VectorXd::Zero(61);
	Yp = VectorXd::Zero(61);
}

Simulation::~Simulation(){
}

void Simulation::define_Y_vector(){
    Y << r0, p0, dr0, w0,
        FL.q_init, FL.dq, ML.q_init, ML.dq, RL.q_init, RL.dq,
        FR.q_init, FR.dq, MR.q_init, MR.dq, RR.q_init, RR.dq;
}

void Simulation::Y2qdq(Eigen::Vector<double, 61> Y)
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

Eigen::Vector<double, 61> Simulation::dqddq2Yp()
{
    Yp << dr0, dp0, ddr0, dw0,
        FL.dq, FL.ddq, ML.dq, ML.ddq, RL.dq, RL.ddq,
        FR.dq, FR.ddq, MR.dq, MR.ddq, RR.dq, RR.ddq;

	return Yp;
}

void Simulation::run(){
    t_c = 0;
    t_e = 2;
    dt = 0.001;
	step = 0;

    g = -9.80665;

	Vector4d L_q_init(M_PI_4, 0, 0, -M_PI_4*3);
	Vector4d R_q_init(-M_PI_4, 0, 0,  M_PI_4*3);

    FL.q_init = L_q_init;
    ML.q_init = L_q_init;
    RL.q_init = L_q_init;
    FR.q_init = R_q_init;
    MR.q_init = R_q_init;
    RR.q_init = R_q_init;

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
		Y_next = Y + (dt/6.0)*(k1 + 2*k2 + 3*k3 + k4);
		t_next = t_c + dt;

		std::vector<double> row;
		row.reserve(2 + 6*(6 + 6 + 6 + 6 + 6));

		row.push_back(static_cast<double>(step));
		row.push_back(t_c);

		auto push_leg = [&](const Subsystem& S){
			// q(4)
			for (int i=0;i<4;++i) row.push_back(S.q[i]);
			row.push_back(0); row.push_back(0); // Python의 0,0

			// dq(4)
			for (int i=0;i<4;++i) row.push_back(S.dq[i]);
			row.push_back(0); row.push_back(0);

			// ddq(4)
			for (int i=0;i<4;++i) row.push_back(S.ddq[i]);
			row.push_back(0); row.push_back(0);

			// re*1000 (3)
			row.push_back(S.re.x()*1000.0);
			row.push_back(S.re.y()*1000.0);
			row.push_back(S.re.z()*1000.0);

			// rpy (3)
			row.push_back(S.rpy.x());
			row.push_back(S.rpy.y());
			row.push_back(S.rpy.z());
		};

		push_leg(FL);
		push_leg(ML);
		push_leg(RL);
		push_leg(FR);
		push_leg(MR);
		push_leg(RR);

		log.push_back(std::move(row));

		std::cout << "t_c : " << t_c << std::endl;

		t_c = t_next;
		step++;
		Y = Y_next;
    }

	const std::string out_csv = "sim_data.csv";
	write_csv(out_csv, log);
	std::cout << "[OK] saved: " << out_csv << "  rows=" << log.size() << "\n";
}

Eigen::Vector<double, 61> Simulation::analysis(Eigen::Vector<double, 61> Y)
{
	Y2qdq(Y);

    base_position_analysis();
    base_velocity_analysis();

	sub_position_analysis(FL);
	sub_position_analysis(ML);
	sub_position_analysis(RL);
	sub_position_analysis(FR);
	sub_position_analysis(MR);
	sub_position_analysis(RR);

	sub_velocity_analysis(FL);
	sub_velocity_analysis(ML);
	sub_velocity_analysis(RL);
	sub_velocity_analysis(FR);
	sub_velocity_analysis(MR);
	sub_velocity_analysis(RR);

	sub_mass_force_analysis(FL);
	sub_mass_force_analysis(ML);
	sub_mass_force_analysis(RL);
	sub_mass_force_analysis(FR);
	sub_mass_force_analysis(MR);
	sub_mass_force_analysis(RR);
    
    base_mass_force_analysis();

    EQM();

    base_acceleration_analysis();

	sub_acceleration_analysis(FL);
	sub_acceleration_analysis(ML);
	sub_acceleration_analysis(RL);
	sub_acceleration_analysis(FR);
	sub_acceleration_analysis(MR);
	sub_acceleration_analysis(RR);

	Yp = dqddq2Yp();

	return Yp;
}

void Simulation::base_position_analysis()
{
    double q0 = p0[0];
	Vector3d qv = p0.segment<3>(1);
	Matrix3d S = skew(qv);
	Matrix3d I = Eigen::Matrix3d::Identity();

    // E0 = [-qv, S + q0*I]
    E0.col(0) = -qv;
    E0.block<3,3>(0,1) = S + q0*I;

    // G0 = [-qv, -S + q0*I]
    G0.col(0) = -qv;
    G0.block<3,3>(0,1) = -S + q0*I;

	A0 = E0*G0.transpose();
	rpy0 = mat2rpy(A0);

	rho0 = A0*rho0p;
	r0c = r0 + rho0;
}

void Simulation::base_velocity_analysis()
{
	w0t = skew(w0);
	r0t = skew(r0);
	dr0t = skew(dr0);
	dr0c = dr0 + w0t*rho0;

	Y0h << dr0 + dr0t*w0, w0;
}

void Simulation::sub_position_analysis(Subsystem &sub)
{
	sub.A01pp << cos(sub.q[0]), -sin(sub.q[0]), 0, sin(sub.q[0]), cos(sub.q[0]), 0, 0, 0, 1;
	sub.A12pp << cos(sub.q[1]), -sin(sub.q[1]), 0, sin(sub.q[1]), cos(sub.q[1]), 0, 0, 0, 1;
	sub.A23pp << cos(sub.q[2]), -sin(sub.q[2]), 0, sin(sub.q[2]), cos(sub.q[2]), 0, 0, 0, 1;
	sub.A34pp << cos(sub.q[3]), -sin(sub.q[3]), 0, sin(sub.q[3]), cos(sub.q[3]), 0, 0, 0, 1;

	sub.A1 = A0*sub.C01*sub.A01pp;
	sub.A2 = sub.A1*sub.C12*sub.A12pp;
	sub.A3 = sub.A2*sub.C23*sub.A23pp;
	sub.A4 = sub.A3*sub.C34*sub.A34pp;

	sub.s01 = A0*sub.s01p;
	sub.s12 = sub.A1*sub.s12p;
	sub.s23 = sub.A2*sub.s23p;
	sub.s34 = sub.A3*sub.s34p;

	sub.r1 = r0 + sub.s01;
	sub.r2 = sub.r1 + sub.s12;
	sub.r3 = sub.r2 + sub.s23;
	sub.r4 = sub.r3 + sub.s34;

	sub.rho1 = sub.A1*sub.rho1p;
	sub.rho2 = sub.A2*sub.rho2p;
	sub.rho3 = sub.A3*sub.rho3p;
	sub.rho4 = sub.A4*sub.rho4p;

	sub.r1c = sub.r1 + sub.rho1;
	sub.r2c = sub.r2 + sub.rho2;
	sub.r3c = sub.r3 + sub.rho3;
	sub.r4c = sub.r4 + sub.rho4;

	sub.s4e = sub.A4*sub.s4ep;
	sub.re = sub.r4 + sub.s4e;
	sub.Ae = sub.A4*sub.C4e;
	sub.rpy = mat2rpy(sub.Ae);
}

void Simulation::sub_velocity_analysis(Subsystem &sub)
{
	sub.H1 = A0*sub.C01*sub.u_vec1;
	sub.H2 = sub.A1*sub.C12*sub.u_vec2;
	sub.H3 = sub.A2*sub.C23*sub.u_vec3;
	sub.H4 = sub.A3*sub.C34*sub.u_vec4;

	sub.w1 = w0 + sub.H1*sub.dq[0];
	sub.w2 = sub.w1 + sub.H2*sub.dq[1];
	sub.w3 = sub.w2 + sub.H3*sub.dq[2];
	sub.w4 = sub.w3 + sub.H4*sub.dq[3];

	sub.w1t = skew(sub.w1);
	sub.w2t = skew(sub.w2);
	sub.w3t = skew(sub.w3);
	sub.w4t = skew(sub.w4);

	sub.dr1 = dr0 + w0t*sub.s01;
	sub.dr2 = sub.dr1 + sub.w1t*sub.s12;
	sub.dr3 = sub.dr2 + sub.w2t*sub.s23;
	sub.dr4 = sub.dr3 + sub.w3t*sub.s34;

	sub.r1t = skew(sub.r1);
	sub.r2t = skew(sub.r2);
	sub.r3t = skew(sub.r3);
	sub.r4t = skew(sub.r4);

	sub.dre = sub.dr4 + sub.w4t*sub.r4;

	sub.B1 << sub.r1t*sub.H1, sub.H1;
	sub.B2 << sub.r2t*sub.H2, sub.H2;
	sub.B3 << sub.r3t*sub.H3, sub.H3;
	sub.B4 << sub.r4t*sub.H4, sub.H4;

	sub.dr1t = skew(sub.dr1);
	sub.dr2t = skew(sub.dr2);
	sub.dr3t = skew(sub.dr3);
	sub.dr4t = skew(sub.dr4);

	sub.dr1c = sub.dr1 + sub.w1t*sub.rho1;
	sub.dr2c = sub.dr2 + sub.w2t*sub.rho2;
	sub.dr3c = sub.dr3 + sub.w3t*sub.rho3;
	sub.dr4c = sub.dr4 + sub.w4t*sub.rho4;

	sub.dH1 = w0t*sub.H1;
	sub.dH2 = sub.w1t*sub.H2;
	sub.dH3 = sub.w2t*sub.H3;
	sub.dH4 = sub.w3t*sub.H4;

	sub.D1 << sub.dr1t*sub.H1 + sub.r1t*sub.dH1, sub.dH1; sub.D1 *= sub.dq[0];
	sub.D2 << sub.dr2t*sub.H2 + sub.r2t*sub.dH2, sub.dH2; sub.D2 *= sub.dq[1];
	sub.D3 << sub.dr3t*sub.H3 + sub.r3t*sub.dH3, sub.dH3; sub.D3 *= sub.dq[2];
	sub.D4 << sub.dr4t*sub.H4 + sub.r4t*sub.dH4, sub.dH4; sub.D4 *= sub.dq[3];

	sub.Y1h = Y0h + sub.B1*sub.dq[0];
	sub.Y2h = sub.Y1h + sub.B2*sub.dq[1];
	sub.Y3h = sub.Y2h + sub.B3*sub.dq[2];
	sub.Y4h = sub.Y3h + sub.B4*sub.dq[3];
}

void Simulation::sub_mass_force_analysis(Subsystem &sub)
{
	sub.A1_C11 = sub.A1*sub.C11;
	sub.A2_C22 = sub.A2*sub.C22;
	sub.A3_C33 = sub.A3*sub.C33;
	sub.A4_C44 = sub.A4*sub.C44;

	sub.J1c = sub.A1_C11*sub.J1p*sub.A1_C11.transpose();
	sub.J2c = sub.A2_C22*sub.J2p*sub.A2_C22.transpose();
	sub.J3c = sub.A3_C33*sub.J3p*sub.A3_C33.transpose();
	sub.J4c = sub.A4_C44*sub.J4p*sub.A4_C44.transpose();

	sub.r1ct = skew(sub.r1c);
	sub.r2ct = skew(sub.r2c);
	sub.r3ct = skew(sub.r3c);
	sub.r4ct = skew(sub.r4c);

	sub.dr1ct = skew(sub.dr1c);
	sub.dr2ct = skew(sub.dr2c);
	sub.dr3ct = skew(sub.dr3c);
	sub.dr4ct = skew(sub.dr4c);

	sub.f1c = Vector3d(0, 0, sub.m1*g);
	sub.f2c = Vector3d(0, 0, sub.m2*g);
	sub.f3c = Vector3d(0, 0, sub.m3*g);
	sub.f4c = Vector3d(0, 0, sub.m4*g);

	sub.t1c = Vector3d(0, 0, 0);
	sub.t2c = Vector3d(0, 0, 0);
	sub.t3c = Vector3d(0, 0, 0);
	sub.t4c = Vector3d(0, 0, 0);

	sub.M1h_11 = sub.m1*Matrix3d::Identity();
	sub.M1h_12 = -sub.m1*sub.r1ct;
	sub.M1h_22 = sub.J1c - sub.m1*sub.r1ct*sub.r1ct;

	sub.M1h.block<3,3>(0, 0) = sub.M1h_11;
	sub.M1h.block<3,3>(0, 3) = sub.M1h_12;
	sub.M1h.block<3,3>(3, 0) = -sub.M1h_12;
	sub.M1h.block<3,3>(3, 3) = sub.M1h_22;

	sub.M2h_11 = sub.m2*Matrix3d::Identity();
	sub.M2h_12 = -sub.m2*sub.r2ct;
	sub.M2h_22 = sub.J2c - sub.m2*sub.r2ct*sub.r2ct;

	sub.M2h.block<3,3>(0, 0) = sub.M2h_11;
	sub.M2h.block<3,3>(0, 3) = sub.M2h_12;
	sub.M2h.block<3,3>(3, 0) = -sub.M2h_12;
	sub.M2h.block<3,3>(3, 3) = sub.M2h_22;

	sub.M3h_11 = sub.m3*Matrix3d::Identity();
	sub.M3h_12 = -sub.m3*sub.r3ct;
	sub.M3h_22 = sub.J3c - sub.m3*sub.r3ct*sub.r3ct;

	sub.M3h.block<3,3>(0, 0) = sub.M3h_11;
	sub.M3h.block<3,3>(0, 3) = sub.M3h_12;
	sub.M3h.block<3,3>(3, 0) = -sub.M3h_12;
	sub.M3h.block<3,3>(3, 3) = sub.M3h_22;

	sub.M4h_11 = sub.m4*Matrix3d::Identity();
	sub.M4h_12 = -sub.m4*sub.r4ct;
	sub.M4h_22 = sub.J4c - sub.m4*sub.r4ct*sub.r4ct;

	sub.M4h.block<3,3>(0, 0) = sub.M4h_11;
	sub.M4h.block<3,3>(0, 3) = sub.M4h_12;
	sub.M4h.block<3,3>(3, 0) = -sub.M4h_12;
	sub.M4h.block<3,3>(3, 3) = sub.M4h_22;

	sub.Q1h << sub.f1c + sub.m1*sub.dr1ct*sub.w1,
			sub.t1c + sub.r1ct*sub.f1c + sub.m1*sub.r1ct*sub.dr1ct*sub.w1 - sub.w1t*sub.J1c*sub.w1;
	sub.Q2h << sub.f2c + sub.m2*sub.dr2ct*sub.w2,
			sub.t2c + sub.r2ct*sub.f2c + sub.m2*sub.r2ct*sub.dr2ct*sub.w2 - sub.w2t*sub.J2c*sub.w2;
	sub.Q3h << sub.f3c + sub.m3*sub.dr3ct*sub.w3,
			sub.t3c + sub.r3ct*sub.f3c + sub.m3*sub.r3ct*sub.dr3ct*sub.w3 - sub.w3t*sub.J3c*sub.w3;
	sub.Q4h << sub.f4c + sub.m4*sub.dr4ct*sub.w4,
			sub.t4c + sub.r4ct*sub.f4c + sub.m4*sub.r4ct*sub.dr4ct*sub.w4 - sub.w4t*sub.J4c*sub.w4;

	sub.K4 = sub.M4h;
	sub.K3 = sub.M3h + sub.K4;
	sub.K2 = sub.M2h + sub.K3;
	sub.K1 = sub.M1h + sub.K2;

	sub.L4 = sub.Q4h;
	sub.L3 = sub.Q3h + sub.L4 - sub.K4*sub.D4;
	sub.L2 = sub.Q2h + sub.L3 - sub.K3*sub.D3;
	sub.L1 = sub.Q1h + sub.L2 - sub.K2*sub.D2;

	sub.M(0,0) = sub.B1.transpose()*sub.K1*sub.B1;
	sub.M(0,1) = sub.B1.transpose()*sub.K2*sub.B2;
	sub.M(0,2) = sub.B1.transpose()*sub.K3*sub.B3;
	sub.M(0,3) = sub.B1.transpose()*sub.K4*sub.B4;

	sub.M(1,0) = sub.B2.transpose()*sub.K2*sub.B1;
	sub.M(1,1) = sub.B2.transpose()*sub.K2*sub.B2;
	sub.M(1,2) = sub.B2.transpose()*sub.K3*sub.B3;
	sub.M(1,3) = sub.B2.transpose()*sub.K4*sub.B4;

	sub.M(2,0) = sub.B3.transpose()*sub.K3*sub.B1;
	sub.M(2,1) = sub.B3.transpose()*sub.K3*sub.B2;
	sub.M(2,2) = sub.B3.transpose()*sub.K3*sub.B3;
	sub.M(2,3) = sub.B3.transpose()*sub.K4*sub.B4;

	sub.M(3,0) = sub.B4.transpose()*sub.K4*sub.B1;
	sub.M(3,1) = sub.B4.transpose()*sub.K4*sub.B2;
	sub.M(3,2) = sub.B4.transpose()*sub.K4*sub.B3;
	sub.M(3,3) = sub.B4.transpose()*sub.K4*sub.B4;

	sub.Q(0) = sub.B1.transpose()*(sub.L1 - sub.K1*(sub.D1));
	sub.Q(1) = sub.B2.transpose()*(sub.L2 - sub.K2*(sub.D1 + sub.D2));
	sub.Q(2) = sub.B3.transpose()*(sub.L3 - sub.K3*(sub.D1 + sub.D2 + sub.D3));
	sub.Q(3) = sub.B4.transpose()*(sub.L4 - sub.K4*(sub.D1 + sub.D2 + sub.D3 + sub.D4));

	sub.Myq.col(0) = sub.K1*sub.B1;
	sub.Myq.col(1) = sub.K2*sub.B2;
	sub.Myq.col(2) = sub.K3*sub.B3;
	sub.Myq.col(3) = sub.K4*sub.B4;
}

void Simulation::base_mass_force_analysis()
{
	A0_C00 = A0*C00;
	J0c = A0_C00*J0p*A0_C00.transpose();

	r0ct = skew(r0c);
	dr0ct = skew(dr0c);

	f0c = Vector3d(0, 0, m0*g);
	t0c = Vector3d(0, 0, 0);

	M0h_11 = m0*Matrix3d::Identity();
	M0h_12 = -m0*r0ct;
	M0h_22 = J0c - m0*r0ct*r0ct;
	M0h.block<3,3>(0,0) = M0h_11;
	M0h.block<3,3>(0,3) = M0h_12;
	M0h.block<3,3>(3,0) = -M0h_11;
	M0h.block<3,3>(3,3) = M0h_11;

	Q0h << f0c + m0*dr0ct*w0,
			t0c + r0ct*f0c + m0*dr0ct*w0 - w0t*J0c*w0;

	K0 = M0h + FL.K1 + ML.K1 + RL.K1 + FR.K1 + MR.K1 + RR.K1;
	L0 = Q0h + FL.L1 + ML.L1 + RL.L1 + FR.L1 + MR.L1 + RR.L1
			- (FL.K1*FL.D1 + ML.K1*ML.D1 + RL.K1*RL.D1 + FR.K1*FR.D1 + MR.K1*MR.D1 + RR.K1*RR.D1);
}

void Simulation::EQM()
{
	M.setZero();
	M.block<6,6>(0,0) = Matrix6d::Identity();
	M.block<4,4>(6,6) = FL.M;
	M.block<4,4>(10,10) = ML.M;
	M.block<4,4>(14,14) = RL.M;
	M.block<4,4>(18,18) = FR.M;
	M.block<4,4>(22,22) = MR.M;
	M.block<4,4>(26,26) = RR.M;

	Q.setZero();
	Q << Vector6d::Zero(), FL.Q, ML.Q, RL.Q, FR.Q, MR.Q, RR.Q;
//	Q.segment<4>(6) = FL.Q;
//	Q.segment<4>(10) = ML.Q;
//	Q.segment<4>(14) = RL.Q;
//	Q.segment<4>(18) = FR.Q;
//	Q.segment<4>(22) = MR.Q;
//	Q.segment<4>(26) = RR.Q;

	ddq = M.ldlt().solve(Q);
//	ddq = M.llt().solve(Q);
}

void Simulation::base_acceleration_analysis()
{
	dY0h = Y.segment<6>(0);
	FL.ddq = Y.segment<4>(6);
	ML.ddq = Y.segment<4>(10);
	RL.ddq = Y.segment<4>(14);
	FR.ddq = Y.segment<4>(18);
	MR.ddq = Y.segment<4>(22);
	RR.ddq = Y.segment<4>(26);

	dp0 = 0.5*E0.transpose()*w0;

	T0.block<3,3>(0,0) = Matrix3d::Identity();
	T0.block<3,3>(0,3) = -r0t;
	T0.block<3,3>(3,0) = Matrix3d::Zero();
	T0.block<3,3>(3,3) = Matrix3d::Identity();

	R0 << dr0t*w0, Vector3d::Zero();
	dY0b = T0*dY0h - R0;

	ddr0 = dY0b.segment<3>(0);
	dw0 = dY0b.segment<3>(3);

	dw0t = skew(dw0);
	ddr0c = ddr0 + dw0t*rho0 + w0t*w0t*rho0;
}

void Simulation::sub_acceleration_analysis(Subsystem &sub)
{
	sub.dY1h = dY0h + sub.B1*sub.ddq[0] + sub.D1;
	sub.dY2h = sub.dY1h + sub.B2*sub.ddq[1] + sub.D2;
	sub.dY3h = sub.dY2h + sub.B3*sub.ddq[2] + sub.D3;
	sub.dY4h = sub.dY3h + sub.B4*sub.ddq[3] + sub.D4;

	sub.T1.setIdentity();	sub.T1.block<3,3>(0,3) = -sub.r1t;
	sub.T2.setIdentity();	sub.T2.block<3,3>(0,3) = -sub.r2t;
	sub.T3.setIdentity();	sub.T3.block<3,3>(0,3) = -sub.r3t;
	sub.T4.setIdentity();	sub.T4.block<3,3>(0,3) = -sub.r4t;

	sub.dT1.setZero();	sub.dT1.block<3,3>(0,3) = -sub.dr1t;
	sub.dT2.setZero();	sub.dT2.block<3,3>(0,3) = -sub.dr2t;
	sub.dT3.setZero();	sub.dT3.block<3,3>(0,3) = -sub.dr3t;
	sub.dT4.setZero();	sub.dT4.block<3,3>(0,3) = -sub.dr4t;

	sub.R1 << sub.dr1t*sub.w1, Vector3d::Zero();
	sub.R2 << sub.dr2t*sub.w2, Vector3d::Zero();
	sub.R3 << sub.dr3t*sub.w3, Vector3d::Zero();
	sub.R4 << sub.dr4t*sub.w4, Vector3d::Zero();

	sub.dY1b = sub.dT1*sub.Y1h + sub.T1*sub.dY1h;
	sub.dY2b = sub.dT2*sub.Y2h + sub.T2*sub.dY2h;
	sub.dY3b = sub.dT3*sub.Y3h + sub.T3*sub.dY3h;
	sub.dY4b = sub.dT4*sub.Y4h + sub.T4*sub.dY4h;

	sub.ddr1 = sub.dY1b.segment<3>(0); sub.dw1 = sub.dY1b.segment<3>(3);
	sub.ddr2 = sub.dY2b.segment<3>(0); sub.dw2 = sub.dY2b.segment<3>(3);
	sub.ddr3 = sub.dY3b.segment<3>(0); sub.dw3 = sub.dY3b.segment<3>(3);
	sub.ddr4 = sub.dY4b.segment<3>(0); sub.dw4 = sub.dY4b.segment<3>(3);

	sub.ddr1c = sub.ddr1 + sub.dw1t*sub.rho1 + sub.w1t*sub.w1t*sub.rho1;
	sub.ddr2c = sub.ddr2 + sub.dw2t*sub.rho2 + sub.w2t*sub.w2t*sub.rho2;
	sub.ddr3c = sub.ddr3 + sub.dw3t*sub.rho3 + sub.w3t*sub.w3t*sub.rho3;
	sub.ddr4c = sub.ddr4 + sub.dw4t*sub.rho4 + sub.w4t*sub.w4t*sub.rho4;
}
