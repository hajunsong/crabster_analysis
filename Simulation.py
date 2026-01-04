import numpy as np

t_c: float = 0
dt: float = 0
t_e: float = 0
g: float = 0
step: float = 0
motion_flag: bool = False

L_q_init = np.zeros(4, dtype=float)
R_q_init = np.zeros(4, dtype=float)
