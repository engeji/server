import pytest
import pandas as pd
from typing import List, Tuple
from .. comp import Comp
from ..mode import Mode

@pytest.fixture()
def test_modes()->List[Tuple[Mode,Comp]]:
    df = pd.read_excel('./spch_module/test/test_2step.xlsx', sheet_name='Лист2')
    return [Mode(row['Q'], row['Рвх'], row['T']) for idn, row in df.iterrows()]

