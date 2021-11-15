"""Модуль для класса с файлами результатов в формате Excel
"""
from collections import namedtuple
from typing import List
import pandas
from .header import Header, get_dic_HEADERS_LIST

class ResultExcelTable(Header):
    """Класс результатов расчетов
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
        super().__init__(*zip(*[
            get_dic_HEADERS_LIST(head)['title'].split(',')
        for head in self._data_frame.columns]))

        for item in self._list_prove:
            self.add_data(item._asdict().values())
