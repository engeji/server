import math
from typing import List

from scipy.optimize import minimize
import numpy as np
from .mode import Mode
from .modes import Comp


class Solver:
    def __init__(self,comp:Comp,mode:Mode):
        self.comp:Comp = comp
        self.mode:Mode = mode
    def ob_func(self, x):
        return 100 * ((x[0] - x[1] ** x[1])**2) + (1 - x[0])**2

