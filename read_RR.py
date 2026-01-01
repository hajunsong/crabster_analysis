from read_data import *
import read_base as base

body1 = read_R_body1(base.sijp_RR, base.Cij_RR)
body2 = read_R_body2()
body3 = read_R_body3()
body4 = read_R_body4()
body = [body1, body2, body3, body4]
M: np.ndarray = field(default_factory=lambda: np.zeros((4,4)))
Q: np.ndarray = field(default_factory=lambda: np.zeros(4))
Myq: np.ndarray = field(default_factory=lambda: np.zeros((6,4)))
ddq: np.ndarray = field(default_factory=lambda: np.zeros(4))