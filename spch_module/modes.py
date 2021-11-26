"""Модуль класса входных данных
"""
from collections import namedtuple
from typing import Iterable, List, Tuple, Union, Optional

import numpy as np
import matplotlib.pyplot as plt

from .formulas import dh, my_z, ob_raskh, calc_c00
from .header import BaseCollection, Header, get_format_by_key
from .limit import Limit
from .mode import Mode
from .spch import Spch
from .gdh import get_gdh_curvs

LIST_ITEMS_SUMMARY = 'type_spch mght kpd comp_degree volume_rate percent_x t_out'
class StageSummary(namedtuple('Summary', LIST_ITEMS_SUMMARY)):
    """Класс показателей работы ступени
    """

LIST_ITEMS_STAGE = 'type_spch w_cnt'
class Stage(namedtuple('stage_tupe', LIST_ITEMS_STAGE)):
    """Класс ступени ДКС
    """
    def calc_stage_summary_in(self, q_in:float, p_in:float, t_in:float, lim:Limit, freq:float)->StageSummary:
        """Расчет одной ступени

        Args:
            q_in (float): Дебит всей ступени, млн. м3/сут
            p_in (float): Давление входа в ступень, МПа
            t_in (float): Температура газа на входе в ступень, К
            lim (Limit): Экземпляр класса ПВТ свойств
            freq (float): Частота, об/мин

        Returns:
            StageSummary: Показатель работы ступень
        """
        spch:Spch = self.type_spch
        q_one = q_in / self.w_cnt
        k_raskh = spch.koef_raskh(
            q_one, p_in, freq, t_in, lim.r_val, lim.plot_std
        )
        z_in = my_z(p_in, t_in)
        ob_raskh_val, comp_degree = spch.calc_xy(
            freq, k_raskh, z_in, lim.r_val, t_in, lim.k_val
        )
        kpd_pol = spch.calc_k_kpd(k_raskh)
        dh_val = dh(comp_degree, z_in, t_in, lim.r_val, lim.k_val, kpd_pol)
        percent_x = (k_raskh - spch.min_k_raskh) / (spch.max_k_raskh - spch.min_k_raskh) * 100
        mght = dh_val / kpd_pol * q_one / 24 / 60 / 60 * (10**6) * lim.plot_std / (10**3)
        t_out = t_in * (comp_degree ** (lim.k_val - 1 ) / (lim.k_val * kpd_pol))
        return StageSummary(spch, mght, kpd_pol, comp_degree, ob_raskh_val, percent_x, t_out)

    def get_freq_max_min(self, mode:Mode, lim:Limit)->Tuple[float]:
        return self.type_spch.get_freq_bound(mode.get_volume_rate(lim) / self.w_cnt)
    def show_plt(self, lim:Limit, t_in:float, f_max:float, f_min:float, summ:Iterable[StageSummary]=None):
        sp:Spch = self.type_spch
        list_all_curve = get_gdh_curvs(
            sp, t_in, k=lim.k_val, R=lim.r_val, plot_st=lim.plot_std, freqs=np.linspace(f_max,f_min,9))['gdh']['datasets']
        list_freq_curve = list(filter(lambda dic: dic['my_type']=='freq', list_all_curve))
        curves = list(map(lambda dic: dic['data'], list_freq_curve))
        for curv in curves:
            x_val,y_val, label = list(zip(*[
                [dic['x'], dic['y'], dic['label']]
            for dic in curv]))
            plt.plot(x_val,y_val)
            plt.annotate(label[0], (x_val[0],y_val[0]))
        if isinstance(summ, Iterable):
            for cur_summ in summ:
                plt.scatter(cur_summ.volume_rate, cur_summ.comp_degree)
        plt.show()

class ModeCollection(BaseCollection):
    """Iterable-класс режимов работы
    """
    def __init__(self, modes:Union[Mode, Iterable[Mode]]):
        """Конструктор класса массива режимов работы

        Args:
            modes (Union[Mode, Iterable[Mode]]): Режим(ы) работы
        """
        super().__init__(modes)

class CompSummary(BaseCollection):
    """Iterable-класс показателей работы компановки
    """
    def __init__(self, res:Iterable[StageSummary], mode:Mode):
        """Конструктор класса результатов работы компановки

        Args:
            res (Iterable[StageSummary]): Показатель(и) работы ступени
            mode (Mode): Режим работы
        """
        super().__init__(res)
        self.mode = mode
        self.summaries:Iterable[StageSummary] = res
    def get_list_str_with_plus(self)->Iterable[str]:
        """Строковое представление показателей работы компановки

        Returns:
            Iterable[str]: Возврощяет Iterable строковых представлений работы компановки,
                в виде 'показатель1+показатель2+...показательN'
        """
        return [
            '+'.join([
                f'{item.__getattribute__(key):{get_format_by_key(key)}}'
            for item in self._list_items])
        for key in self._list_items[0]._asdict().keys()] #FIXME перенести меня в CompCollection


class Comp(BaseCollection):
    """Класс компановки ДКС
    """
    def __init__(self, lim: Limit, stages:Union[Stage, Iterable[Stage]]):
        """Конструктор компановки ДКС

        Args:
            lim (Limit): ПВТ-свойтва при компримировани
            stages (Union[Stage, Iterable[Stage]]): Ступень(и) ДКС
        """
        self.lim = lim
        super().__init__(stages)
    def calc_comp_summary(self, mode: Mode, freqs:Iterable[float])->CompSummary:
        """Расчет работы компановки

        Args:
            mode (Mode): Режим работы
            freqs (Iterable[float]): Частота(ы), об/мин
                (Количесвто элементов списка должно совпадать с количесвтом ступеней)

        Returns:
            CompSummary: возврощяет показатель работы компановки
        """
        assert len(freqs) == len(self._list_items
            ),"(Количесвто элементов списка частот должно совпадать с количесвтом ступеней)"
        _p_in = mode.p_in
        _t_in = mode.t_in
        _res:List[StageSummary] = []
        for stage, freq in zip(self._list_items, freqs):
            _res.append(
                stage.calc_stage_summary_in(
                    mode.q_in, _p_in, mode.t_in, self.lim, freq
                )
            )
            _p_in *= _res[-1].comp_degree - self.lim.dp_avo
            _t_in = self.lim.t_avo
        return CompSummary(_res, mode)
    def get_freq_bound(self, mode:Mode):
        stage_1:Stage = self._list_items[0]
        f_max, f_min = stage_1.get_freq_max_min(mode,self.lim)
        freq_arr = np.linspace(f_max, f_min, 20)
        res = []
        list_summ:List[StageSummary] = [
            stage_1.calc_stage_summary_in(mode.q_in, mode.p_in, mode.t_in,self.lim, cur_freq)
        for cur_freq in freq_arr]

        for stage in self[1:]:
            st:Stage = stage
            list_mode:List[Mode] = [
                Mode(self.lim.t_avo, mode.q_in, mode.p_in * summ.comp_degree - self.lim.dp_avo)
            for summ in list_summ]

            list_freqs = [
                [
                    *st.get_freq_max_min(mod,self.lim)
                ]
            for idx, mod in enumerate(list_mode)]

            c00_max, c00_min = [
                calc_c00(freq_arr, y_cur, 3)
            for y_cur in zip(*list_freqs)]
            res.append([c00_max, c00_min])
        return res

    def show_plt(self, mode:Mode, f_max:float, f_min:float, summ:StageSummary):
        stage_1:Stage = self._list_items[0]
        f_dim_max = f_max / stage_1.type_spch.fnom
        f_dim_min = f_min / stage_1.type_spch.fnom
        stage_1.show_plt(self.lim, mode.t_in,f_dim_max, f_dim_min,summ)

class CompSummaryCollection(Header):
    """Iterable-класс режимов работы компановки
    """
    def __init__(self, summarires: Iterable[CompSummary]):
        """Конструктор Iterable-класса режимов работы компановки

        Args:
            summarires (Iterable[CompSummary]): режим(ы) работы компановки
        """
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
