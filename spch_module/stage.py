from typing import Iterable, List, Tuple, Union

from .facilities import get_spch_by_name
from .formulas import calc_t_out, dh, my_z, ob_raskh
from .limit import Limit
from .summary import Summary
class _Stage:
    def __init__(self, spch_name:str=None, lim:Limit=None, w_cnt:int=None):
        self.type_spch = get_spch_by_name(spch_name)
        self._lim = lim
        self.w_cnt = w_cnt
    @property
    def k_val(self)->float: return self._lim.k_val
    @property
    def r_val(self)->float: return self._lim.r_val
    @property
    def plot_std(self)->float: return self._lim.plot_std
    @property
    def t_avo(self)->float: return self._lim.t_avo
    @property
    def dp_avo(self)->float: return self._lim.dp_avo
    def calc_xy_percent_kpd(self, q_one:float, p_in:float, t_in:float, freq:float)-> Tuple[float, float, float, float]:
        koef_raskh = self.type_spch.koef_raskh(
            q_in=q_one, p_in=p_in, freq=freq, t_in=t_in,
            r_val=self.r_val, plot_std=self.plot_std)
        z_in = my_z(p_in, t_in)
        kpd = self.type_spch.calc_k_kpd(koef_raskh)
        volume_rate, comp_degree = self.type_spch.calc_xy(
            freq=freq, k_raskh=koef_raskh, z_val=z_in, r_val=self.r_val,
            t_in=t_in, k_val=self.k_val)
        percent_x = self.type_spch.percent_x_by_k_raskh(koef_raskh)
        return volume_rate, comp_degree, percent_x, kpd
    def get_freq_min_max(self, q_in:float, p_in:float, t_in:float, w_current:int)->Tuple[Summary,Summary]:
        volume_rate = ob_raskh(q_in/w_current, p_in, t_in, self.r_val, self.plot_std)
        freqs = self.type_spch.get_freq_bound(volume_rate)
        return tuple(Summary(self, q_in, p_in, t_in, freq, w_current) for freq in freqs)