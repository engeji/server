"""[summary]
"""
from collections import namedtuple
from typing import List

import pandas
import pytest
from ..limit import GET_DEFAULT_LIMIT, DEFAULT_LIMIT
from ..mode import Mode
from ..modes import ModeCollection, Comp, Limit, Stage
from ..solver import Solver
from .. import GET_SPCH_BY_NAME, GET_COMP_BY_NAME

PATH_EXCEL = 'data_for_test\\for_tst_2step.xlsx'

f_excel = pandas.ExcelFile(PATH_EXCEL)
df: pandas.DataFrame = f_excel.parse(
    sheet_name=f_excel.sheet_names[0]
)
prove_cls = namedtuple('prove_tup', df.columns)

list_prove:List[prove_cls] = [
    prove_cls(**{
        column:row[1][column]
    for column in df.columns})
for row in df.iterrows()]

@pytest.fixture
def mode_coll()->ModeCollection:
    return ModeCollection([
        Mode(
            GET_DEFAULT_LIMIT("t_in"),
            prove.q_in,
            float(prove.p_in.split('+')[0])
        )
    for prove in list_prove])

@pytest.fixture
def list_comp()->List[Comp]:
    res = []
    for prove in list_prove:
        res.append(GET_COMP_BY_NAME(
            prove.type_spch.split('+'),
            [
                float(wcnt)
            for wcnt in prove.w_cnt.split('+')]))
    return res