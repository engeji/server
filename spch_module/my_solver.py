import math
from typing import List

from scipy.optimize import minimize

from .comp import Comp, Result, Solush
from .spch import np


class Solver:
    def __init__(self, f, x0):
        self._f = f
        self._x0 = x0
    def calc(self):
        self.res = minimize(self._f, self._x0, method='nelder-mead',
            options={'xtol':1e-8, 'disp':True}
        )
    
        

