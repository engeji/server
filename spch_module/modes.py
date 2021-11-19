"""Модуль класса входных данных
"""
from typing import Iterable, Union, List
from collections import namedtuple
from .spch import Spch
from .header import BaseCollection, Header, get_format_by_key
from .limit  import Limit
from .formulas import my_z, dh


LIST_ITEMS_MODE = 't_in q_in p_in p_out'
class Mode(namedtuple('Mode', LIST_ITEMS_MODE)):
    """Класс режима работы
    """

LIST_ITEMS_SUMMARY = 'type_spch mght kpd comp_degree volume_rate percent_x'
class StageSummary(namedtuple('Summary', LIST_ITEMS_SUMMARY)):
    """Класс показателей работы ступени
    """

LIST_ITEMS_STAGE = 'type_spch w_cnt'
class Stage(namedtuple('stage_tupe',LIST_ITEMS_STAGE)):
    """Класс ступени ДКС
    """
    def calc_stage_summary(
        self, q_in:float, p_in:float, t_in:float, lim:Limit, freq:float)->StageSummary:
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
        ob_raskh, comp_degree = spch.calc_xy(
            freq, k_raskh, z_in, lim.r_val, t_in, lim.k_val
        )
        kpd_pol = spch.calc_k_kpd(k_raskh)
        dh_val = dh(comp_degree, z_in, t_in, lim.r_val, lim.k_val, kpd_pol)
        percent_x = (k_raskh - spch.min_k_raskh) / (spch.max_k_raskh - spch.min_k_raskh) * 100
        mght = dh_val / kpd_pol * q_one / 24 / 60 / 60 * (10**6) * lim.plot_std / (10**3)
        return StageSummary(spch, mght, kpd_pol, comp_degree, ob_raskh, percent_x)

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
        for key in self._list_items[0]._asdict().keys()]

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
