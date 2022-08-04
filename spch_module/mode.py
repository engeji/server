from typing import List, Union
from .header import Header, Header_list
class Mode(Header):
    """
    >>> Mode()
    <BLANKLINE>
    Комер. расх.|Давл. (треб)|Т.вх
     млн. м3/сут|     МПа    |  К 
       20.00    |    2.00    |285 
    <BLANKLINE>
    >>> Mode(1, 99,999)
    <BLANKLINE>
    Комер. расх.|Давл. (треб)|Т.вх
     млн. м3/сут|     МПа    |  К 
        1.00    |   99.00    |999 
    <BLANKLINE>
    >>> Mode([20,25], 5, 293)
    <BLANKLINE>
    Комер. расх.|Давл. (треб)|Т.вх
     млн. м3/сут|     МПа    |  К 
    20.00+25.00 |    5.00    |293 
    <BLANKLINE>
    """
    class List_q_in(list):
        def __getitem__(self, index):        
            if isinstance(index, slice):
                return super().__getitem__(index)
            try:
                return super().__getitem__(index)
            except IndexError:
                return super().__getitem__(-1)
    def __init__(self, q_in:Union[List[float],float]=None, p_input:float=None, t_in:float=None):
        q_def:float = Header_list.q_in.value['default']
        if q_in == None:
            self.q_in = Mode.List_q_in([q_def])
        else:
            if isinstance(q_in, (float,int)):
                self.q_in =  Mode.List_q_in([q_in])
            else:
                self.q_in = Mode.List_q_in(q_in)
        self.p_input = p_input if p_input != None else Header_list.p_input.value['default']
        self.t_in = t_in if t_in != None else Header_list.t_in.value['default']
    def _data(self)->List[List[str]]:
        fmts, keys = zip(*[
            (Header_list[key].value['fmt'], key)
        for key in self.__dict__])

        # res = [] 
        # for idx_line in range(len(self.q_in)):
        one_list = []
        for key, fmt in zip(keys, fmts):
            attr = getattr(self, key)#[idx_line]
            if isinstance(attr, list):
                value = '+'.join(map(lambda x: format(x, fmt), attr))
            else:
                value = format(attr,fmt)
            one_list.append(value)
        # res.append(one_list)
        return [one_list]