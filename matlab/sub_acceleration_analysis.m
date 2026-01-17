function body = sub_acceleration_analysis(body, base)

    body(1).dYih = base.dYih + body(1).Bi*body(1).ddqi + body(1).Di;
    body(2).dYih = body(1).dYih + body(2).Bi*body(2).ddqi + body(2).Di;
    body(3).dYih = body(2).dYih + body(3).Bi*body(3).ddqi + body(3).Di;
    body(4).dYih = body(3).dYih + body(4).Bi*body(4).ddqi + body(4).Di;
    
    for i = 1 : 4
        body(i).Ti = [eye(3) -body(i).rit; zeros(3) eye(3)];
        body(i).dTi = [zeros(3) -body(i).drit; zeros(3,6)];
        body(i).Ri = [body(i).drit*body(i).wi; zeros(3,1)];
        body(i).dYib = body(i).dTi*body(i).Yih + body(i).Ti*body(i).dYih;
        
        body(i).ddri = body(i).dYib(1:3,1);
        body(i).dwi = body(i).dYib(4:6,1);
        body(i).dwit = tilde(body(i).dwi);
        
        body(i).ddric = body(i).ddri + body(i).dwit*body(i).rhoi + body(i).wit*body(i).wit*body(i).rhoi;
    end

end