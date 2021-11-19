"""Модуль тестирования инициализации
"""
import pytest
from . import ALL_SPCH_LIST
from .excel_res import ResultExcelTable

def test_init_db():
    """[summary]
    """
    print(*ALL_SPCH_LIST, sep='\n')
    assert isinstance(ALL_SPCH_LIST, list)

@pytest.fixture
def result_file():
    """[summary]
    """
    path_excel = './data_for_test/for_tst_2step.xlsx'
    res = ResultExcelTable(path_excel)
    return res

def test_read_excel(result_file, capsys):#pylint: disable=redefined-outer-name
    with capsys.disabled():
        print(result_file)
    assert True

def test_mode_collection(result_file, capsys):#pylint: disable=redefined-outer-name
    with capsys.disabled():
        print(result_file.get_mode_collection)
    assert True

def test_list_comp(result_file, capsys):#pylint: disable=redefined-outer-name
    with capsys.disabled():
        print(result_file.get_list_comp)
    assert True


def test_comp_summary_with_freqs_from_excel(result_file, capsys):#pylint: disable=redefined-outer-name
    with capsys.disabled():
        print(*result_file.get_list_comp_summary, sep='\n')
    assert True

def test_comp_summary_collections_with_freqs_from_excel(result_file, capsys):#pylint: disable=redefined-outer-name
    with capsys.disabled():
        print(result_file.get_CompSummaryCollection)
    assert True
