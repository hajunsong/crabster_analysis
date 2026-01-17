function body = read_R_body4()

    body.qi = 0;
    body.dqi = 0;
    body.ddqi = 0;

    body.sijp = [0; -509; 0]*0.001;
    body.Cij = ang2mat(pi/2, pi/2, 0);
    
    body.sep = [-823.56;0;0]*0.001;
    body.Ce = ang2mat(pi, pi/2, pi/2);
    
    body.mi = 11.5;
    body.Ixx = 686629.019;
    body.Ixy = 10499.954;
    body.Iyy = 44753.249;
    body.Iyz = 23952.157;
    body.Izz = 705784.865;
    body.Izx = -1652.691;
    body.Jip = [body.Ixx, body.Ixy, body.Izx;
                body.Ixy, body.Iyy, body.Iyz;
                body.Izx, body.Iyz, body.Izz]*1e-6;
             
    body.rhoip = [-322.25; 51.84; 0]*0.001;
    body.Cii = ang2mat(pi, pi/2, pi/2);
    
    body.u_vec = [0;0;1];

end