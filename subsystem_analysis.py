from data_container import *
import read_base as base
from typing import List

def sub_position_analysis(body: List[Body, Body, Body, Body]):
    # for i in range(0, 4): print(body[i].qi)
    for i in range(0, 4):
        body[i].Aijpp = [
            [np.cos(body[i].qi), -np.sin(body[i].qi), 0],
            [np.sin(body[i].qi),  np.sin(body[i].qi), 0],
            [0, 0, 1]
        ]

    for i in range(0, 4):
        if i == 0:
            body[i].Ai = base.Ai@body[i].Cij@body[i].Aijpp
            body[i].sij = base.Ai@body[i].sijp
            body[i].ri = base.ri + body[i].sij

    return body
    