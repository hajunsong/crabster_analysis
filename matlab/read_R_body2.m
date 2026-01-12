function body = read_R_body2()

    body.qi = 0;
    body.dqi = 0;
    body.ddqi = 0;

    body.sijp = [-120; 0; 0]*0.001;
    body.Cij = ang2mat(-pi/2, pi/2, pi/2);
    
    body.sep = [];
    body.Ce = [];
    
    body.mi = 12.9;
    body.Ixx = 101693.397;
    body.Ixy = 54.639;
    body.Iyy = 43784.882;
    body.Iyz = -3156.796;
    body.Izz = 101586.518;
    body.Izx = 3.734;
    body.Jip = [body.Ixx, body.Ixy, body.Izx;
                body.Ixy, body.Iyy, body.Iyz;
                body.Izx, body.Iyz, body.Izz]*1e-6;
             
    body.rhoip = [0; 0; 101.13]*0.001;
    body.Cii = ang2mat(pi, pi/2, pi);
    
    body.u_vec = [0;0;1];

end