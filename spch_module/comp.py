from collections import namedtuple
from typing import Iterable, Tuple, List
from .formulas import my_z, dh
from .spch import Spch
from .struct import Limit, Mode
from .defaults import get_dic_HEADERS_LIST, Header
from typing import List, Tuple, Iterable
from .summary import Solv, BorderCollection
import math


class Comp:
    __slots__ = ('_p_in', '_q', '_t_in', '_spch_list', '_lim')   
    def __init__(self, spch_list:Iterable[Spch], lim:Limit):
        self._spch_list:Iterable[Spch] = spch_list
        self._lim:Limit = lim

    def _avo(self, p_out):
        return p_out - 0.06

    def get_sol_comp_by_mode(self, freqs: List[int], cur_mode:Mode)->List[Solv]:
        """Расчет режима для компановки по частотам

        Args:
            freqs (List[int]): Массив частот, об/мин
            cur_mode (Mode): Экземпляр режима

        Returns:
            List[spch_solv]: Массив показателей работы ступеней
        """        
        self._p_in = cur_mode.p_in
        self._t_in = cur_mode.t_in
        self._q = cur_mode.q
        res:List[Solv] = []
        for ind_stage, spch in enumerate(self._spch_list):
            res.append(spch.get_sol_stage_by_mode_and_limit(
                freqs[ind_stage], self._t_in, self._p_in, self._q, self._lim
            ))
            self._p_in = self._avo(res[-1].p_out_res)
            self._t_in = self._lim.t_avo
        return res
    
    def __repr__(self):
        return f'{" + ".join([str(s) for s in self._spch_list])} with {self._lim}'


class Solush(Mode):
    def set_sol_by_comp(self, freqs:Iterable[int], comp:Comp):
        self._sol_data:List[Solv] = comp.get_sol_comp_by_mode(freqs,self)    

    def get_data_line(self):
        return [
            *[
                f'{self.__getattribute__(head):.{get_dic_HEADERS_LIST(head)["dim"]}f}'
            for head in Mode.__slots__],
            *self.get_solv_line()
        ]

    def __repr__(self):
        return ' '.join(self.get_solv_line())

    def get_solv_line(self):
        return [
            '+'.join([
                f'{stage.__getattribute__(head):.{get_dic_HEADERS_LIST(head)["dim"]}f}' 
            for stage in self._sol_data])
        for head in Solv._fields]

    def get_all_objective_value(self, freqs:Iterable[int], comp:Comp, borders:BorderCollection)->List[float]:
        """[summary]

        Args:
            freqs (Iterable[int]): [description]
            comp (Comp): [description]
            borders (BorderCollection): [description]

        Returns:
            List[float]: [description]
        """        
        self.set_sol_by_comp(freqs, comp)

        weight_list, gasoline_rate = zip(*[
            [
                s.get_objective_value(borders),
                s.gasoline_rate
            ]
        for s in self._sol_data])
        #FIXME correct sum weight_list

        dp = abs(self._sol_data[-1].p_out_res - self.p_out)
        return (dp / .1)**2 + sum(weight_list)

class Result(Header):
    def __init__(self, list_sol:Iterable[Solush]=None):
        self._list_solush:Iterable[Solush] = [] if list_sol == None else [list_sol]
        self._idx = 0
        headers, dims = zip(*[
            get_dic_HEADERS_LIST(item)['title'].split(',')
        for item in [*Mode.__slots__, *Solv._fields]])
        super().__init__(headers, dims)
        for s in self._list_solush:
            self.append(s)
    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = self._list_solush[self._idx]
        except IndexError:
            self._idx = 0
            raise StopIteration()
        self._idx += 1
        return item

    def __getitem__(self, index):
        return self._list_solush[index]

    def append(self, sol: Solush):
        self._list_solush.append(sol)
        self.add_data(sol.get_solv_line())
    