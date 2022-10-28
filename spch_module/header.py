""" Модуль классов дискриптеров
"""
from typing import Iterable, Dict,Tuple, List, Union, TypeVar
import enum

import numpy as np
class Header_list(enum.Enum):
    type_spch = {"title":"Тип СПЧ","fmt":""}
    q_in = {"title":"Комер. расх., млн. м3/сут","fmt":".2f", "default":20}
    t_in = {"title":"Т.вх, К","fmt":".0f", "default":285.}
    p_input = {"title": "Давл. (треб), МПа","fmt":".2f", "default":2.}
    p_out_req = {"title": "Давл. вых(треб), МПа","fmt":".2f", "default":0}
    p_in = {"title": "Давл. вх, МПа","fmt":".2f", "default":0}
    p_out = {"title": "Давл. вых, МПа","fmt":".2f", "default":0}
    freq = {"title": "Частота, об/мин","fmt":".0f", "default":5200}
    freq_dim = {"title": "Частота, д.ед","fmt":".0f", "default":0}
    mght = {"title": "Мощность, кВт","fmt":".0f", "default":0}
    isWork = {"title": "Режим,","fmt":"" , "default":""}
    p_out_res = {"title": "Давл. вых.(расч), МПа","fmt":".2f", "default":0}
    comp_degree = {"title":"Ст. сжатия, д. ед.","fmt":".2f", "default":0}
    w_cnt = {"title": "ГПА(макс. раб), шт","fmt":".0f", "default":1}
    w_cnt_current = {"title": "ГПА(тек. раб), шт","fmt":".0f", "default":1}
    gasoline_rate = {"title":"Расход топлива, тыс м3/сут","fmt":".0f", "default":0}
    t_out = {"title": "Т.вых, С","fmt":".0f", "default":0}
    percent_x = {"title":"Помп. удал, д. ед","fmt":".0f", "default":0}
    volume_rate = {"title":"Об. расход, м3/мин","fmt":".0f", "default":0}
    kpd  = {"title":"Пол. кпд, д. ед","fmt":".2f", "default":0}
    max_val = {"title":"Максимум,","fmt":".2f", "default":0}
    min_val = {"title":"Минимум,","fmt":".2f", "default":0}
    weight = {"title":"Вес,","fmt":".0f", "default":0}
    param = {"title":"param", "fmt":"", "default":""}
    dp_avo =  {'title':'Потери АВО, МПа', 'fmt':'.2f', 'default':.06}
    t_avo =  {'title':'Т.АВО, К', 'fmt':'.0f', 'default':282.}
    r_val =  {'title':'R, Дж/кг К', 'fmt':'.1f', 'default':512}
    k_val =  {'title':'Коефф. пол., д. ед', 'fmt':'.2f', 'default':1.31}
    plot_std =  {'title':'Ст. плот., кг/м3', 'fmt':'.3f', 'default':.698}

class Header:
    def __repr__(self):
        if hasattr(self, '_keys'):
            keys = self._keys
        else:
            keys = self.__dict__.keys()
        titles = zip(*[
            Header_list[key].value['title'].split(',')
        for key in filter(lambda x: x[0] != '_', keys)])        

        
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
 
    def _data(self)->List[List[str]]:
        keys = self._keys
        fmts, values_list = zip(*[
            (Header_list[key].value['fmt'], getattr(self, key))
        for key in keys])
        return [[
            '+'.join(map(lambda x: format(x, fmts[idx]), values))
        for idx, values in enumerate(values_list)]]