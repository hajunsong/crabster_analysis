function body = read_R_body1(sijp, Cij)

    body.qi = 0;
    body.dqi = 0;
    body.ddqi = 0;

    body.sijp = sijp;
    body.Cij = Cij;
    
    body.sep = [];
    body.Ce = [];
    
    body.mi = 3.6;
    body.Ixx = 24217.363;
    body.Ixy = 1.142;
    body.Iyy = 22602.121;
    body.Iyz = -3.656;
    body.Izz = 24383.284;
    body.Izx = 4.718;
    body.Jip = [body.Ixx, body.Ixy, body.Izx;
                body.Ixy, body.Iyy, body.Iyz;
                body.Izx, body.Iyz, body.Izz]*1e-6;
             
    body.rhoip = [-19.41; 0; 0]*0.001;
    body.Cii = ang2mat(pi, pi/2, pi/2);
    
    body.u_vec = [0;0;1];

end