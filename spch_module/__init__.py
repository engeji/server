"""Пакет для моделирования ДКС
"""
import math
import os
import sys
from collections import namedtuple
from itertools import groupby
from types import SimpleNamespace
from typing import List, Union, Iterable

import numpy as np
import xlrd

from .spch import Spch
from .modes import Comp, Stage
from .limit import Limit, DEFAULT_LIMIT

PATH_BASE = r'spch_module\base'
PATH_BASE_FILES = PATH_BASE + r'\text_files'
wb = xlrd.open_workbook(PATH_BASE + r'\dbqp.xls')
all_data = [{'name':lis, 'lis': wb.sheet_by_name(lis)} for lis in wb.sheet_names()]
ALL_SPCH_LIST:List[Spch] = list(filter(lambda x : float(x.mgth) == 16.0, [
    Spch(item['lis'])
for item in all_data]))

for f in os.listdir(PATH_BASE_FILES):
    with open(f'{PATH_BASE_FILES}\\{f}', 'r') as my_file:
        lines = my_file.read()
    ALL_SPCH_LIST.append(Spch(None, lines, '.'.join(f.split('.')[:-1])))

def GET_SPCH_BY_NAME(name:str)->Spch:
    return next(filter(lambda sp: sp.name == name, ALL_SPCH_LIST))

def GET_COMP_BY_NAME(
    names:Union[str, Iterable[str]],
    w_cnt:Union[int, Iterable[int]],
    lim:Limit=DEFAULT_LIMIT
    )->Comp:
    if isinstance(names, Iterable):
        assert isinstance(w_cnt, Iterable)
        stages = [
            Stage(GET_SPCH_BY_NAME(name), w_cnt[idx])
        for idx, name in enumerate(names)]
    else:
        assert isinstance(w_cnt, int)
        stsages = Stage(GET_SPCH_BY_NAME(names), w_cnt)
    return Comp(lim, stages)
