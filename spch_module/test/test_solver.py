from .conftest import list_comp, mode_coll
from ..solver import Solver

def test_shwplt(list_comp, mode_coll, capsys):
    solver = Solver(list_comp[0], mode_coll[0])
    # res = solver.optimize()
    with capsys.disabled():
        # print(res)
        pass
    solver.show_plt()
    assert True