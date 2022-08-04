"""Пакет для моделирования ДКС
"""
from .facilities import get_all_spch
from .spch import Spch

PATH_BASE = r'spch_module\base'
PATH_BASE_FILES = PATH_BASE + r'\text_files'
ALL_SPCH_LIST = get_all_spch()

def get_spch_by_name(title:str)->Spch: return next(filter(lambda x: x.name == title, ALL_SPCH_LIST ))
    

