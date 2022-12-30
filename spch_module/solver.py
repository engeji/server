from typing import List, TYPE_CHECKING, Tuple

from .comp import Comp
from .mode import Mode
from .summary import Summary
import numpy as np
import matplotlib.pyplot as plt
# if TYPE_CHECKING:

class Solver:
    def __init__(self, comp:Comp, mode:Mode) -> None:
        self.comp = comp
        self.mode = mode
        self.min_1st, self.max_1st = self.comp[0].get_freq_bound_max_min(mode,[self.comp.type_spch[0].fnom])
        self.freq_x_for_plot = np.linspace( self.min_1st.freq[0], self.max_1st.freq[0], 10)  
        self.border_summs = [
            self.func_constr([freq,0])
        for freq in self.freq_x_for_plot]
        self.freq_y_for_plot1 = [
            self.func_constr([freq,0])[0].freq[1]
        for freq in self.freq_x_for_plot]

        self.freq_y_for_plot2 = [
            self.func_constr([freq,0])[1].freq[1]
        for freq in self.freq_x_for_plot]

        fix, ax = plt.subplots()
        ax.plot(self.freq_x_for_plot, self.freq_y_for_plot1)
        ax.plot(self.freq_x_for_plot, self.freq_y_for_plot2)
        plt.show()
        
    def func_constr(self,freq:List[float])->Tuple[Summary, Summary]:
        return self.comp.get_freq_bound_max_min(self.mode, freq)

    def objec_func(self, freq:List[float])->float: #TODO: целевая функция
        res = self.comp.calc_via_p_in(self.mode, freq)
        base_value = sum(res.mght)/ len(res) / (10**3)
