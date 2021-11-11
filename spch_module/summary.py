from collections import namedtuple
from typing import Iterable
import math

c00_gasoline = [0.00550941, 29.38351752]
SOLV_LIST = [
    'freq',
    'freq_dim',
    'mght',
    'p_out_res',
    'volume_rate',
    'comp_degree',
    'percent_x',
    'kpd',
    't_out'
]

One_Border = namedtuple('bor_tup','key weight max_val min_val')   

class BorderCollection:
    def __init__(self, borders:Iterable[One_Border]):
        self._borders:Iterable[One_Border] = borders
        self._idx = 0

    def __iter__(self):
        return self

    @property
    def get_mid_border(self):
        return {
            bor.key: bor.min_val + (bor.max_val - bor.min_val) / 2
        for bor in self._borders}
    def __next__(self):
        try:
            item = self._borders[self._idx]
        except IndexError:
            self._idx = 0
            raise StopIteration()
        self._idx += 1
        return item

class Solv(namedtuple('spch_solv', SOLV_LIST)):    
    def _get_norm_value(self, val, min_val, max_val):
        if min_val <= val <= max_val:
            return 0            
        return math.fabs((val - min_val) / (max_val - min_val))

    @property
    def gasoline_rate(self):
        res = c00_gasoline[0] * self.mght + c00_gasoline[1]
        return res if res > 0 else 0

    def get_objective_value(self, borders:BorderCollection):
        sum_weight =  sum([            
            self._get_norm_value(self.__getattribute__(b.key), b.min_val, b.max_val)*b.weight
        for b in borders])
        return sum_weight
    
    
        
        
        
