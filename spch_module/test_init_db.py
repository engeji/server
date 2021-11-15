"""Модуль тестирования инициализации
"""
from . import ALL_SPCH_LIST


def test_init_db():
    """[summary]
    """
    print(*ALL_SPCH_LIST, sep='\n')
    assert isinstance(ALL_SPCH_LIST, list)
    