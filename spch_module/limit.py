"""Модуль для класса Limit - свойсва флюида и ограничения расчета
"""
from collections import namedtuple

DEFAULT_LIMITS = [
    {'key':'t_in', 'title':'Температура входа, К', 'value':285},
    {'key':'dp_avo', 'title':'Потери АВО, МПа', 'value':0.06},
    {'key':'t_avo', 'title':'Температура после АВО, К', 'value':293},
    {'key':'r_val', 'title':'Газовая постоянная R, Дж/кг К', 'value':500.8},
    {'key':'k_val', 'title':'Коеффицинет политропы, д. ед', 'value':1.31},
    {'key':'plot_std', 'title':'Стандартная плотность, кг/м3', 'value':.692},
]
def GET_DEFAULT_LIMIT(key:str)->float:
    return next(filter(lambda dic: dic['key'] == key, DEFAULT_LIMITS))['value']
LIST_LIMIT = 'r_val k_val plot_std t_avo dp_avo'



class Limit(namedtuple('Limit', LIST_LIMIT)):
    """Класс граничных условий

    Args:
        r_val (float): R постоянная 
        k_val (float): K постоянная 
        plot_std (float): стандартная плотность  
        t_avo (float): температура после АВО  
        dp_avo (float): потери на АОВ  
    """    
    def get_t_out(self, comp_degree:float, t_in:float, kpd:float)->float:
        return t_in * (comp_degree ** (self.k_val - 1 ) / (self.k_val * kpd))-273.15
"""Класс параметров свойств флюида
"""
DEFAULT_LIMIT = Limit(**{
    key:GET_DEFAULT_LIMIT(key)
for key in LIST_LIMIT.split()})
