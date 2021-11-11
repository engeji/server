import math
from types import SimpleNamespace
from itertools import groupby
from matplotlib import pyplot as plt
import numpy as np
import pandas
from numpy import linalg as LA
from .formulas import ob_raskh, my_z, dh, plot
from collections import namedtuple
from .struct import DEFAULT_SETTINGS, Limit
from typing import List
from .summary import Solv
import re
# from .comp import Solush
class Spch:           
    """ Класс для Сменной проточной части (СПЧ)
    """
    def _init_from_txt(self, text, title):
        self.name = title
        _, HEAD, DATA = re.split(r'HEAD\n|\nDATA\n', text)
        self.mgth, self.stepen, self.R, self.T, self.ptitle, self.ppred, self.fnom, z = [
            float(next(filter(lambda x: x[0]==letter, [line.split('\t') for line in HEAD.split('\n')]))[1])
        for letter in 'mght eps R T p_title Ppred fnom Z'.split()]
        self.d = .8
        dic_header = {head:ind for ind, head in enumerate(DATA.split('\n')[0].split('\t'))}
        all_points = [
            SimpleNamespace(
                q = float(line.split('\t')[dic_header['q']]),
                kpd = float(line.split('\t')[dic_header['kpd']]),
                freq = float(line.split('\t')[dic_header['f']]) * self.fnom,
                comp = float(line.split('\t')[dic_header['comp']]),
            )
        for line in DATA.split('\n')[1:]]
        self._freq, self._x_raskh, self._y_kpd, self._y_nap = np.array([(
            x.freq,
            self.koef_raskh_by_ob(x.q, x.freq),
            x.kpd,
            self.koef_nap_by_comp(x.comp, x.freq, self.T, self.R, x.kpd, z),
        ) for x in all_points], dtype=object).T     

    def __init__(self, sheet=None, text=None, title=None):
        self._c00_kpd = self._c00_nap = ()
        self.R=self.T=self.P=self.stepen=self.d=self.ppred=self.mgth=self.ptitle=self.fnom=0    
        self.name = ''     
        if text != None:
            self._init_from_txt(text, title)
        elif sheet != None:
            self._init_from_xl(sheet)
        
        self._min_k_raskh, self._max_k_raskh = (
            f(self._x_raskh) for f in (min, max)
        )        

    def _init_from_xl(self, sheet):
        """инициализация

        Args:
            sheet (xlrd.sheet.Sheet): Лист из базы данных
        """
        self.name = sheet.name
        lines = [[coll.value for coll in list(row)] for row in list(sheet.get_rows())]       
        self.ind_end_points = [line[0] for line in lines].index('//')
        all_points = []               
        for ind in range(self.ind_end_points):
            if lines[ind][0] != '/':                 
                all_points += [SimpleNamespace(
                    Q = lines[ind][0],
                    PinMPa = lines[ind][1],
                    kpd = float(lines[ind][4]),
                    freq = float(lines[ind][5]))]

        all_attribs = {lines[ind][0]:lines[ind][1]  for ind in range(self.ind_end_points+1, len(lines))}                       
        self.__dict__ = {**self.__dict__,
            **{letter:all_attribs[letter] for letter in ('R', 'T', 'P', 'stepen', 'd', 'ppred', 'mgth', 'ptitle', 'fnom')}}                
        self.ptitle = float(self.ptitle)
        self._x_raskh, self._y_nap, self._y_kpd, self._freq = np.array([[
            self.koef_raskh(x.Q, x.PinMPa, x.freq, self.T, self.R, DEFAULT_SETTINGS.plot),
            self.koef_nap(x.PinMPa, 
                self.P, x.freq, self.T, self.R, x.kpd),
            x.kpd,
            x.freq
        ] for x in all_points], dtype=object).T
                     
    def _calc_c00(self, x:list, y:list, power)-> tuple:
        a = np.vstack([[v ** p for p in range(power)] for v in x])        
        return LA.lstsq(a, np.array(y, dtype=float), rcond=None)[0]
    

   
        


