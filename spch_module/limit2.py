"""Модуль для класса Limit - свойсва флюида и ограничения расчета
"""
from .discript import Base_header
from typing import List
@Base_header('r_val k_val t_avo dp_avo plot_std')
class _Limit:pass
class Limit2(_Limit):
    """
    >>> Limit2()
    <BLANKLINE>
       R    |Коефф. пол.|Т.АВО|Потери АВО|Ст. плот.
     Дж/кг К|   д. ед   |  К  |    МПа   |  кг/м3  
     500.8  |   1.31    | 293 |   0.06   |  0.698  
    <BLANKLINE>
    >>> Limit2(300)
    <BLANKLINE>
       R    |Коефф. пол.|Т.АВО|Потери АВО|Ст. плот.
     Дж/кг К|   д. ед   |  К  |    МПа   |  кг/м3  
     300.0  |   1.31    | 293 |   0.06   |  0.698  
    <BLANKLINE>
    >>> Limit2([1,2])
    <BLANKLINE>
       R    |Коефф. пол.|Т.АВО|Потери АВО|Ст. плот.
     Дж/кг К|   д. ед   |  К  |    МПа   |  кг/м3  
    1.0+2.0 |   1.31    | 293 |   0.06   |  0.698  
    <BLANKLINE>

    Класс граничных условий
    Args:
        r_val (float): R постоянная 
        k_val (float): K постоянная 
        plot_std (float): стандартная плотность  
        t_avo (float): температура после АВО  
        dp_avo (float): потери на АВО  
    """    
    def __init__(self, r_val:float=None, k_val:float=None, t_avo:float=None, dp_avo:float=None, plot_std:float=None):
        self.r_val = r_val
        self.k_val = k_val
        self.t_avo = t_avo
        self.dp_avo = dp_avo
        self.plot_std = plot_std

    