"""Модуль класса компановка
"""
from __future__ import annotations
from .discript import Base_header, BaseData
from typing import List, TYPE_CHECKING, Union, List, Tuple
from .limit import Limit, DEFAULT_LIMIT
from .facilities import get_spch_by_name
from .formulas import my_z, dh, calc_t_out, ob_raskh
from .summary import CompSummary
from . weight import DEFAULT_BORDER
from . limit2 import Limit2
from .solver import Solver
from .mode2 import Mode2
if TYPE_CHECKING:
    from .spch import Spch
    from .mode import Mode

@Base_header('type_spch w_cnt r_val k_val plot_std t_avo dp_avo')
class _Comp(Limit2):...
class Comp2(_Comp):
    """
    >>> Comp2('ГПА-ц3-16С-45-1.7(ККМ)', 1)
    <BLANKLINE>
     Тип СПЧ |ГПА|   R    |Коефф. пол.|Ст. плот.|Т.АВО|Потери АВО
             | шт| Дж/кг К|   д. ед   |  кг/м3  |  К  |    МПа   
    16/45-1.7| 1 | 500.8  |   1.31    |  0.698  | 293 |   0.06   
    <BLANKLINE>
    >>> Comp2(['ГПА-ц3-16С-45-1.7(ККМ)', 'ГПА Ц3 16с76-1.7М'], [1,2])
    <BLANKLINE>
          Тип СПЧ      |ГПА|   R    |Коефф. пол.|Ст. плот.|Т.АВО|Потери АВО
                       | шт| Дж/кг К|   д. ед   |  кг/м3  |  К  |    МПа   
    16/45-1.7+16/76-1.7|1+2| 500.8  |   1.31    |  0.698  | 293 |   0.06   
    <BLANKLINE>
    >>> Comp2('ГПА-ц3-16С-45-1.7(ККМ)', 1) + Comp2('ГПА Ц3 16с76-1.7М', 2)
    <BLANKLINE>
          Тип СПЧ      |ГПА|   R    |Коефф. пол.|Ст. плот.|Т.АВО|Потери АВО
                       | шт| Дж/кг К|   д. ед   |  кг/м3  |  К  |    МПа   
    16/45-1.7+16/76-1.7|1+2| 500.8  |   1.31    |  0.698  | 293 |   0.06   
    <BLANKLINE>
    """
    def __init__(self,
        type_spch:Union[List[str], str]=None,
        w_cnt: Union[List[int], int]=None,
        lim: Union[List[Limit], Limit]=Limit2()):
        if isinstance(type_spch, list):
            assert len(type_spch) == len(w_cnt), ('Количество ГПА не соответсвтует количеству СПЧ')
            self.type_spch =[
                get_spch_by_name(sp)
            for sp in type_spch]
            self.w_cnt = w_cnt
            self._w_cnt_current = self.w_cnt
        elif isinstance(type_spch, str):
            self.w_cnt = w_cnt
            self._w_cnt_current = self.w_cnt
            self.type_spch = get_spch_by_name(type_spch)
        elif type_spch is None:
            self.type_spch = type_spch
            self.w_cnt = w_cnt
            self._w_cnt_current = w_cnt
        for key_lim in lim.params:
            setattr(self, key_lim, getattr(lim, key_lim))
        # if isinstance(lim, list):
        #     self.r_val = [l.r_val for l in lim]
        #     self.k_val = [l.k_val for l in lim]
        #     self.plot_std = [l.plot_std for l in lim]
        #     self.t_avo = [l.t_avo for l in lim]
        #     self.dp_avo = [l.dp_avo for l in lim]
        # else:
        #     self.r_val = [lim.r_val]
        #     self.k_val = [lim.k_val]
        #     self.plot_std = [lim.plot_std]
        #     self.t_avo = [lim.t_avo]
        #     self.dp_avo = [lim.dp_avo]

    @property
    def w_cnt_current(self):
        return self._w_cnt_current
    @w_cnt_current.setter
    def w_cnt_current(self, val):
        self._w_cnt_current = val
    def _calc_one_stage(self, mode:Mode2, idx:int, freq:float)->CompSummary:        
        q_one = mode.q_in / self.w_cnt_current
        t_in = mode.t_in if idx == 0 else self.t_avo
        koef_raskh = self.type_spch[idx].koef_raskh(
            q_in=q_one, p_in=mode.p_input, freq=freq, t_in=t_in,
            r_val=self.r_val, plot_std=self.plot_std)
        z_in = my_z(mode.p_input[idx], t_in)
        kpd = self.type_spch[idx].calc_k_kpd(koef_raskh)
        volume_rate, comp_degree = self.type_spch[idx].calc_xy(
            freq=freq, k_raskh=koef_raskh, z_val=z_in, r_val=self.r_val,
            t_in=t_in, k_val=self.k_val)
        percent_x = self.type_spch[idx].percent_x_by_k_raskh(koef_raskh)
        # return volume_rate, koef_raskh, z_in, self.r_val, t_in, self.k_val
        res = CompSummary()
        res.freq = freq
        res.comp_degree = comp_degree
        res.volume_rate = volume_rate
        res.percent_x = percent_x
        res.w_cnt = self.w_cnt_current
        res.border = DEFAULT_BORDER
        res.type_spch = self.type_spch[idx]
        res.kpd = kpd
        res.t_out = calc_t_out(self.k_val, comp_degree, t_in, kpd)
        res.p_in = mode.p_input
        res.p_out = comp_degree * mode.p_input
        dh_val = dh(comp_degree, z_in, t_in, self.r_val, self.k_val, kpd)
        res.mght = q_one * self.plot_std * (10**6) / 24 / 60 / 60 * dh_val / kpd / (10**3)
        return res

    def calc_via_p_in(self, mode:Mode2, freq:List[float]) -> CompSummary:
        res = self._calc_one_stage(mode, 0, BaseData(freq))
        cur_mode = mode.clone()
        cur_mode.p_input = res.p_out - self.dp_avo
        for idx in range(1, self._row_cnt):
            cur_cumm = self._calc_one_stage(cur_mode, idx, BaseData(freq))
            res += cur_cumm
            cur_mode.p_input = cur_cumm.p_out - self.dp_avo
        return res
    def _get_freq_min_max_one_stage(self, idx:int, mode:Mode2)->Tuple[float,float]:
        volume_rate = ob_raskh(mode.q_in[idx], mode.p_input, mode.t_in, self.r_val, self.plot_std) / self.w_cnt_current[idx]
        return self.type_spch[idx].get_freq_bound(volume_rate)

    def get_freq_bound_min_max(self, mode:Mode2, all_freqs:List[float])->Tuple[float,float]:
        assert len(all_freqs) == len(self
            ),"(Количество элементов списка частот должно совпадать с количеством ступеней)"
        res = [self[0]._get_freq_min_max_one_stage(0,mode)]
        p_in = mode.p_input
        t_in = mode.t_in
        for idx_stage, stage in list(enumerate(self))[1:]:
            prev_summ = self[idx_stage-1]._calc_one_stage(
                mode=Mode2(mode.q_in[idx_stage], p_in, t_in), idx=idx_stage-1, freq=all_freqs[idx_stage-1])
            p_in = p_in * prev_summ.comp_degree - stage.dp_avo
            t_in = stage.t_avo
            res.append(stage._get_freq_min_max_one_stage(idx_stage,Mode2(mode.q_in[idx_stage], p_in, t_in)))
        return res
        
    def calc_auto_p_in(self, mode: Mode2) -> CompSummary:
        pass    