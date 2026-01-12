function [base, FL, ML, RL, FR, MR, RR] = read_data()

    base = read_base();
    FL = read_FL(base.sijp_FL, base.Cij_FL);
    ML = read_ML(base.sijp_ML, base.Cij_ML);
    RL = read_RL(base.sijp_RL, base.Cij_RL);
    FR = read_FR(base.sijp_FR, base.Cij_FR);
    MR = read_MR(base.sijp_MR, base.Cij_MR);
    RR = read_RR(base.sijp_RR, base.Cij_RR);

end