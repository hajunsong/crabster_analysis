function mat = ang2mat(psi, theta, phi)

    mat_psi = [cos(psi), -sin(psi), 0; sin(psi), cos(psi), 0; 0, 0, 1];
    mat_theta = [1, 0, 0; 0, cos(theta), -sin(theta); 0, sin(theta), cos(theta)];
    mat_phi = [cos(phi), -sin(phi), 0; sin(phi), cos(phi), 0; 0, 0, 1];
    
    mat = mat_psi*mat_theta*mat_phi;

end