from dataclasses import dataclass, field
import numpy as np

@dataclass
class subsystem:
    q: np.ndarray = field(default_factory=lambda: np.zeros(4, dtype=np.float64))
    dq: np.ndarray = field(default_factory=lambda: np.zeros(4, dtype=np.float64))
    ddq: np.ndarray = field(default_factory=lambda: np.zeros(4, dtype=np.float64))

    m1: float = 3.6
    m2: float = 12.9
    m3: float = 11.1
    m4: float = 11.5

    J1p: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))
    J2p: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))
    J3p: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))
    J4p: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))

    rho1p: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    rho2p: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    rho3p: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    rho4p: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))

    C11: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))
    C22: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))
    C33: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))
    C44: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))

    u_vec1: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    u_vec2: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    u_vec3: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    u_vec4: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))

    s12p: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    s23p: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    s34p: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    s4ep: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float64))

    C12: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))
    C23: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))
    C34: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))
    C4e: np.ndarray = field(default_factory=lambda: np.zeros((3, 3), dtype=np.float64))

