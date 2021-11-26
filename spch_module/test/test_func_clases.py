from .conftest import mode_coll, list_comp
from ..mode import Mode
from ..modes import Comp, Stage
import numpy as np
def test_mode_col(mode_coll, capsys):
    with capsys.disabled():
        print(mode_coll)
    assert True

def test_list_comp(list_comp, capsys):
    with capsys.disabled():
        print(list_comp)
    assert True

def test_freq_bound(list_comp, mode_coll, capsys):
    idx = 10
    mode:Mode = mode_coll[idx]
    comp:Comp = list_comp[idx]
    stage_1:Stage = comp[0]
    freq_min, freq_max = stage_1.get_freq_max_min(mode, comp.lim)
    p_in_list = [
        mode.p_in * stage_1.calc_stage_summary_in(mode.q_in, mode.p_in,mode.t_in,comp.lim,freq).comp_degree - comp.lim.dp_avo
    for freq in np.linspace(freq_min, freq_max, 5)]
    with capsys.disabled():
        print('\n')
        print(*p_in_list, sep='\n')
