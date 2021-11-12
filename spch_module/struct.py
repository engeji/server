from collections import namedtuple
from .defaults import DEFAULT_LIMITS, HEADERS_LIST
# from .comp import Comp

from typing import Iterable


class Limit:
    __slots__ = (dic['key'] for dic in DEFAULT_LIMITS)
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])
class Mode:
    __slots__ = 'q p_in p_out t_in'.split()
    def __init__(self, q, p_in, p_out, t_in):        
        self.q = q
        self.p_in = p_in
        self.p_out = p_out
        self.t_in = t_in
    