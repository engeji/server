
import xlrd
from .spch import SpchInit, Spch
from typing import List
import os


def get_all_spch()->List[Spch]:
    PATH_BASE = r'spch_module\base'
    PATH_BASE_FILES = PATH_BASE + r'\text_files'
    wb = xlrd.open_workbook(PATH_BASE + r'\dbqp.xls')
    all_data = [{'name':lis, 'lis': wb.sheet_by_name(lis)} for lis in wb.sheet_names()]
    res = list(filter(lambda x : float(x.mgth) == 16.0, [
        Spch((SpchInit(item['lis'])))
    for item in all_data]))

    for f in os.listdir(PATH_BASE_FILES):
        with open(f'{PATH_BASE_FILES}\\{f}', 'r') as my_file:
            lines = my_file.read()
        res.append(Spch(SpchInit(None, lines, '.'.join(f.split('.')[:-1]))))
    return res