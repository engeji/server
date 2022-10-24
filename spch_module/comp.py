"""Модуль класса входных данных
"""
from typing import Iterable, List, Tuple, Union

from flask import g
from numpy import result_type

from . import get_spch_by_name
from .formulas import calc_t_out, dh, my_z, ob_raskh
from .header import Header, Header_list
from .limit import DEFAULT_LIMIT, Limit
from .mode import Mode
from .summary import Summary
from .spch import Spch
from .stage import _Stage

class Comp(Limit,Header):
    """Класс компановки ДКС

    >>> Comp('ГПА-ц3-16С-45-1.7(ККМ)', 1)
    <BLANKLINE>
     Тип СПЧ |ГПА(макс. раб)|ГПА(тек. раб)|   R    |Коефф. пол.|Ст. плот.|Т.АВО|Потери АВО
             |      шт      |      шт     | Дж/кг К|   д. ед   |  кг/м3  |  К  |    МПа   
    16/45-1.7|      1       |      1      | 500.8  |   1.31    |  0.692  | 293 |   0.06   
    <BLANKLINE>
    >>> comp2 = Comp(['ГПА-ц3-16С-45-1.7(ККМ)', 'ГПА Ц3 16с76-1.7М'], [1,2])
    >>> comp2
    <BLANKLINE>
     Тип СПЧ |ГПА(макс. раб)|ГПА(тек. раб)|   R    |Коефф. пол.|Ст. плот.|Т.АВО|Потери АВО
             |      шт      |      шт     | Дж/кг К|   д. ед   |  кг/м3  |  К  |    МПа   
    16/45-1.7|      1       |      1      | 500.8  |   1.31    |  0.692  | 293 |   0.06   
    16/76-1.7|      2       |      2      | 500.8  |   1.31    |  0.692  | 293 |   0.06   
    <BLANKLINE>
    >>> [stage for stage in comp2]
    [
     Тип СПЧ |ГПА(макс. раб)|ГПА(тек. раб)|   R    |Коефф. пол.|Ст. плот.|Т.АВО|Потери АВО
             |      шт      |      шт     | Дж/кг К|   д. ед   |  кг/м3  |  К  |    МПа   
    16/45-1.7|      1       |      1      | 500.8  |   1.31    |  0.692  | 293 |   0.06   
    , 
     Тип СПЧ |ГПА(макс. раб)|ГПА(тек. раб)|   R    |Коефф. пол.|Ст. плот.|Т.АВО|Потери АВО
             |      шт      |      шт     | Дж/кг К|   д. ед   |  кг/м3  |  К  |    МПа   
    16/76-1.7|      2       |      2      | 500.8  |   1.31    |  0.692  | 293 |   0.06   
    ]
    """
    # _w_cnt_current:int = [1]
    def __init__(self, spch_name:Union[str, List[str]], gpa_cnt_max:Union[int,List[int]], lim:Union[Limit, List[Limit]]=None) -> None:                
        self._keys = 'type_spch w_cnt w_cnt_current r_val k_val plot_std t_avo dp_avo'.split()
        self._fmts = [Header_list[key].value['fmt'] for key in self._keys]
        if isinstance(spch_name, str) and isinstance(gpa_cnt_max,int):  
            lim = DEFAULT_LIMIT if lim == None else lim         
            self._stages = [_Stage(spch_name, lim, gpa_cnt_max)]            
        elif isinstance(spch_name, list) and isinstance(gpa_cnt_max,list):
            assert len(spch_name) == len(gpa_cnt_max), 'Не верная размерность списков'
            lim = [DEFAULT_LIMIT] * len(gpa_cnt_max) if lim == None else [lim] * len(gpa_cnt_max)         
            self._stages = [_Stage(sp, lim[idx], gpa_cnt_max[idx]) for idx, sp in enumerate(spch_name)]
        else:
            raise TypeError(f'несоответствие типов аргументы инициализатора spch_name {spch_name} gpa_cnt_max{gpa_cnt_max}')        
        self.w_cnt_current = self.w_cnt
    @property
    def w_cnt(self)->List[int]: return [st.w_cnt for st in self._stages]
    @property
    def type_spch(self)->List[Spch]: return [st.type_spch for st in self._stages]
    @property
    def r_val(self)->List[float]: return [st.r_val for st in self._stages]
    @property
    def k_val(self)->List[float]: return [st.k_val for st in self._stages]
    @property
    def plot_std(self)->List[float]: return [st.plot_std for st in self._stages]
    @property
    def t_avo(self)->List[float]: return [st.t_avo for st in self._stages]
    @property
    def dp_avo(self)->List[float]: return [st.dp_avo for st in self._stages]
    def _data(self)->List[List[str]]:
        res = []
        for idx, st in enumerate(self._stages):
            one_stage = []
            for key, fmt in  zip(self._keys, self._fmts):
                one_stage.append(format(getattr(self, key )[idx], fmt))
            res.append(one_stage)
        return res
    def calc_via_p_in(self, mode:Mode, freq:List[float]) -> Summary:
        res = Summary(self._stages[0], mode.q_in[0], mode.p_input, mode.t_in, freq[0], self.w_cnt_current[0])
        for idx, stage in list(enumerate(self._stages))[1:]:
            res += Summary(
                stage, mode.q_in[idx], res.p_out[-1] - self.dp_avo[idx], 
                self.t_avo[idx], freq[idx], self.w_cnt_current[idx])
        return res

    def get_freq_bound_max_min(self, mode:Mode, all_freqs:List[float])->Tuple[Summary,Summary]:
        assert len(all_freqs) == len(self
            ),"(Количество элементов списка частот должно совпадать с количеством ступеней)"
        res = [self._stages[0].get_freq_min_max(mode.q_in[0], mode.p_input, mode.t_in, self.w_cnt_current[0])]
        p_in = mode.p_input
        t_in = mode.t_in
        for idx, stage in list(enumerate(self._stages))[1:]:
            prev_summ = Summary(self._stages[idx-1], mode.q_in[idx-1], p_in, t_in, all_freqs[idx-1], self.w_cnt_current[idx-1])
            p_in = prev_summ.p_out[0] - self.dp_avo[idx-1]
            t_in = self.t_avo[idx]
            res.append(stage.get_freq_min_max(mode.q_in[idx], p_in, t_in, self.w_cnt_current[idx]))
            # q_one = (mode.q_in[-1] if len(mode.q_in) != len(self) else mode.q_in[idx_stage]) / self.w_cnt_current[idx_stage]
            # prev_summ = self._calc_one_stage(q_one, p_in, t_in, idx_stage, all_freqs[idx_stage-1])
            # p_in = p_in * prev_summ.comp_degree[0] - self.dp_avo[idx_stage-1]
            # t_in = self.t_avo[idx_stage]
            # res.append(self._get_freq_min_max_one_stage(idx_stage,Mode(mode.q_in, p_in, t_in)))
        return tuple(Summary.sum(v) for v in zip(*res))
    def __len__(self)->int:return len(self.w_cnt)
    def __iter__(self)->Iterable['Comp']: return map(lambda x: Comp(x.type_spch.name, x.w_cnt, x._lim), self._stages)
    def __getitem__(self,idx)->'Comp':
        if isinstance(idx, slice):
            raise TypeError('иннах, слайсов нет пока')
        else:
            if idx <= (len(self) -1):
                return Comp(self._stages[idx].type_spch.name, self.w_cnt[idx], self._stages[idx]._lim)
            else:
                raise TypeError(f'idx is {idx}{self} len is {len(self)}')
    