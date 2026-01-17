clc; clear all; close all;

global g motion_flag torque_flag subsystem_flag

format long g

[base, FL, ML, RL, FR, MR, RR] = read_data();

t_c = 0;
dt = 0.001;
t_e = 2;
g = -9.80665;
step = 0;
intcount = 1;

motion_flag = 0;
torque_flag = 0;
subsystem_flag = 0;

L_q_init = [pi/4, 0, 0, -pi*3/4];
R_q_init = [-pi/4, 0, 0, pi*3/4];
% L_q_init = zeros(4,1);
% R_q_init = zeros(4,1);
for i = 1 : 4
    FL.body(i).qi_init = L_q_init(i);
    RL.body(i).qi_init = L_q_init(i);
    ML.body(i).qi_init = L_q_init(i);
    FR.body(i).qi_init = R_q_init(i);
    MR.body(i).qi_init = R_q_init(i);
    RR.body(i).qi_init = R_q_init(i);
end

sub = [FL, ML, RL, FR, MR, RR];

Y = define_Y_vector(base, sub);

fp = fopen('mat_data.csv', 'w+');

while t_c <= t_e
    
    [Yp, base, sub] = analysis(Y, t_c, base, sub);
    
    % [Y_next, t_next, intcount] = absh3(t_c, Y, Yp, dt, intcount);
    
    % k1
    k1 = Yp;

    % k2
    y2 = Y + (dt/2) * k1;
    [k2, base, sub] = analysis(y2, t_c + dt/2, base, sub);

    % k3
    y3 = Y + (dt/2) * k2;
    [k3, base, sub] = analysis(y3, t_c + dt/2, base, sub);

    % k4
    y4 = Y + dt * k3;
    [k4, base, sub] = analysis(y4, t_c + dt, base, sub);

    % RK4 update
    Y_next = Y + (dt/6) * (k1 + 2*k2 + 2*k3 + k4);
    t_next = t_c + dt;

    fprintf("%3.5f %3.7f\t %3.7f\t %3.7f\n", t_c, base.ddri');

    data_save(fp, sub, base, step, t_c);
    
    Y = Y_next;
    t_c = t_next;
    step = step + 1;
    
end

fclose('all');

plotting;