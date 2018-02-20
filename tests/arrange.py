import unittest
import pandas as pd
from tableshaper.commands.arrange import arrange

class TestArrange(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'Arrange'
        cls.table_1 = pd.read_csv('tests/data/table1.csv')

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