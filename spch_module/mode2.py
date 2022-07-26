from .discript import Base_header
from typing import List

# class _mode:pass
@Base_header('q_in p_input t_in')
class _Mode2:...
class Mode2(_Mode2):
    """
    >>> Mode2()
    <BLANKLINE>
    Комер. расх.|Давл. (треб)|Т.вх
     млн. м3/сут|     МПа    |  К 
       20.00    |    2.00    |285 
    <BLANKLINE>
    >>> Mode2(1, 99,999)
    <BLANKLINE>
    Комер. расх.|Давл. (треб)|Т.вх
     млн. м3/сут|     МПа    |  К 
        1.00    |   99.00    |999 
    <BLANKLINE>
    >>> Mode2([20,25], 5, 293)
    <BLANKLINE>
    Комер. расх.|Давл. (треб)|Т.вх
     млн. м3/сут|     МПа    |  К 
    20.00+25.00 |    5.00    |293 
    <BLANKLINE>
    >>> Mode2(20, 5, 293) + Mode2(25, 5, 293)
    <BLANKLINE>
    Комер. расх.|Давл. (треб)|Т.вх
     млн. м3/сут|     МПа    |  К 
    20.00+25.00 |    5.00    |293 
    <BLANKLINE>
    """
    def __init__(self ,q_in:float=None, p_input:float=None, t_in:float=None):
        self.q_in = q_in
        self.p_input = p_input
        self.t_in = t_in