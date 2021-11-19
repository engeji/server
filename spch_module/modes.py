"""Модуль класса входных данных
"""
from typing import Iterable, Union, List, TypeVar, NamedTuple, Tuple
from collections import namedtuple
from .spch import Spch
from .header import BaseCollection, Header, get_format_by_key
from .limit  import Limit
from .formulas import my_z, dh


list_items_mode = 't_in q_in p_in p_out'
class Mode(namedtuple('Mode', list_items_mode)):...


list_items_summary = 'type_spch mght kpd comp_degree volume_rate percent_x'
class StageSummary(namedtuple('Summary', list_items_summary)):...
 

class clas_name:

self.a b


list_items_stage = 'type_spch w_cnt'
class Stage(namedtuple('stage_tupe',list_items_stage)):
    def calc_stage_summary(self, q_in, p_in, t_in, lim:Limit, freq:float)->StageSummary:
        spch:Spch = self.type_spch
        q_one = q_in / self.w_cnt
        k_raskh = spch.koef_raskh(
            q_one, p_in, freq, t_in, lim.r_val, lim.plot_std
        )
        z_in = my_z(p_in, t_in)
        ob_raskh, comp_degree = spch.calc_xy(
            freq, k_raskh, z_in, lim.r_val, t_in, lim.k_val
        )
        kpd_pol = spch.calc_k_kpd(k_raskh)
        dh_val = dh(comp_degree, z_in, t_in, lim.r_val, lim.k_val, kpd_pol)
        percent_x = (k_raskh - spch.min_k_raskh) / (spch.max_k_raskh - spch.min_k_raskh) * 100
        mght = dh_val / kpd_pol * q_one / 24 / 60 / 60 * (10**6) * lim.plot_std / (10**3)
        return StageSummary(spch, mght, kpd_pol, comp_degree, ob_raskh, percent_x)

class ModeCollection(BaseCollection):
    def __init__(self, modes:Union[Mode, Iterable[Mode]]):
        super().__init__(modes)

class CompSummary(BaseCollection):
    def __init__(self, res:Iterable[StageSummary], mode:Mode):
        super().__init__(res)
        self.mode = mode
    def get_list_str_with_plus(self)->Iterable[str]:
        return [
            '+'.join([
                f'{item.__getattribute__(key):{get_format_by_key(key)}}'
            for item in self._list_items])
        for key in self._list_items[0]._asdict().keys()]
        
class Comp(BaseCollection):
    def __init__(self, lim: Limit, stages:Union[Stage, Iterable[Stage]]):
        self.lim = lim
        super().__init__(stages)
    def calc_comp_summary(self, mode: Mode, freqs:Iterable[float])->CompSummary:
        assert len(freqs) == len(self._list_items),""
        _p_in = mode.p_in
        _t_in = mode.t_in
        _res:List[StageSummary] = []
        for stage, freq in zip(self._list_items, freqs):
            _res.append(
                stage.calc_stage_summary(
                    mode.q_in, _p_in, mode.t_in, self.lim, freq
                )
            )
            _p_in *= _res[-1].comp_degree - self.lim.dp_avo
            _t_in = self.lim.t_avo
        return CompSummary(_res, mode)

class CompSummaryCollection(Header):
    def __init__(self, summarires: Iterable[CompSummary]):
        super().__init__((
            *summarires[0].mode._fields,
            *summarires[0]._list_items[0]._fields
        ))
        for summ in summarires:
            self.add_data(
                [
                    *[
                        f'{summ.mode._asdict()[key]:{get_format_by_key(key)}}'
                    for key in summ.mode._asdict().keys()],
                    *summ.get_list_str_with_plus()
                ]
            )
