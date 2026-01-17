function [p, v, a] = joint_motion(t_c, x0, h0, x1, h1)

    if t_c <= x0
        p = h0;
        v = 0;
        a = 0;
    elseif t_c >= x1
        p = h1;
        v = 0;
        a = 0;
    else
        h = x1 - x0;
        s = (t_c - x0)/h;
        p = h0 + (h1 - h0)*(10*s*s*s - 15*s*s*s*s + 6*s*s*s*s*s);
        v = ((h1 - h0)/h)*(30*s*s - 60*s*s*s + 30*s*s*s*s);
        a = ((h1 - h0)/(h*h))*(60*s - 180*s*s + 120*s*s*s);
    end

end