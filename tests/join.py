import unittest
import pandas as pd
from tidytable.commands.join import join

class TestJoin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'Join'
        cls.joinable_1 = pd.read_csv('tests/data/joinable1.csv')
        cls.joinable_2 = pd.read_csv('tests/data/joinable2.csv')

    def test_join_left(self):
        actual = join(self.joinable_1, 'left', 'id', 'tests/data/joinable2.csv')
        expect = self.joinable_1.copy().merge(self.joinable_2, 'left', 'id')
        self.assertTrue(expect.equals(actual))
    
    def test_join_right(self):
        actual = join(self.joinable_1, 'right', 'id', 'tests/data/joinable2.csv')
        expect = self.joinable_1.copy().merge(self.joinable_2, 'right', 'id')
        self.assertTrue(expect.equals(actual))
    
    def test_join_inner(self):
        actual = join(self.joinable_1, 'inner', 'id', 'tests/data/joinable2.csv')
        expect = self.joinable_1.copy().merge(self.joinable_2, 'inner', 'id')
        self.assertTrue(expect.equals(actual))
    
    def test_join_outer(self):
        actual = join(self.joinable_1, 'outer', 'id', 'tests/data/joinable2.csv')
        expect = self.joinable_1.copy().merge(self.joinable_2, 'outer', 'id')
        self.assertTrue(expect.equals(actual))

if __name__ == '__main__':
    unittest.main()