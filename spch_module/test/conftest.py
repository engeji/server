import pytest
import pandas as pd
from typing import List, Tuple

from ..limit import Limit
from ..comp import Comp
from ..mode import Mode

@pytest.fixture()
def test_modes()->List[Tuple[Mode,Comp, pd.Series]]:
    df = pd.read_excel('./spch_module/test/test_2step.xlsx', sheet_name='Лист2')
    return [
        (
            Mode(r['Q'], r['Рвх'],r['T']),
            Comp([r['СПЧ1'],r['СПЧ2']],
                 [r['w_cnt1'],r['w_cnt2']],
                    Limit(r_val=r['R'])),
            r)
    for _, r in df.iterrows()]

