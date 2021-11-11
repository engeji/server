import os
import sys
sys.path.append(r'E:\macro\dks_vue\server')
from collections import namedtuple
from typing import Iterable, List

from test_main import Main_test

from spch_module.struct import Limit# pylint: disable=import-error
from spch_module.defaults import DEFAULT_LIMITS# pylint: disable=import-error
from spch_module.comp import Result, Solush# pylint: disable=import-error

class Test_freq(Main_test):
    def get_result(self):
        t_in = next(filter(lambda x: x['key']=='t_in', DEFAULT_LIMITS))['value']
        res = Result(None)
        for prove in self._list_prove:
            q = prove.q / float(prove.w_cnt.split('+')[0])
            s = Solush(q, prove.p_in, prove.p_out, t_in)
            freqs = list(map(int,prove.freq.split('+')))
            s.set_sol_by_comp(freqs, self._comp)
            res.append(s)
            print(s, sum([int(ss.gasoline_rate) for ss in s._sol_data]))
        return res


if __name__ == "__main__":
    lim = Limit(**{
        dic['key']:dic['value']
    for dic in DEFAULT_LIMITS})  

    xl_file = r'server\tests\for_tst_2step_freq.xlsx'

    t = Test_freq(xl_file, lim)
    print(t.get_result())