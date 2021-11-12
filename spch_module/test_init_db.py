"""
    Модуль тестирования инициализации
"""
# import pytest
from . import ALL_SPCH_LIST

def test_has_file_db():
    """[summary]
    """
    base_xl = r'base\db.xls'
    assert isinstance(ALL_SPCH_LIST, list)
