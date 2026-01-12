function Y = define_Y_vector(base, sub)

    global motion_flag

    Y(1:3,1) = base.ri;
    Y(4:7,1) = base.pi;
    Y(8:10,1) = base.dri;
    Y(11:13,1) = base.wi;

    if motion_flag == 0
        indx = 14;
        for sindx = 1 : 6
            for i = 1 : 4
                Y(indx, 1) = sub(sindx).body(i).qi_init;
                indx = indx + 1;
            end
            for i = 1 : 4
                Y(indx, 1) = sub(sindx).body(i).dqi;
                indx = indx + 1;
            end
        end
    end

end