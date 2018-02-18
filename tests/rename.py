import unittest
import pandas as pd
from tidytable.commands.rename import rename

class TestRename(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'Mutate'
        cls.table_1 = pd.read_csv('tests/data/table1.csv')

    def test_rename_assign(self):
        actual = rename(self.table_1, 'assign', 'n <- cases, pop <- population')
        expect = (
            self.table_1
                .copy()
                .rename(columns = { 'cases': 'n', 'population': 'pop' })
        )
        self.assertTrue(expect.equals(actual))
    
    def test_rename_map(self):
        actual = rename(self.table_1, 'map', 'name.upper()')
        expect = (
            self.table_1
                .copy()
                .rename(columns = lambda name: name.upper())
        )
        self.assertTrue(expect.equals(actual))



if __name__ == '__main__':
    unittest.main()