
import xlrd
from .spch import SpchInit, Spch
from typing import List
import os
from .header import Header_list


def get_all_spch()->List[Spch]:
    PATH_BASE = r'spch_module\base'
    PATH_BASE_FILES = PATH_BASE + r'\text_files'
    wb = xlrd.open_workbook(PATH_BASE + r'\dbqp.xls')
    all_data = [{'name':lis, 'lis': wb.sheet_by_name(lis)} for lis in wb.sheet_names()]
    res = list(filter(lambda x : float(x.mgth) == 16.0, [
        Spch((SpchInit(Header_list.k_val.value['default'],Header_list.plot_std.value['default'],item['lis'])))
    for item in all_data]))

    for f in os.listdir(PATH_BASE_FILES):
        with open(f'{PATH_BASE_FILES}\\{f}', 'r') as my_file:
            lines = my_file.read()
        res.append(Spch(SpchInit(Header_list.k_val.value['default'],Header_list.plot_std.value['default'],None, lines, '.'.join(f.split('.')[:-1]))))
    return res
ALL_SPCH_LIST = get_all_spch()
PATH_BASE = r'spch_module\base'
PATH_BASE_FILES = PATH_BASE + r'\text_files'

def get_spch_by_name(title:str)->Spch: return next(filter(lambda x: x.name == title, ALL_SPCH_LIST))