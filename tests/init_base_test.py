import unittest
import sys
sys.path.append('spch_module')
from spch_module import ALL_SPCH_LIST #pylint: disable=import-error
class init_test(unittest.TestCase):
    def test_laod_all(self):
        self.assertGreater(len(ALL_SPCH_LIST), 0,"")