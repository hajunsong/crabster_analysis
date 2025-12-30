from read_data import *
import read_base as base

body1 = read_R_body1(base.sijp_FR, base.Cij_FR)
body2 = read_R_body2()
body3 = read_R_body3()
body4 = read_R_body4()
body = [body1, body2, body3, body4]