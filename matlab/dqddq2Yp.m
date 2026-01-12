function Yp = dqddq2Yp(base, sub)

    global motion_flag

    Yp(1:3,1) = base.dri;
    Yp(4:7,1) = base.dpi;
    Yp(8:10,1) = base.ddri;
    Yp(11:13,1) = base.dwi;

    if motion_flag == 0
        indx = 14;
        for sindx = 1 : 6
            for i = 1 : 4
                Yp(indx, 1) = sub(sindx).body(i).dqi;
                indx = indx + 1;
            end
            for i = 1 : 4
                Yp(indx, 1) = sub(sindx).body(i).ddqi;
                indx = indx + 1;
            end
        end
    end

end