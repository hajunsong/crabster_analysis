function body = read_L_body2()

    body.qi = 0;
    body.dqi = 0;
    body.ddqi = 0;

    body.sijp = [120; 0; 0]*0.001;
    body.Cij = ang2mat(-pi/2, pi/2, pi/2);
    
    body.sep = [];
    body.Ce = [];
    
    body.mi = 12.9000000000000;
    body.Ixx = 101693.397000000;
    body.Ixy = -54.6390000000000;
    body.Iyy = 43784.8820000000;
    body.Iyz = 3156.79600000000;
    body.Izz = 101586.518000000;
    body.Izx = -3.73400000000000;
    body.Jip = [body.Ixx, body.Ixy, body.Izx;
                body.Ixy, body.Iyy, body.Iyz;
                body.Izx, body.Iyz, body.Izz]*1e-6;
             
    body.rhoip = [0; 0; -101.13]*0.001;
    body.Cii = [1 0 0; 0 0 1; 0 -1 0];
    
    body.u_vec = [0;0;1];

end