"""[summary]
"""
from __future__ import annotations
from turtle import settiltangle
from typing import TYPE_CHECKING, Iterable, List

from numpy import var

from .header import BaseCollection, BaseStruct, get_format_by_key, MyList
from .weight import DEFAULT_BORDER
from .discript import Base_header, Header_list
from .formulas import dh, my_z
from . limit2 import Limit2
from dataclasses import dataclass
if TYPE_CHECKING:
    from .comp2 import Comp2
    from .mode import Mode
    from .mode2 import Mode2
    from .spch import Spch
    from .weight import Border
    from .comp import Stage

@Base_header('type_spch freq mght p_in p_out comp_degree w_cnt t_out percent_x volume_rate')
class _CompSummary:...
class CompSummary(_CompSummary):
    """Класс показателей работы ступени
    >>> CompSummary()
    <BLANKLINE>
           Тип СПЧ        |Частота|Мощность|Давл. вх|Ст. сжатия|Давл. вых(треб)|Пол. кпд|Об. расход|Помп. удал
                          | об/мин|   кВт  |   МПа  |  д. ед.  |      МПа      |  д. ед |  м3/мин  |   д. ед  
    ГПА-ц3-16С-45-1.7(ККМ)|   0   |   0    |  0.00  |   0.00   |     0.00      |  0.00  |    0     |    0     
    <BLANKLINE>
    """

    # def __init__(self, mode:Mode2) -> None:
    #     self._init_p_in(mode)
    #     from dataclasses import dataclass
    # def _init_p_in(self, mode:Mode2):
    #     self.pp = pp
        #         q_one = mode.q_in / self.w_cnt_current
        # t_in = mode.t_in if idx == 0 else self.t_avo
        # koef_raskh = self.type_spch[idx].koef_raskh(
        #     q_in=q_one, p_in=mode.p_input, freq=freq, t_in=t_in,
        #     r_val=self.r_val, plot_std=self.plot_std)
        # z_in = my_z(mode.p_input[idx], t_in)
        # kpd = self.type_spch[idx].calc_k_kpd(koef_raskh)
        # volume_rate, comp_degree = self.type_spch[idx].calc_xy(
        #     freq=freq, k_raskh=koef_raskh, z_val=z_in, r_val=self.r_val,
        #     t_in=t_in, k_val=self.k_val)
        # percent_x = self.type_spch[idx].percent_x_by_k_raskh(koef_raskh)
        # # return volume_rate, koef_raskh, z_in, self.r_val, t_in, self.k_val
        # res = CompSummary()
        # res.freq = freq
        # res.comp_degree = comp_degree
        # res.volume_rate = volume_rate
        # res.percent_x = percent_x
        # res.w_cnt = self.w_cnt_current
        # res.border = DEFAULT_BORDER
        # res.type_spch = self.type_spch[idx]
        # res.kpd = kpd
        # res.t_out = calc_t_out(self.k_val, comp_degree, t_in, kpd)
        # res.p_in = mode.p_input
        # res.p_out = comp_degree * mode.p_input
        # dh_val = dh(comp_degree, z_in, t_in, self.r_val, self.k_val, kpd)
        # res.mght = q_one * self.plot_std * (10**6) / 24 / 60 / 60 * dh_val / kpd / (10**3)
    def freq_dim(self):
        return self.freq / self.type_spch.fnom
    @property
    def gasoline_rate(self):
        return 0
    @property
    def prime(self)->float:
        return self.border.get_obj_val(self) - .01
    @property
    def second(self)->float:
        return self.mght*self.w_cnt/(10**3)

class CompSummaryCollection(BaseCollection[BaseStruct]):
    """Iterable-класс режимов работы компановки
    """
    def __init__(self,summaries:List[CompSummary]):
        lines = [
            BaseStruct(
                **{
                    key:comp_summ.mode[key]
                for key in comp_summ.mode.get_keys},
                **{
                    key:comp_summ[:,key]
                for key in comp_summ[0].get_keys}
            )
            for comp_summ in summaries]
        super().__init__(lines)
        
