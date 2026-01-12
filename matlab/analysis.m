function [Yp, base, sub] = analysis(Y, t_c, base, sub)

    global g motion_flag

    [base, sub] = Y2qdq(Y, base, sub);

    if motion_flag == 1
        for i = 1 : 3
            [sub(i).body(1).qi, sub(i).body(1).dqi, sub(i).body(1).ddqi] = joint_motion(t_c, 0, 0, 0.05, pi/4);
            [sub(i).body(2).qi, sub(i).body(2).dqi, sub(i).body(2).ddqi] = joint_motion(t_c, 0, 0, 0.05, 0);
            [sub(i).body(3).qi, sub(i).body(3).dqi, sub(i).body(3).ddqi] = joint_motion(t_c, 0, 0, 0.05, 0);
            [sub(i).body(4).qi, sub(i).body(4).dqi, sub(i).body(4).ddqi] = joint_motion(t_c, 0, 0, 0.05, -pi/4*3);
        end

        for i = 4 : 6
            [sub(i).body(1).qi, sub(i).body(1).dqi, sub(i).body(1).ddqi] = joint_motion(t_c, 0, -pi/4, 0.1, -pi/4);
            [sub(i).body(2).qi, sub(i).body(2).dqi, sub(i).body(2).ddqi] = joint_motion(t_c, 0, 0, 0.1, 0);
            [sub(i).body(3).qi, sub(i).body(3).dqi, sub(i).body(3).ddqi] = joint_motion(t_c, 0, 0, 0.1, 0);
            [sub(i).body(4).qi, sub(i).body(4).dqi, sub(i).body(4).ddqi] = joint_motion(t_c, 0, pi/4*3, 0.1, pi/4*3);
        end
    end
    
    base.Ei = [-base.pi(2:4,1),tilde(base.pi(2:4,1))+base.pi(1)*eye(3)];
    base.Gi = [-base.pi(2:4,1),-tilde(base.pi(2:4,1))+base.pi(1)*eye(3)];
    base.Ai = base.Ei*base.Gi';
    base.rpy = mat2rpy(base.Ai);
    
    base.Jic = base.Ai*base.Cii*base.Jip*(base.Ai*base.Cii)';
    
    base.rhoi = base.Ai*base.rhoip;
    base.ric = base.ri + base.rhoi;
    
    base.wit = tilde(base.wi);
    base.rit = tilde(base.ri);
    
    base.dric = base.dri + base.wit*base.rhoi;
    
    base.drit = tilde(base.dri);
    base.drict = tilde(base.dric);
    base.rict = tilde(base.ric);
    
    base.Yih = [base.dri + base.drit*base.wi;base.wi];
    
    base.fic = [0;0;base.mi*g];
    base.tic = [0;0;0];
    
    base.Mih = [base.mi*eye(3) -base.mi*base.rict; base.mi*base.rict base.Jic - base.mi*base.rict*base.rict];
    base.Qih = [base.fic + base.mi*base.drict*base.wi;base.tic + base.rict*base.fic + base.mi*base.rict*base.drict*base.wi - base.wit*base.Jic*base.wi];

    for sindx = 1 : 6
        sub(sindx).body = sub_position_analysis(sub(sindx).body, base);
        sub(sindx).body = sub_velocity_analysis(sub(sindx).body, base);
    end
    
    for sindx = 1 : 6
        sub(sindx) = sub_mass_force_analysis(sub(sindx));
    end
    
    base.Ki = zeros(6,6);
    base.Li = zeros(6,1);
    for sindx = 1 : 6
        base.Ki = base.Ki + sub(sindx).body(1).Ki;
        base.Li = base.Li + sub(sindx).body(1).Li - sub(sindx).body(1).Ki*sub(sindx).body(1).Di;
        base.Li = base.Li + sub(sindx).body(1).Qjh_RSDA;
    end
    base.Ki = base.Ki + base.Mih;
    base.Li = base.Li + base.Qih;

    if motion_flag == 1
        for sindx = 1 : 6
            base.Li = base.Li - sub(sindx).Myq*sub(sindx).ddq;
        end
        ddq = base.Ki\base.Li;
        base.dYih = ddq(1:6,1);
    else
        base.Ki = eye(6);
        base.Li = zeros(6,1);

        M = [base.Ki    sub(1).Myq  sub(2).Myq  sub(3).Myq  sub(4).Myq  sub(5).Myq  sub(6).Myq;
            sub(1).Myq' sub(1).M    zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4);
            sub(2).Myq' zeros(4,4)  sub(2).M    zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4);
            sub(3).Myq' zeros(4,4)  zeros(4,4)  sub(3).M    zeros(4,4)  zeros(4,4)  zeros(4,4);
            sub(4).Myq' zeros(4,4)  zeros(4,4)  zeros(4,4)  sub(4).M    zeros(4,4)  zeros(4,4);
            sub(5).Myq' zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4)  sub(5).M    zeros(4,4);
            sub(6).Myq' zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4)  sub(6).M];
            
        Q = [base.Li
            sub(1).Q
            sub(2).Q
            sub(3).Q
            sub(4).Q
            sub(5).Q
            sub(6).Q]; 

        M = [eye(6,6)   zeros(6,4)  zeros(6,4)  zeros(6,4)  zeros(6,4)  zeros(6,4)  zeros(6,4);
            zeros(6,4)' sub(1).M    zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4);
            zeros(6,4)' zeros(4,4)  sub(2).M    zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4);
            zeros(6,4)' zeros(4,4)  zeros(4,4)  sub(3).M    zeros(4,4)  zeros(4,4)  zeros(4,4);
            zeros(6,4)' zeros(4,4)  zeros(4,4)  zeros(4,4)  sub(4).M    zeros(4,4)  zeros(4,4);
            zeros(6,4)' zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4)  sub(5).M    zeros(4,4);
            zeros(6,4)' zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4)  zeros(4,4)  sub(6).M];

        Q = [zeros(6,1)
            sub(1).Q
            sub(2).Q
            sub(3).Q
            sub(4).Q
            sub(5).Q
            sub(6).Q]; 
        
        ddq = M\Q;
        base.dYih = ddq(1:6,1);
        
        sub(1).body(1).ddqi = ddq(7,1);
        sub(1).body(2).ddqi = ddq(8,1);
        sub(1).body(3).ddqi = ddq(9,1);
        sub(1).body(4).ddqi = ddq(10,1);
        
        sub(2).body(1).ddqi = ddq(11,1);
        sub(2).body(2).ddqi = ddq(12,1);
        sub(2).body(3).ddqi = ddq(13,1);
        sub(2).body(4).ddqi = ddq(14,1);
        
        sub(3).body(1).ddqi = ddq(15,1);
        sub(3).body(2).ddqi = ddq(16,1);
        sub(3).body(3).ddqi = ddq(17,1);
        sub(3).body(4).ddqi = ddq(18,1);
        
        sub(4).body(1).ddqi = ddq(19,1);
        sub(4).body(2).ddqi = ddq(20,1);
        sub(4).body(3).ddqi = ddq(21,1);
        sub(4).body(4).ddqi = ddq(22,1);
        
        sub(5).body(1).ddqi = ddq(23,1);
        sub(5).body(2).ddqi = ddq(24,1);
        sub(5).body(3).ddqi = ddq(25,1);
        sub(5).body(4).ddqi = ddq(26,1);
        
        sub(6).body(1).ddqi = ddq(27,1);
        sub(6).body(2).ddqi = ddq(28,1);
        sub(6).body(3).ddqi = ddq(29,1);
        sub(6).body(4).ddqi = ddq(30,1);
    end
    
    base.dpi = 0.5*base.Ei'*base.wi;
    
    base.Ti = [eye(3) -base.rit;
                zeros(3) eye(3)];
    base.Ri = [base.drit*base.wi;zeros(3,1)];
    base.dYib = base.Ti*base.dYih - base.Ri;
    
    base.ddri = base.dYib(1:3,1);
    base.dwi = base.dYib(4:6,1);
    
    base.dwit = tilde(base.dwi);
    base.ddric = base.ddri + base.dwit*base.rhoi + base.wit*base.wit*base.rhoi;
    
    for sindx = 1 : 6
        sub(sindx).body = sub_acceleration_analysis(sub(sindx).body, base);
    end
    
    Yp = dqddq2Yp(base, sub);

end