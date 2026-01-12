function data_save(fp, sub, base, step, t_c)

    fprintf(fp, '%d, %3.3f, ',step, t_c);
    for i = 1 : 6
        fprintf(fp, '%3.7f, %3.7f, %3.7f, %3.7f, %3.7f, %3.7f, ', sub(i).body(1).qi, sub(i).body(2).qi, sub(i).body(3).qi, sub(i).body(4).qi, 0, 0);
        fprintf(fp, '%3.7f, %3.7f, %3.7f, %3.7f, %3.7f, %3.7f, ', sub(i).body(1).dqi, sub(i).body(2).dqi, sub(i).body(3).dqi, sub(i).body(4).dqi, 0, 0);
        fprintf(fp, '%3.7f, %3.7f, %3.7f, %3.7f, %3.7f, %3.7f, ', sub(i).body(1).ddqi, sub(i).body(2).ddqi, sub(i).body(3).ddqi, sub(i).body(4).ddqi, 0, 0);
        fprintf(fp, '%3.7f, %3.7f, %3.7f, ', sub(i).body(4).re'*1000);
        fprintf(fp, '%3.7f, %3.7f, %3.7f, ', sub(i).body(4).rpy);
    end
    fprintf(fp, '%3.7f, %3.7f, %3.7f, %3.7f, %3.7f, %3.7f, ', base.ric*1000', base.rpy');
    fprintf(fp, '%3.7f, %3.7f, %3.7f, %3.7f, %3.7f, %3.7f, ', base.dric*1000', base.wi');
    fprintf(fp, '%3.7f, %3.7f, %3.7f, %3.7f, %3.7f, %3.7f, ', base.ddric*1000', base.dwi');
    for i = 1 : 6
        for j = 1 : 4
            fprintf(fp, '%3.7f, ', sub(i).body(j).Ti_RSDA*1000);
        end
        fprintf(fp, '%3.7f, %3.7f, ', 0, 0);
    end
    fprintf(fp, '\n');

end