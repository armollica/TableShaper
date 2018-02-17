import unittest
import pandas as pd
from tidytable.commands.arrange import arrange

class TestArrange(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.table_1 = pd.read_csv('tests/data/table1.csv')
        cls.table_2 = pd.read_csv('tests/data/table2.csv')
        cls.table_3 = pd.read_csv('tests/data/table3.csv')
        cls.table_4a = pd.read_csv('tests/data/table4a.csv')
        cls.table_4b = pd.read_csv('tests/data/table4b.csv')
        cls.table_5 = pd.read_csv('tests/data/table5.csv')

    def test_arrange_single(self):
        actual = arrange(self.table_1, 'year')
        expect = self.table_1.copy()
        expect = expect.sort_values('year')
        self.assertTrue(expect.equals(actual))

        actual = arrange(self.table_1, 'population')
        expect = self.table_1.copy()
        expect = expect.sort_values('population')
        self.assertTrue(expect.equals(actual))
    
    def test_arrange_multiple(self):
        actual = arrange(self.table_1, 'year, population')
        expect = self.table_1.copy()
        expect = expect.sort_values(['year', 'population'])
        self.assertTrue(expect.equals(actual))

        actual = arrange(self.table_1, 'year, population:desc')
        expect = self.table_1.copy()
        expect = expect.sort_values(['year', 'population'],
                                    ascending = [True, False])
        self.assertTrue(expect.equals(actual))


if __name__ == '__main__':
    unittest.main()