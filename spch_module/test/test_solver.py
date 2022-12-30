from .. comp import Comp
from ..mode import Mode
from ..summary import Summary
from ..solver import Solver
import pytest

@pytest.mark.parametrize('mode, comp',[
    # (Mode(), Comp('ГПА-ц3-16С-45-1.7(ККМ)', 2)),
    (Mode(), Comp(['ГПА-ц3-16С-45-1.7(ККМ)', 'ГПА Ц3 16с76-1.7М'], [1,2])),
])
def test_solver_func(mode:Mode, comp:Comp,):
    s = Solver(comp, mode)
    # print(f'freqs is {s.freq_x_for_plot}')
    # print(s.border_summs)
    # print(f'freqs y is {s.freq_y_for_plot1}')
    # print(f'freqs y is {s.freq_y_for_plot2}')



@pytest.mark.parametrize('a, res',[
    (1,1),
    (2,4),
    (-1,1),
    (3,6),
])
def test_vsevolod(a,res):
    assert a**2 == res
