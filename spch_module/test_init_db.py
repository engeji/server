"""Модуль тестирования инициализации
"""
# import pytest
from . import ALL_SPCH_LIST

def test_has_file_db():
    """[summary]
    """
    assert isinstance(ALL_SPCH_LIST, list)
