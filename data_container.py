import numpy as np
from dataclasses import dataclass, field
from utils import *

@dataclass
class Body:
    # joint states
    qi: float = 0.0
    qi_init: float = 0.0
    dqi: float = 0.0
    ddqi: float = 0.0

    # pose
    ri: np.ndarray = field(default_factory=lambda: np.zeros(3))
    pi: np.ndarray = field(default_factory=lambda: np.array([1,0,0,0]))
    Ai: np.ndarray = field(default_factory=lambda: np.eye(3))
    rpy: np.ndarray = field(default_factory=lambda: np.zeros(3))

    dri: np.ndarray = field(default_factory=lambda: np.zeros(3))
    wi: np.ndarray = field(default_factory=lambda: np.zeros(3))

    # params
    mi: float = 1.0
    Jip: np.ndarray = field(default_factory=lambda: np.eye(3))
    rhoip: np.ndarray = field(default_factory=lambda: np.zeros(3))
    Cii: np.ndarray = field(default_factory=lambda: np.eye(3))

    # parent-child kinematic params
    sijp: np.ndarray = field(default_factory=lambda: np.zeros(3))
    Cij: np.ndarray = field(default_factory=lambda: np.eye(3))
    sij: np.ndarray = field(default_factory=lambda: np.zeros(3))

    # derived: COM
    rhoi: np.ndarray = field(default_factory=lambda: np.zeros(3))
    ric: np.ndarray = field(default_factory=lambda: np.zeros(3))
    rict: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))

    # end-effector (only link4 has se, Ce)
    sep: np.ndarray | None = None
    se: np.ndarray | None = None
    Ce: np.ndarray | None = None
    re: np.ndarray | None = None
    Ae: np.ndarray | None = None
    dre: np.ndarray | None = None

    # analysis intermediate (MATLAB-like)
    Aijpp: np.ndarray = field(default_factory=lambda: np.eye(3))
    u_vec: np.ndarray = field(default_factory=lambda: np.array([0,0,1]))
    Hi: np.ndarray = field(default_factory=lambda: np.zeros(3))
    dHi: np.ndarray = field(default_factory=lambda: np.zeros(3))
    Di: np.ndarray = field(default_factory=lambda: np.zeros(6))
    Bi: np.ndarray = field(default_factory=lambda: np.zeros(6))

    wit: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))
    rit: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))
    drit: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))
    dric: np.ndarray = field(default_factory=lambda: np.zeros(3))
    drict: np.ndarray = field(default_factory=lambda: np.zeros((3, 3)))

    fic: np.ndarray = field(default_factory=lambda: np.zeros(3))
    tic: np.ndarray = field(default_factory=lambda: np.zeros(3))

    Ai_Cii: np.ndarray = field(default_factory=lambda: np.eye(3))
    Jic: np.ndarray = field(default_factory=lambda: np.eye(3))

    ddri: np.ndarray = field(default_factory=lambda: np.zeros(3))
    dwi: np.ndarray = field(default_factory=lambda: np.zeros(3))
    ddric: np.ndarray = field(default_factory=lambda: np.zeros(3))

@dataclass
class SubSystem:
    body1: Body = field(default_factory=Body)
    body2: Body = field(default_factory=Body)
    body3: Body = field(default_factory=Body)
    body4: Body = field(default_factory=Body)
    M: np.ndarray = field(default_factory=lambda: np.zeros((4,4)))
    Q: np.ndarray = field(default_factory=lambda: np.zeros(4))
    Myq: np.ndarray = field(default_factory=lambda: np.zeros((6,4)))
    ddq: np.ndarray = field(default_factory=lambda: np.zeros(4,1))


