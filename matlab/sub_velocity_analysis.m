function body = sub_velocity_analysis(body, base)

    body(1).Hi = base.Ai*body(1).Cij*body(1).u_vec;
    body(2).Hi = body(1).Ai*body(2).Cij*body(2).u_vec;
    body(3).Hi = body(2).Ai*body(3).Cij*body(3).u_vec;
    body(4).Hi = body(3).Ai*body(4).Cij*body(4).u_vec;
    
    body(1).wi = base.wi + body(1).Hi*body(1).dqi;
    body(2).wi = body(1).wi + body(2).Hi*body(2).dqi;
    body(3).wi = body(2).wi + body(3).Hi*body(3).dqi;
    body(4).wi = body(3).wi + body(4).Hi*body(4).dqi;
    
    body(1).wit = tilde(body(1).wi);
    body(2).wit = tilde(body(2).wi);
    body(3).wit = tilde(body(3).wi);
    body(4).wit = tilde(body(4).wi);
    
    body(1).dri = base.dri + base.wit*body(1).sij;
    body(2).dri = body(1).dri + body(1).wit*body(2).sij;
    body(3).dri = body(2).dri + body(2).wit*body(3).sij;
    body(4).dri = body(3).dri + body(3).wit*body(4).sij;
    
    body(4).dre = body(4).dri + body(4).wit*body(4).re;
    
    body(1).rit = tilde(body(1).ri);
    body(2).rit = tilde(body(2).ri);
    body(3).rit = tilde(body(3).ri);
    body(4).rit = tilde(body(4).ri);
    
    body(1).Bi = [body(1).rit*body(1).Hi;body(1).Hi];
    body(2).Bi = [body(2).rit*body(2).Hi;body(2).Hi];
    body(3).Bi = [body(3).rit*body(3).Hi;body(3).Hi];
    body(4).Bi = [body(4).rit*body(4).Hi;body(4).Hi];
    
    body(1).drit = tilde(body(1).dri);
    body(2).drit = tilde(body(2).dri);
    body(3).drit = tilde(body(3).dri);
    body(4).drit = tilde(body(4).dri);
    
    body(1).dric = body(1).dri + body(1).wit*body(1).rhoi;
    body(2).dric = body(2).dri + body(2).wit*body(2).rhoi;
    body(3).dric = body(3).dri + body(3).wit*body(3).rhoi;
    body(4).dric = body(4).dri + body(4).wit*body(4).rhoi;
    
    body(1).dHi = base.wit*body(1).Hi;
    body(2).dHi = body(1).wit*body(2).Hi;
    body(3).dHi = body(2).wit*body(3).Hi;
    body(4).dHi = body(3).wit*body(4).Hi;
    
    body(1).Di = [body(1).drit*body(1).Hi + body(1).rit*body(1).dHi;body(1).dHi]*body(1).dqi;
    body(2).Di = [body(2).drit*body(2).Hi + body(2).rit*body(2).dHi;body(2).dHi]*body(2).dqi;
    body(3).Di = [body(3).drit*body(3).Hi + body(3).rit*body(3).dHi;body(3).dHi]*body(3).dqi;
    body(4).Di = [body(4).drit*body(4).Hi + body(4).rit*body(4).dHi;body(4).dHi]*body(4).dqi;
    
    body(1).Yih = base.Yih + body(1).Bi*body(1).dqi;
    body(2).Yih = body(1).Yih + body(2).Bi*body(2).dqi;
    body(3).Yih = body(2).Yih + body(3).Bi*body(3).dqi;
    body(4).Yih = body(3).Yih + body(4).Bi*body(4).dqi;

end