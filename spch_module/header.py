"""Модуль для класса заголовков для переопределения repr в виде таблицы
"""
from typing import Iterable, Union, List, NamedTuple

HEADERS_LIST = [
    {"fmt":".2f", "key":"q_in", "title":"Комер. расх., млн. м3/сут"},
    {"fmt":".0f", "key":"t_in", "title":"Темп. входа, К"},
    {"fmt":".2f", "key":"p_in_req", "title": "Давл. вх(треб), МПа"},
    {"fmt":".2f", "key":"p_out_req", "title": "Давл. вых(треб), МПа"},
    {"fmt":".2f", "key":"p_in", "title": "Давл. вх, МПа"},
    {"fmt":".2f", "key":"p_out", "title": "Давл. вых, МПа"},
    {"fmt":""   , "key":"type_spch", "title": "Тип СПЧ,"},
    {"fmt":".0f", "key":"freq", "title": "Частота, об/мин"},
    {"fmt":".0f", "key":"mght", "title": "Мощность, кВт"},
    {"fmt":""   , "key":"isWork", "title": "Режим,"},
    {"fmt":".2f", "key":"p_out_res", "title": "Давл. вых.(расч), МПа"},
    {"fmt":".2f", "key":"comp_degree", "title":"Ст. сжатия, д. ед."},
    {"fmt":".0f", "key":"w_cnt", "title": "К-во раб. ГПА, шт"},
    {"fmt":".0f", "key":"gasoline_rate", "title":"Расход топлива, тыс м3/сут"},
    {"fmt":".0f", "key":"t_out", "title": "Темп. выхода, С"},
    {"fmt":".0f", "key":"percent_x", "title":"Помп. удал, д. ед"},
    {"fmt":".0f", "key":"volume_rate", "title":"Об. расход, м3/мин"},
    {"fmt":".2f", "key":"kpd", "title":"Пол. кпд, д. ед"},
    {"fmt":".2f", "key":"freq_dim", "title":"От. частота, д. ед"},
]

def get_dic_HEADERS_LIST(header:str):
    return next(filter(lambda dic: header in dic.values(), HEADERS_LIST))

def header_titles_from_list(headers:Iterable[str])->Iterable[Iterable[str]]:
    return zip(*[
        get_dic_HEADERS_LIST(head)['title'].split(',')
    for head in headers])

def get_format_by_key(key:str)->str:
    return next(filter(lambda dic: dic['key']==key, HEADERS_LIST))['fmt']

class Header:
    def __init__(self, header_titles:Iterable[str]):
        self._header, self._dimen = header_titles_from_list(header_titles)
        self._max_len = [len(item) for item in self._header]
        self._data:Iterable[Iterable[str]] = []

    def add_data(self, data_line:Iterable[str]):
        self._max_len = [
            len(str(value)) if self._max_len[ind] < len(str(value)) else self._max_len[ind]
        for ind, value in enumerate(data_line)]
        self._data.append(data_line)
    def __repr__(self):
        self._line_split = '|'.join([f'{"":{"="}^{val}}' for ind, val in enumerate(self._max_len)])
        self._line1 = '|'.join([f'{val:^{self._max_len[ind]+1}}'
            for ind, val in enumerate(self._header)])
        self._line2 = '|'.join([f'{val:^{self._max_len[ind]+1}}'
            for ind, val in enumerate(self._dimen)])
        return f'\n'.join([
            '\n'.join([
                "",
                self._line1,
                self._line2
            ]),
            *[
                "|".join([
                    f"{item:^{self._max_len[ind]+1}}"
                for ind, item in enumerate(line)])
            for line in self._data]
        ])

class BaseCollection(Header):
    def __init__(self, items:Union[NamedTuple, Iterable[NamedTuple]]):
        self._idx = 0
        self._list_items:List[NamedTuple] = []
        if isinstance(items, Iterable):
            super().__init__(items[0]._fields)
            self._list_items = list(items)
            for item in items:
                self.add_data([
                    f'{item._asdict()[key]:{get_format_by_key(key)}}'
                for key in item._asdict().keys()])
        elif isinstance(items, NamedTuple):
            super().__init__(items._fields)
            self.add_data([
                f'{items._asdict()[key]:{get_format_by_key(key)}}'
            for key in items._asdict().keys()])
            self._list_items = [items]
        else:
            assert False, "sad"
    def __iter__(self):
        return self
    def __next__(self)->NamedTuple:
        try:
            item = self._list_items[self._idx]
        except IndexError as idx_err:
            raise StopIteration() from idx_err
        self._idx +=1
        return item
