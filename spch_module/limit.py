"""Модуль для класса Limit - свойсва флюида и ограничения расчета
"""
from .header import Header_list
class Limit:
    """Класс граничных условий

    Args:
        r_val (float): R постоянная 
        k_val (float): K постоянная 
        plot_std (float): стандартная плотность  
        t_avo (float): температура после АВО  
        dp_avo (float): потери на АОВ  

    """    
    def __init__(self, r_val=None, k_val=None, plot_std=None, t_avo=None, dp_avo=None):
        self.r_val = Header_list.r_val.value['default']  if r_val == None else r_val
        self.k_val = Header_list.k_val.value['default']  if k_val == None else k_val
        self.plot_std = Header_list.plot_std.value['default']  if plot_std == None else plot_std
        self.t_avo = Header_list.t_avo.value['default']  if t_avo == None else t_avo
        self.dp_avo = Header_list.dp_avo.value['default']  if dp_avo == None else dp_avo
    def get_t_out(self, comp_degree:float, t_in:float, kpd:float)->float:
        return t_in * (comp_degree ** (self.k_val - 1 ) / (self.k_val * kpd))-273.15
