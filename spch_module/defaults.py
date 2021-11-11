BORDER_LIST = [
    {'key':'freq_dim', 'weight':9000., 'max_val':1.1, 'min_val':.7},
    {'key':'mght', 'weight':9000, 'max_val':16000, 'min_val':7000},
    {'key':'percent_x', 'weight':9000., 'max_val':100, 'min_val':0},
]

c00_fuel = []

DEFAULT_LIMITS = [
    {'key':'t_in', 'title':'Температура входа, К', 'value':308},
    {'key':'t_avo', 'title':'Температура после АВО, К', 'value':293},
    {'key':'R', 'title':'Газовая постоянная R, Дж/кг К', 'value':500.8},
    {'key':'k', 'title':'Коеффицинет политропы, д. ед', 'value':1.31},
    {'key':'plot', 'title':'Стандартная плотность, кг/м3', 'value':.692},
]

HEADERS_LIST = [
    {"dim":2, "key":"q", "title":"Комер. расх., млн. м3/сут"},
    {"dim":0, "key":"t_in", "title":"Темп. входа, К"},
    {"dim":2, "key":"p_in_req", "title": "Давл. вх(треб), МПа"},
    {"dim":2, "key":"p_out_req", "title": "Давл. вых(треб), МПа"},
    {"dim":2, "key":"p_in", "title": "Давл. вх, МПа"},
    {"dim":2, "key":"p_out", "title": "Давл. вых, МПа"},
    {"dim":0, "key":"type_spch", "title": "Тип СПЧ,"},
    {"dim":0, "key":"freq", "title": "Частота, об/мин"},
    {"dim":0, "key":"mght", "title": "Мощность, кВт"},
    {"dim":0, "key":"isWork", "title": "Режим,"},
    {"dim":2, "key":"p_out_res", "title": "Давл. вых.(расч), МПа"},
    {"dim":2, "key":"comp_degree", "title":"Степень сжатия, д. ед."},
    {"dim":0, "key":"w_cnt", "title": "Кол-ов рабочих ГПА, шт"},
    {"dim":0, "key":"gasoline_rate", "title":"Расход топлива, тыс м3/сут"},
    {"dim":0, "key":"t_out", "title": "Темп. выхода, С"},
    {"dim":0, "key":"percent_x", "title":"Помп. удал, д. ед"},
    {"dim":0, "key":"volume_rate", "title":"Об. расход, м3/мин"},    
    {"dim":2, "key":"kpd", "title":"Пол. кпд, д. ед"},    
    {"dim":2, "key":"freq_dim", "title":"От. частота, д. ед"},    
]

def get_dic_HEADERS_LIST(header:str):
    return next(filter(lambda x: header in x.values(), HEADERS_LIST))

from typing import Iterable
class Header:
    def __init__(self, header_titles:Iterable[str], dimens_titles:Iterable[str]):
        self._header = header_titles
        self._dimen = dimens_titles
        self._max_len = [len(item) for item in self._header]
        self._data:Iterable[Iterable[str]] = []
        self._line_split = '|'.join([f'{"":{"="}^{val}}' for ind, val in enumerate(self._max_len)])
    
    def add_data(self, data_line:Iterable[str]):
        self._max_len = [
            len(str(value)) if self._max_len[ind] < len(str(value)) else self._max_len[ind]
        for ind, value in enumerate(data_line)]
        self._data.append(data_line)
    def __repr__(self):
        self._line1 = '|'.join([f'{val:^{self._max_len[ind]+1}}' for ind, val in enumerate(self._header)])
        self._line2 = '|'.join([f'{val:^{self._max_len[ind]+1}}' for ind, val in enumerate(self._dimen)])
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
        



    


    
    
