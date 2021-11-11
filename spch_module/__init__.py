import xlrd
import math
from typing import List
from types import SimpleNamespace
from itertools import groupby
import numpy as np
from collections import namedtuple
from .spch import Spch
import os
import sys

#server\spch_module\base\dbqp.xls
path_base = r'server\spch_module\base'
path_base_files = path_base + r'\text_files'
wb = xlrd.open_workbook(path_base + r'\dbqp.xls')
all_data = [{'name':lis, 'lis': wb.sheet_by_name(lis)} for lis in wb.sheet_names()]
ALL_SPCH_LIST:List[Spch] = list(filter(lambda x : float(x.mgth) == 16.0, [Spch(item['lis']) for item in all_data]))

for f in os.listdir(path_base_files):
    with open(f'{path_base_files}\\{f}', 'r') as my_file:
        lines = my_file.read() 
    ALL_SPCH_LIST.append(Spch(None, lines, '.'.join(f.split('.')[:-1])))

GROUPED_SPCH_LIST = [
    ("{0:.0f}".format(key), list([SimpleNamespace(name=v.name, title=str(v), fnom=v.fnom)
        for v in sorted(val, key=lambda x:x.stepen)]))
            for key, val in groupby(sorted(ALL_SPCH_LIST, key=lambda x:x.ptitle), key=lambda x:x.ptitle)]



LENGTH = [
    10,9,11,9,9,9,9,3,7,5,5,7
]

