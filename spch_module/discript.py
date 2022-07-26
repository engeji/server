""" Модуль классов дискриптеров
"""
from multiprocessing.context import assert_spawning
from typing import Iterable, Dict,Tuple, List, Union, TypeVar
import enum
from . __init__ import ALL_SPCH_LIST
import numpy as np
class Header_list(enum.Enum):
    q_in = {"title":"Комер. расх., млн. м3/сут","fmt":".2f", "default":20}
    t_in = {"title":"Т.вх, К","fmt":".0f", "default":285.}
    p_input = {"title": "Давл. (треб), МПа","fmt":".2f", "default":2.}
    p_out_req = {"title": "Давл. вых(треб), МПа","fmt":".2f", "default":0}
    p_in = {"title": "Давл. вх, МПа","fmt":".2f", "default":0}
    p_out = {"title": "Давл. вых, МПа","fmt":".2f", "default":0}
    type_spch = {"title": "Тип СПЧ,","fmt":"", "default": ALL_SPCH_LIST[37]}
    freq = {"title": "Частота, об/мин","fmt":".0f", "default":0}
    freq_dim = {"title": "Частота, д.ед","fmt":".0f", "default":0}
    mght = {"title": "Мощность, кВт","fmt":".0f", "default":0}
    isWork = {"title": "Режим,","fmt":"" , "default":""}
    p_out_res = {"title": "Давл. вых.(расч), МПа","fmt":".2f", "default":0}
    comp_degree = {"title":"Ст. сжатия, д. ед.","fmt":".2f", "default":0}
    w_cnt = {"title": "ГПА, шт","fmt":".0f", "default":1}
    gasoline_rate = {"title":"Расход топлива, тыс м3/сут","fmt":".0f", "default":0}
    t_out = {"title": "Т.вых, С","fmt":".0f", "default":0}
    percent_x = {"title":"Помп. удал, д. ед","fmt":".0f", "default":0}
    volume_rate = {"title":"Об. расход, м3/мин","fmt":".0f", "default":0}
    kpd  = {"title":"Пол. кпд, д. ед","fmt":".2f", "default":0}
    max_val = {"title":"Максимум,","fmt":".2f", "default":0}
    min_val = {"title":"Минимум,","fmt":".2f", "default":0}
    weight = {"title":"Вес,","fmt":".0f", "default":0}
    mode = {"title":"Комер. расх., млн. м3/сут","fmt":".2f", "default":0}
    param = {"title":"param", "fmt":"", "default":""}
    dp_avo =  {'title':'Потери АВО, МПа', 'fmt':'.2f', 'default':0.06}
    t_avo =  {'title':'Т.АВО, К', 'fmt':'.0f', 'default':293.}
    r_val =  {'title':'R, Дж/кг К', 'fmt':'.1f', 'default':500.8}
    k_val =  {'title':'Коефф. пол., д. ед', 'fmt':'.3f', 'default':1.31}
    plot_std =  {'title':'Ст. плот., кг/м3', 'fmt':'.3f', 'default':0.698}

_T = TypeVar('_T')
class BaseData(list):
    dic_func = {
        'add': lambda x,y: x+y,
        'radd': lambda x,y: y+x,
        'mul': lambda x,y: x*y, 
        'rmul': lambda x,y: y*x, 
        'div': lambda x,y: x/y, 
        'rdiv': lambda x,y: y/x, 
        'pow': lambda x,y: x**y, 
        'rpow': lambda x,y: y**x, 
    }
    def __repr__(self) -> str:
        return 'base '+ super().__repr__()
    def func(self, other, key):
        if isinstance(other, (list,BaseData,np.ndarray)):
            return BaseData([
                self.dic_func[key](a,b)
            for a,b in zip(self, other)])
        elif isinstance(other, (int,float,np.float64) ):
            return BaseData([
                 self.dic_func[key](x,other)
            for x in self])
    def __getitem__(self, idx):
        try:
            return super().__getitem__(idx)
        except IndexError:
            return super().__getitem__(0)
    def __add__(self, other: List[_T]) -> List[_T]:return self.func(other, 'add')
    def __radd__(self, other: List[_T]) -> List[_T]:return self.func(other, 'radd')
    def __sub__(self, other: List[_T]) -> List[_T]:return self + (-other)
    def __rsub__(self, other: List[_T]) -> List[_T]:return other + ( -self)
    def __neg__(self) -> List[_T]:return BaseData([-val for val in self])
    def __mul__(self, other: List[_T]) -> List[_T]:return self.func(other, 'mul')
    def __rmul__(self, other: List[_T]) -> List[_T]:return self.func(other, 'rmul')
    def __truediv__(self, other: List[_T]) -> List[_T]:return self.func(other, 'div')
    def __rtruediv__(self, other: List[_T]) -> List[_T]:return self.func(other, 'rdiv')
    def __pow__(self, other: List[_T]) -> List[_T]:return self.func(other, 'pow')
    def __rpow__(self, other: List[_T]) -> List[_T]:return self.func(other, 'rpow')
class BaseStruct:
    def __set__(self,obj,value):
        if not hasattr(obj, '_row_cnt'):
            setattr(obj, '_row_cnt', 1)
        if isinstance(value, list):
            cur_cnt = getattr(obj, '_row_cnt')
            setattr(obj, '_row_cnt', max(cur_cnt, len(value)) )
            # assert cur_cnt == len(value), f'{value=} {cur_cnt=} {max(cur_cnt, len(value))}'
        if value is None:
            val =  Header_list[self.key[1:]].value['default']
            # setattr(obj, self.key, BaseData(
            #     val if isinstance(val, list) else [val]
            # ))
            setattr(obj, self.key, BaseData([val]))
        else:
            setattr(obj, self.key, BaseData(
                value if isinstance(value, list) else [value]
            ))
    def __get__(self,obj,cls):
        if not hasattr(obj, self.key):
            self.__set__(obj, None)
            # setattr(obj, self.key, BaseData())
        value = getattr(obj, self.key)
        return value
    def __set_name__(self, cls, key):
        self.key = f'_{key}'
        self.cls = cls
    
def Base_header(keys:Union[List[str], str])->int:
    if type(keys) == str:
        keys = keys.split()
    def wraper(cls):
        fmts = [Header_list[key].value['fmt'] for key in keys]
        def __repr__(self):
            titles = zip(*[
                Header_list[key].value['title'].split(',')
            for key in keys])

            lines = [*titles, *self._data()]
            lenth = [
                len(max(col, key=len))
            for col in zip(*lines)]
            res =  '\n' + '\n'.join([
                '|'.join([
                    f'{word:^{lenth}}'
                for word, lenth in zip(line_words, lenth)])
            for line_words in lines]) + '\n'
            return res
        # def _data(self) -> List[List[str]]:
        #     return [
        #         [
        #             f"{getattr(self,f'_{key}')[idx]:{fmt}}"
        #         for key, fmt in zip(self.params, self.fmts)]
        #     for idx in range(self._row_cnt)]
        def _data(self) -> List[List[str]]:
            return [[
                '+'.join([
                    f'{value:{fmt}}'
                for value in getattr(self, f'_{key}')])
            for fmt, key in zip(self.fmts, self.params)]]
        def __add__(self, other):
            res = self.clone()
            setattr(res, '_row_cnt', getattr(self, '_row_cnt') + 1)
            for key in self.params:
                curr_val = getattr(res, f'_{key}')
                new_val = getattr(other, f'_{key}')
                if not len(set([*curr_val, *new_val])) == 1:
                    curr_val.extend(new_val)
            return res
        def __iadd__(self, other):
            # assert False, f'{self}, {other}'
            return self + other
            
        def clone(self):
            new_obj = self.__class__()
            for key in keys:
                val = getattr(self, f'{key}')
                setattr(new_obj, f'{key}', val)
            return new_obj
            
        # def __new__(_cls, *args, **kwargs):
        #     return _cls(*args, **kwargs)
        # dct = {'__new__': __new__}
        
        dct = {'__repr__': __repr__}
        if not hasattr(cls, '_data'):
            dct['_data'] = _data
        if not hasattr(cls, '__add__'):
            dct['__add__'] = __add__
        if not hasattr(cls, '__iadd__'):
            dct['__iadd__'] = __iadd__
        def __getitem__(self, index):
            new_obj = self.__class__()
            for key in keys:
                val = getattr(self, f'{key}')
                if index < len(val):
                    setattr(new_obj, f'{key}', val[index])
                else:
                    setattr(new_obj, f'{key}', val[-1])
            return new_obj
                

        def __iter__(self):
            self._ind = 0
            return self
        def __next__(self):
            if self._ind < self._row_cnt:
                self._ind += 1
                return self[self._ind]
            raise StopIteration

        dct['__iter__'] = __iter__            
        dct['__next__'] = __next__                    
        dct['__getitem__'] = __getitem__
        dct['__len__'] = lambda self: len(getattr(self, keys[0]))
        dct['clone'] = clone
        dct['fmts'] = fmts
        dct['params'] = keys
        dct['__name__'] = cls.__name__
        dct['__doc__'] = cls.__doc__
        dct['__annotations__'] = {}

        for key in keys:
            dct['__annotations__'][key] = float
            dct[key] = BaseStruct()
        return type(cls.__name__, (cls,), dct)
    return wraper