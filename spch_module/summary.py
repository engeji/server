# @Base_header('type_spch freq mght p_in p_out comp_degree w_cnt t_out percent_x volume_rate')
import __future__

import re
from typing import TYPE_CHECKING, List

from .header import Header, Header_list, Iterable
from .formulas import dh, my_z
if TYPE_CHECKING:
    from .spch import Spch
    from .comp import Comp
    from .stage import _Stage


class Summary(Header):
    def __init__(self, _stage:'_Stage', q_stage:float, p_in:float, t_in:float, freq:float, w_cnt_current:int) -> None:
        self.stages = [_stage]
        self.type_spch = [_stage.type_spch]
        self.freq = [freq]
        self.p_in = [p_in]
        self.w_cnt_current = [w_cnt_current]
        self._q_in = [q_stage]
        self._keys = 'type_spch freq mght p_in p_out comp_degree w_cnt_current t_out percent_x volume_rate'.split()
        self.volume_rate, self.comp_degree, self.percent_x, self.kpd = tuple(
            [v] for v in  _stage.calc_xy_percent_kpd(q_stage/w_cnt_current, p_in, t_in, freq)
        )
        z_in = my_z(p_in, t_in)
        dh_val = dh(self.comp_degree[0], z_in, t_in, _stage.r_val, _stage.k_val, self.kpd[0])
        self.mght = [q_stage / w_cnt_current * _stage.plot_std* (10**6) / 24 / 60 / 60 * dh_val / self.kpd[0] / (10**3)]
        self.t_out = [_stage._lim.get_t_out(self.comp_degree[0], t_in, self.kpd[0])]
    @property
    def p_out(self): return [comp_degree * p_in for comp_degree, p_in in zip(self.comp_degree,self.p_in)]

    def __add__(self, other:"Summary")->"Summary": #FIXME: добавить None
        if other == None:
            return self
        assert isinstance(other, Summary), TypeError(f'Не поддерживамый тип для {other}')
        for key in filter(lambda key: key[0] != '_', self.__dict__):
            getattr(self, key).extend(getattr(other, key))
        return self
    @classmethod
    def sum(cls, __iterable:Iterable['Summary'])->'Summary':
        seed = __iterable[0]
        for item in range(1, len(__iterable)):
            seed += __iterable[item]
        return seed
    def __len__(self)->int:return len(self.stages)

        