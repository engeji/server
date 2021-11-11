import os
import sys
sys.path.append(r'E:\macro\dks_vue\server')
from collections import namedtuple
from itertools import chain
from typing import Iterable, List

import matplotlib.pyplot as plt
import numpy as np
import pandas
from matplotlib import cm
from spch_module.comp import Solush  # pylint: disable=import-error
from spch_module.defaults import (BORDER_LIST,  # pylint: disable=import-error
                                  DEFAULT_LIMITS)
from spch_module.my_solver import Solver  # pylint: disable=import-error
from spch_module.struct import Limit   # pylint: disable=import-error
from spch_module.summary import Solv, BorderCollection, One_Border  # pylint: disable=import-error

from test_main import Main_test
class My_cls(tuple):
    def __new__(_cls, a, b, c):
        print(locals())
        return tuple.__new__(_cls, (a,b,c))

print(f"res={My_cls(*'1 2 3'.split(' '))}")

fig, ax = plt.subplots()
class Test_solv(Main_test):
    def __init__(self, path, lim, border_list:BorderCollection):
        self._border_list = border_list
        super().__init__(path, lim)
        ind = 13
        p = self._list_prove[ind]
        t_in = next(filter(lambda x: x['key']=='t_in', DEFAULT_LIMITS))['value']
        self._s = Solush(
            q = float(p.q) / float(p.w_cnt.split('+')[0]),
            p_in = float(p.p_in.split('+')[0]),
            p_out = float(p.p_out_req),
            t_in = float(t_in)
        )
        self._X, self._Y = np.meshgrid(*[
            np.arange(.5 * sp.fnom, 1.15 * sp.fnom, 50)
        for sp in self._spch_steps])
        f = lambda x1, y1: self._s.get_all_objective_value([x1,y1], self._comp, self._border_list)
        self._np_f = np.vectorize(f)
    

    def show_plt(self):
        Z = self._np_f(self._X, self._Y)
        
        map_min = np.min(Z)
        map_max = np.max(Z)
        def normolize():
            return (map_min + Z) / (map_max - map_min) * 100
        degries = [100,10,1,.1]
        lev = list(chain.from_iterable([
            [f / deg for f in np.linspace(1, 9, 10)]
        for idx, deg in enumerate(degries)]))       
        # color_region = np.zeros((len(lev),3))
        # color_region[:,1:] = .2
        # color_region[:,0] = np.linspace(0,1,len(lev))
        CS = ax.contour(self._X, self._Y, normolize(), lev)
        ax.clabel(CS)
        plt.show()

    def test_solv(self):
        s = Solver(self._np_f, np.array([sp.fnom for sp in self._spch_steps]))
        print(s.res)

if __name__ == "__main__":
    lim = Limit(**{
        dic['key']:dic['value']
    for dic in DEFAULT_LIMITS})  
    dks9 = r'tests\for_tst_2step.xlsx'
    bor = BorderCollection([
        One_Border(**dic)
    for dic in BORDER_LIST])
    t = Test_solv(dks9,lim,bor)
    t.show_plt()

