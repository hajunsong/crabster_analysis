function body = read_R_body3()

    body.qi = 0;
    body.dqi = 0;
    body.ddqi = 0;

    body.sijp = [0; 0; 121]*0.001;
    body.Cij = ang2mat(pi, pi/2, pi);
    
    body.sep = [];
    body.Ce = [];
    
    body.mi = 11.1;
    body.Ixx = 172022.706;
    body.Ixy = 939.804;
    body.Iyy = 67557.291;
    body.Iyz = -151.395;
    body.Izz = 155965.608;
    body.Izx = -39.97;
    body.Jip = [body.Ixx, body.Ixy, body.Izx;
                body.Ixy, body.Iyy, body.Iyz;
                body.Izx, body.Iyz, body.Izz]*1e-6;
             
    body.rhoip = [0; -238.39; -1.08]*0.001;
    body.Cii = [1 0 0; 0 1 0; 0 0 1];
    
    body.u_vec = [0;0;1];

end