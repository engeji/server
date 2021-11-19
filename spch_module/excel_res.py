"""Модуль для класса с файлами результатов в формате Excel
"""
from collections import namedtuple
from typing import List
import pandas
from . import ALL_SPCH_LIST
from .header import Header
from .modes import Comp, CompSummary, Stage, Mode, ModeCollection, CompSummaryCollection
from .limit import DEFAULT_LIMIT, GET_DEFAULT_LIMIT
0
class ResultExcelTable(Header):
    """Класс результатов расчетов из Excel
    """
    def __init__(self, file_path:str):
        f_excel = pandas.ExcelFile(file_path)
        self._data_frame: pandas.DataFrame = f_excel.parse(
            sheet_name=f_excel.sheet_names[0]
        )
        prove_cls = namedtuple('prove_tup', self._data_frame.columns)
        self._list_prove:List[prove_cls] = [
            prove_cls(**{
                column:row[1][column]
            for column in self._data_frame.columns})
        for row in self._data_frame.iterrows()]
        super().__init__(self._data_frame.columns)

        for item in self._list_prove:
            self.add_data(item._asdict().values())
        self._mode_collection:ModeCollection = []
        self._list_Comp:List[Comp] = []
        self._list_CompSummary:List[CompSummary] = []

    @property
    def get_mode_collection(self):
        """Массив режимов работы из Excel
        Returns:
            ModeCollection: Возвращяет экземпляр ModeCollection
        """
        if len(self._mode_collection) == 0:
            self._mode_collection = ModeCollection([
                Mode(
                    GET_DEFAULT_LIMIT('t_in'),
                    float(prove.q_in),
                    float(prove.p_in.split('+')[0]),
                    float(prove.p_out.split('+')[-1])
                )
            for prove in self._list_prove])
        return self._mode_collection
    @property
    def get_list_comp(self)->List[Comp]:
        if len(self._list_Comp) == 0:
            for prove in self._list_prove:
                list_spch = [
                    next(filter(lambda x: x.name == name, ALL_SPCH_LIST))
                for name in prove.type_spch.split('+')]
                list_w_cnt = list(map(float, prove.w_cnt.split('+')))
                self._list_Comp.append(Comp(
                    DEFAULT_LIMIT,
                    [
                        Stage(list_spch[idx], list_w_cnt[idx])
                    for idx in range(len(list_w_cnt))]
                ))
        return self._list_Comp
    @property
    def get_list_comp_summary(self)->List[CompSummary]:
        if len(self._list_CompSummary) == 0:
            for prove, comp, mod in zip(
                self._list_prove, self.get_list_comp, self.get_mode_collection
            ):
                self._list_CompSummary.append(
                    comp.calc_comp_summary(
                        mod, list(map(float, prove.freq.split('+')))
                    )
                )
        return self._list_CompSummary
    @property
    def get_CompSummaryCollection(self)->CompSummaryCollection:
        return CompSummaryCollection(self.get_list_comp_summary)
