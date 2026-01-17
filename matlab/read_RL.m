function sub = read_RL(sijp, Cij)

    sub.body(1) = read_L_body1(sijp, Cij);
    sub.body(2) = read_L_body2();
    sub.body(3) = read_L_body3();
    sub.body(4) = read_L_body4();

    sub.M = zeros(4,4);
    sub.Q = zeros(4,1);
    sub.Myq = zeros(6,4);
    sub.ddq = zeros(4,1);

end