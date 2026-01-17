function body = sub_position_analysis(body, base)

    for i = 1 : 4
        body(i).Aijpp = [cos(body(i).qi), -sin(body(i).qi), 0; sin(body(i).qi), cos(body(i).qi), 0; 0, 0, 1];
    end
    
    for i = 1 : 4
        if i == 1
            body(i).Ai = base.Ai*body(i).Cij*body(i).Aijpp;
            body(i).sij = base.Ai*body(i).sijp;
            body(i).ri = base.ri + body(i).sij;
        else
            body(i).Ai= body(i-1).Ai*body(i).Cij*body(i).Aijpp;
            body(i).sij = body(i-1).Ai*body(i).sijp;
            body(i).ri = body(i-1).ri + body(i).sij;
        end
    end
    
    body(4).se = body(4).Ai*body(4).sep;
    body(4).re = body(4).ri + body(4).se;
    body(4).Ae = body(4).Ai*body(4).Ce;
    body(4).rpy = mat2rpy(body(4).Ae);
    
    body(1).rhoi = body(1).Ai*body(1).rhoip;
    body(2).rhoi = body(2).Ai*body(2).rhoip;
    body(3).rhoi = body(3).Ai*body(3).rhoip;
    body(4).rhoi = body(4).Ai*body(4).rhoip;
    
    body(1).ric = body(1).ri + body(1).rhoi;
    body(2).ric = body(2).ri + body(2).rhoi;
    body(3).ric = body(3).ri + body(3).rhoi;
    body(4).ric = body(4).ri + body(4).rhoi;

end