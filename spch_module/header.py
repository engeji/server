           
from typing import Iterable
from defaults import HEADERS_LIST
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
        
def get_dic_HEADERS_LIST(header:str):
    return next(filter(lambda x: header in x.values(), HEADERS_LIST))




