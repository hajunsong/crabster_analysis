function body = read_L_body4()

    body.qi = 0;
    body.dqi = 0;
    body.ddqi = 0;

    body.sijp = [0; 509; 0]*0.001;
    body.Cij = ang2mat(pi/2, pi/2, 0);
    
    body.sep = [823.56;0;0]*0.001;
    body.Ce = ang2mat(pi, pi/2, pi/2);
    
    body.mi = 11.500000000000000;
    body.Ixx = 686629.019000000;
    body.Ixy = 10499.9540000000;
    body.Iyy = 44753.2490000000;
    body.Iyz = -23952.1570000000;
    body.Izz = 705784.865000000;
    body.Izx = 1652.69100000000;
    body.Jip = [body.Ixx, body.Ixy, body.Izx;
                body.Ixy, body.Iyy, body.Iyz;
                body.Izx, body.Iyz, body.Izz]*1e-6;
             
    body.rhoip = [322.25; 51.84; 0]*0.001;
    body.Cii = ang2mat(pi, pi/2, pi/2);
    
    body.u_vec = [0;0;1];

end