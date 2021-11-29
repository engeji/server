import math
from itertools import chain
from typing import List

from scipy.optimize import minimize, Bounds, OptimizeResult
import numpy as np
import matplotlib.pyplot as plt
from .mode import Mode
from .modes import Comp, StageSummary

fig, ax = plt.subplots()
class Solver:
    def __init__(self,comp:Comp,mode:Mode):
        self.comp:Comp = comp
        self.mode:Mode = mode
    def ob_func(self, x):
        print(f'x is {x}')
        summ:StageSummary = self.comp.calc_comp_summary(self.mode, x).summaries[-1]
        res = (summ.p_in * summ.comp_degree - 8)**2
        return res

    def show_plt(self, point=None):
        X = np.arange(
            self.comp[0].type_spch.fnom*0.5,
            self.comp[0].type_spch.fnom*1.5,
            100)
        Y = np.arange(
            self.comp[1].type_spch.fnom*0.5,
            self.comp[1].type_spch.fnom*1.5,
            100)
        X, Y = np.meshgrid(X,Y)
        Z = self.ob_func([X,Y])
        map_min = np.min(Z)
        map_max = np.max(Z)
        def normolize():
            return (map_min + Z) / (map_max - map_min) * 100
        degries = [100,10,1,.1]
        lev = list(chain.from_iterable([
            [f / deg for f in np.linspace(1, 9, 10)]
        for idx, deg in enumerate(degries)]))
        CS = ax.contour(X, Y, Z)
        # if not point is None:
        #     CS2 = ax.scatter(*point)
        ax.clabel(CS)
        plt.show()
    @property
    def get_bounds(self):
        return Bounds(
            [
                stage.type_spch.fnom * 0.5
            for stage in self.comp],
            [
                stage.type_spch.fnom * 1.5
            for stage in self.comp]
        )

    def optimize(self)->OptimizeResult:
        return minimize(self.ob_func, np.array([5000,5000]), method='SLSQP', bounds=self.get_bounds)