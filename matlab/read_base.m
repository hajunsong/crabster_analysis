function base = read_base()

    base.ri = [0;0;0];
    base.Ai = eye(3);
    base.pi = [1;0;0;0];
    
    base.dri = [0;0;0];
    base.wi = [0;0;0];
    
    base.mi = 582.59;
    base.Ixx = 156890393.0;    base.Ixy = 0;
    base.Iyy = 150169673.0;    base.Iyz = 0;
    base.Izz = 249303699.0;    base.Izx = 0;
    base.Jip = [base.Ixx, base.Ixy, base.Izx;
                base.Ixy, base.Iyy, base.Iyz;
                base.Izx, base.Iyz, base.Izz]*1e-6;
             
    base.rhoip = [0;0;0];
    base.Cii = ang2mat(0, 0, 0);

    base.sijp_FL = [520; 758; 0]*0.001;
    base.Cij_FL = ang2mat(pi/2, pi/2, 0);

    base.sijp_ML = [0; 858; 0]*0.001;
    base.Cij_ML = ang2mat(pi/2, pi/2, 0);

    base.sijp_RL = [-520; 758; 0]*0.001;
    base.Cij_RL = ang2mat(pi/2, pi/2, 0);

    base.sijp_FR = [520; -758; 0]*0.001;
    base.Cij_FR = ang2mat(pi/2, pi/2, 0);

    base.sijp_MR = [0; -858; 0]*0.001;
    base.Cij_MR = ang2mat(pi/2, pi/2, 0);

    base.sijp_RR = [-520; -758; 0]*0.001;
    base.Cij_RR = ang2mat(pi/2, pi/2, 0);

end