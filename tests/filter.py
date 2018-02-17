import unittest
import pandas as pd
from tidytable.commands.filter import filter_dataframe

class TestFilter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'Filter'
        cls.table_1 = pd.read_csv('tests/data/table1.csv')
        cls.table_2 = pd.read_csv('tests/data/table2.csv')
        cls.table_3 = pd.read_csv('tests/data/table3.csv')
        cls.table_4a = pd.read_csv('tests/data/table4a.csv')
        cls.table_4b = pd.read_csv('tests/data/table4b.csv')
        cls.table_5 = pd.read_csv('tests/data/table5.csv')

    def test_filter_vectorized(self):

        # Population is less than 173 million
        actual = filter_dataframe(self.table_1, 'vectorized', 'population < 173000000')
        expect = self.table_1.copy()
        expect = expect[expect.population < 173000000]
        self.assertTrue(expect.equals(actual))

    def test_filter_slice(self):
        
        # Select the first three rows
        actual = filter_dataframe(self.table_1, 'slice', '1:3')
        expect = self.table_1.copy()
        expect = expect.iloc[0:3]
        self.assertTrue(expect.equals(actual))

        # Select the third through sixth rows
        actual = filter_dataframe(self.table_1, 'slice', '3:6')
        expect = self.table_1.copy()
        expect = expect.iloc[2:6]
        self.assertTrue(expect.equals(actual))

if __name__ == '__main__':
    unittest.main()