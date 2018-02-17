import unittest
import pandas as pd
from tidytable.operations import row_mutate, column_mutate, column_mutate_grouped

class TestMutate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.table_1 = pd.read_csv('tests/data/table1.csv')
        cls.table_2 = pd.read_csv('tests/data/table2.csv')
        cls.table_3 = pd.read_csv('tests/data/table3.csv')
        cls.table_4a = pd.read_csv('tests/data/table4a.csv')
        cls.table_4b = pd.read_csv('tests/data/table4b.csv')
        cls.table_5 = pd.read_csv('tests/data/table5.csv')

    def test_row_mutate(self):
        # Note that we need to add the decimal to the one million in
        # denominator. Without it, we would be doing division with two integers
        # which throws away the remainder in standard Python evaluation. Integer
        # division with pandas objects doesn't do this.
        actual = row_mutate(self.table_1, 'population_in_millions', 'population / 1000000.0')
        expect = self.table_1.copy()
        expect['population_in_millions'] = expect['population'] / 1000000
        self.assertTrue(expect.equals(actual))

if __name__ == '__main__':
    unittest.main()