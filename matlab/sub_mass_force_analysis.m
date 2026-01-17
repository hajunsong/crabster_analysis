function sub = sub_mass_force_analysis(sub)

    global g motion_flag

    K = [15000000.; 7000000.; 7000000.; 7000000.]*0.001;
    C = [1500000.; 300000.; 300000.; 700000.]*0.001;
    
    road_h = -0.3;
    contact_K = 55000;
    contact_C = 5500;
    
    for i = 1 : 4
        sub.body(i).Ai_Cii = sub.body(i).Ai*sub.body(i).Cii;
        sub.body(i).Jic = sub.body(i).Ai_Cii*sub.body(i).Jip*sub.body(i).Ai_Cii';
        sub.body(i).rict = tilde(sub.body(i).ric);
        sub.body(i).drict = tilde(sub.body(i).dric);

        sub.body(i).fic = [0;0;sub.body(i).mi*g];
        sub.body(i).tic = [0;0;0];

        % if i == 4
        %     pen_z = road_h - sub.body(i).re(3,1);
        %     pen_dz = -sub.body(i).dre(3,1);
        %     if pen_z > 0
        %         sub.body(i).f_cont = [0;0;pen_z*contact_K + pen_dz*contact_C];
        %     else
        %         sub.body(i).f_cont = zeros(3,1);
        %     end
        %     r4cp = sub.body(i).re - sub.body(i).ric;
        %     r4cpt = tilde(r4cp);
        %     sub.body(i).fic = [0;0;sub.body(i).mi*g] + sub.body(i).f_cont;
        %     sub.body(i).tic = [0;0;0] + r4cpt*sub.body(i).f_cont;
        % end
        
        sub.body(i).Mih = [sub.body(i).mi*eye(3), -sub.body(i).mi*sub.body(i).rict; 
                            sub.body(i).mi*sub.body(i).rict, sub.body(i).Jic - sub.body(i).mi*sub.body(i).rict*sub.body(i).rict];
        sub.body(i).Qih = [sub.body(i).fic + sub.body(i).mi*sub.body(i).drict*sub.body(i).wi;
                            sub.body(i).tic + sub.body(i).rict*sub.body(i).fic + sub.body(i).mi*sub.body(i).rict*sub.body(i).drict*sub.body(i).wi - sub.body(i).wit*sub.body(i).Jic*sub.body(i).wi];
        
        if motion_flag == 1
            sub.body(i).Ti_RSDA = 0;
            sub.body(i).Qih_RSDA = zeros(6,1);
            sub.body(i).Qjh_RSDA = zeros(6,1);
        else
            sub.body(i).Ti_RSDA = (sub.body(i).qi_init-sub.body(i).qi)*K(i,1) - sub.body(i).dqi*C(i,1);
            sub.body(i).Qih_RSDA = [zeros(3,1);sub.body(i).Ti_RSDA*sub.body(i).Hi];
            sub.body(i).Qih = sub.body(i).Qih + sub.body(i).Qih_RSDA;
            sub.body(i).Qjh_RSDA = -sub.body(i).Qih_RSDA;
        end
        sub.body(i).Ti_RSDA = 0;
        sub.body(i).Qih_RSDA = zeros(6,1);
        sub.body(i).Qjh_RSDA = zeros(6,1);
    end


    sub.body(4).Ki = sub.body(4).Mih;
    sub.body(3).Ki = sub.body(4).Ki + sub.body(3).Mih;
    sub.body(2).Ki = sub.body(3).Ki + sub.body(2).Mih;
    sub.body(1).Ki = sub.body(2).Ki + sub.body(1).Mih;
    
    sub.body(4).Li = sub.body(4).Qih;
    sub.body(3).Li = sub.body(3).Qih + sub.body(4).Li - sub.body(4).Ki*sub.body(4).Di + sub.body(4).Qjh_RSDA;
    sub.body(2).Li = sub.body(2).Qih + sub.body(3).Li - sub.body(3).Ki*sub.body(3).Di + sub.body(3).Qjh_RSDA;
    sub.body(1).Li = sub.body(1).Qih + sub.body(2).Li - sub.body(2).Ki*sub.body(2).Di + sub.body(2).Qjh_RSDA;
    
    sub.M(1,1) = sub.body(1).Bi'*sub.body(1).Ki*sub.body(1).Bi;
    sub.M(1,2) = sub.body(1).Bi'*sub.body(2).Ki*sub.body(2).Bi;
    sub.M(1,3) = sub.body(1).Bi'*sub.body(3).Ki*sub.body(3).Bi;
    sub.M(1,4) = sub.body(1).Bi'*sub.body(4).Ki*sub.body(4).Bi;
    
    sub.M(2,1) = sub.body(2).Bi'*sub.body(2).Ki*sub.body(1).Bi;
    sub.M(2,2) = sub.body(2).Bi'*sub.body(2).Ki*sub.body(2).Bi;
    sub.M(2,3) = sub.body(2).Bi'*sub.body(3).Ki*sub.body(3).Bi;
    sub.M(2,4) = sub.body(2).Bi'*sub.body(4).Ki*sub.body(4).Bi;
    
    sub.M(3,1) = sub.body(3).Bi'*sub.body(3).Ki*sub.body(1).Bi;
    sub.M(3,2) = sub.body(3).Bi'*sub.body(3).Ki*sub.body(2).Bi;
    sub.M(3,3) = sub.body(3).Bi'*sub.body(3).Ki*sub.body(3).Bi;
    sub.M(3,4) = sub.body(3).Bi'*sub.body(4).Ki*sub.body(4).Bi;
    
    sub.M(4,1) = sub.body(4).Bi'*sub.body(4).Ki*sub.body(1).Bi;
    sub.M(4,2) = sub.body(4).Bi'*sub.body(4).Ki*sub.body(2).Bi;
    sub.M(4,3) = sub.body(4).Bi'*sub.body(4).Ki*sub.body(3).Bi;
    sub.M(4,4) = sub.body(4).Bi'*sub.body(4).Ki*sub.body(4).Bi;
    
    sub.Myq(:,1) = sub.body(1).Ki*sub.body(1).Bi;
    sub.Myq(:,2) = sub.body(2).Ki*sub.body(2).Bi;
    sub.Myq(:,3) = sub.body(3).Ki*sub.body(3).Bi;
    sub.Myq(:,4) = sub.body(4).Ki*sub.body(4).Bi;
    
    sub.Q(1,1) = sub.body(1).Bi'*(sub.body(1).Li - sub.body(1).Ki*(sub.body(1).Di));
    sub.Q(2,1) = sub.body(2).Bi'*(sub.body(2).Li - sub.body(2).Ki*(sub.body(1).Di + sub.body(2).Di));
    sub.Q(3,1) = sub.body(3).Bi'*(sub.body(3).Li - sub.body(3).Ki*(sub.body(1).Di + sub.body(2).Di + sub.body(3).Di));
    sub.Q(4,1) = sub.body(4).Bi'*(sub.body(4).Li - sub.body(4).Ki*(sub.body(1).Di + sub.body(2).Di + sub.body(3).Di + sub.body(4).Di));

    % for i = 1 : 4
    %     sub.Q(i,1) = sub.Q(i,1) + sub.body(i).Ti_RSDA;
    % end

    sub.ddq(1,1) = sub.body(1).ddqi;
    sub.ddq(2,1) = sub.body(2).ddqi;
    sub.ddq(3,1) = sub.body(3).ddqi;
    sub.ddq(4,1) = sub.body(4).ddqi;

end