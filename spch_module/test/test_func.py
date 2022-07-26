from kiwisolver import Solver
from .. mode2 import Mode2
from .. comp2 import Comp2
from .. solver import Solver
from .. facilities import get_comp_by_name
from ..discript import BaseData
import pytest
@pytest.mark.parametrize('comp, mode', [
    (Comp2(['ГПА-ц3-16С-45-1.7(ККМ)', 'ГПА Ц3 16с76-1.7М'], [1,2]), Mode2()),
])
def test_func_all(comp:Comp2, mode:Mode2):
    res = comp.calc_via_p_in(mode, [5200]*2)
    print(res)
    print(comp._get_freq_min_max_one_stage(0,mode))
    print(comp._get_freq_min_max_one_stage(1,Mode2(mode.q_in, res.p_out[0], comp.t_avo)))
    print(comp.w_cnt)
    # print(comp.get_freq_bound_min_max(mode, [5200,5200]))
    
@pytest.mark.parametrize('comp, mode', [
    (Comp2(), Mode2()),
])
def test_func_solverl(comp:Comp2, mode:Mode2):
    sol = Solver(comp, mode, 80)
    print(sol)