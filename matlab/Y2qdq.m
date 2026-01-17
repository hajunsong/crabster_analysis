function [base, sub] = Y2qdq(Y, base, sub)

    global motion_flag

    base.ri = Y(1:3,1);
    base.pi = Y(4:7,1);
    base.dri = Y(8:10,1);
    base.wi = Y(11:13,1);

    if motion_flag == 0
        indx = 14;
        for sindx = 1 : 6
            for i = 1 : 4
                sub(sindx).body(i).qi = Y(indx, 1);
                indx = indx + 1;
            end
            for i = 1 : 4
                sub(sindx).body(i).dqi = Y(indx, 1);
                indx = indx + 1;
            end
        end
    end

end