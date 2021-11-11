import unittest
import sys
sys.path.append('spch_module')
from spch_module import ALL_SPCH_LIST
class init_test(unittest.TestCase):
    def get_all_spch():
        return ALL_SPCH_LIST
        
    def test_laod_all(self):
        self.assertRaises(Exception, get_all_spch)