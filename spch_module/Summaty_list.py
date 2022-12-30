from .header import Header
from typing import List
from .summary import Summary
class Summary_list(Header): #TODO: подумать над Summary_list
    def __init__(self, summ:List[Summary]) -> None:
        self._keys = 'type_spch freq mght p_in p_out comp_degree w_cnt_current t_out percent_x volume_rate'.split()
    def _data(self)->List[List[str]]:
        keys = self._keys
        fmts, values_list = zip(*[
            (Header_list[key].value['fmt'], getattr(self, key))
        for key in keys])
        return [[
            '+'.join(map(lambda x: format(x, fmts[idx]), values))
        for idx, values in enumerate(values_list)]]