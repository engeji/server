import sys
sys.path.append(r'E:\macro\dks_vue\server')
from spch_module.comp import Comp# pylint: disable=import-error
from spch_module import ALL_SPCH_LIST# pylint: disable=import-error
from spch_module.defaults import Header, get_dic_HEADERS_LIST# pylint: disable=import-error
import pandas
from collections import namedtuple
from typing import List
from spch_module.struct import tup_cls, DEFAULT_LIMITS# pylint: disable=import-error


class Main_test(Header):
    def __init__ (self, path, lim):
        self._cur_limits = lim
        self._f_ex = pandas.ExcelFile(path)
        self._data_list:pandas.DataFrame = self._f_ex.parse(sheet_name=self._f_ex.sheet_names[0])        
        spch_names = self._f_ex.sheet_names[0].split('+')
        self._spch_steps = [
            next(filter(lambda x: x.name==sp_name, ALL_SPCH_LIST))
        for sp_name in spch_names]
        self._comp = Comp(self._spch_steps,self._cur_limits)
        Prove = namedtuple('prove_tup', self._data_list.columns)
        self._list_prove:List[Prove] = [
            Prove(**{
                column:row[1][column]
            for column in self._data_list.columns})
        for row in self._data_list.iterrows()]
        
        print(self._data_list.columns)
        super().__init__(*zip(*[
            get_dic_HEADERS_LIST(head)['title'].split(',')
        for head in self._data_list.columns]))

        for item in self._list_prove:
            self.add_data(item._asdict().values())
if __name__ == '__main__':
    path = r'E:\macro\dks_vue\server\tests'
    f = r'\for_tst_2step_freq.xlsx'
    t = Main_test(path + f, None)
    print(t)