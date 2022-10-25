from .. comp import Comp
from ..mode import Mode
from ..summary import Summary
import pytest
# @pytest.mark.parametrize('func, array, param_name', [
#     ('get_perc_by_mght', np.linspace(2000,20000,10), 'mght'),
#     ('get_mght_by_perc', np.linspace(2,20,10), 'percent_x'),
#     ('get_perc_by_comp', np.linspace(1,2,10), 'comp_degree'),
# ])
# def test_mght_and_perc(func, array, param_name):
# @pytest.mark.parametrize('mode, comp',[
#     (Mode(), Comp('ГПА-ц3-16С-45-1.7(ККМ)', 2)),
#     (Mode(30,None,None), Comp(['ГПА-ц3-16С-45-1.7(ККМ)', 'ГПА Ц3 16с76-1.7М'], [1,2])),
# ])
def test_calcs(test_modes):
    print(test_modes)
    

@pytest.mark.parametrize('mode, comp, freqs',[
    (Mode(), Comp('ГПА-ц3-16С-45-1.7(ККМ)', 2), [5200]),
    (Mode(), Comp(['ГПА-ц3-16С-45-1.7(ККМ)', 'ГПА Ц3 16с76-1.7М'], [1,2]), [5200,5200]),
])
def test_border(mode:Mode, comp:Comp, freqs:float):
    s_100, s_0 = comp.get_freq_bound_max_min(mode, freqs)
    print(s_0)
    print(s_100)
    for idx in range(len(comp)):
        assert abs(s_100.percent_x[idx] - 100) < .0001, f'Ошибка границы {s_100}'
        assert abs(s_0.percent_x[idx] - 0) < .0001, f'Ошибка границы {s_0}'

