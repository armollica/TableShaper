import unittest
import pandas as pd
from tidytable.commands.choose import choose

class TestChoose(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'Choose'
        cls.table_1 = pd.read_csv('tests/data/table1.csv')

    def test_choose_filter(self):

        # Column name is "country" or "population"
        actual = choose(self.table_1, 'filter', 'name == "country" or name == "population"')
        expect = self.table_1.copy()
        column_names = filter(lambda name: name == "country" or name == "population", list(expect))
        expect = expect[column_names]
        self.assertTrue(expect.equals(actual))

        # Column name is less that six characters long
        actual = choose(self.table_1, 'filter', 'len(name) < 6')
        expect = self.table_1.copy()
        column_names = filter(lambda name: len(name) < 6, list(expect))
        expect = expect[column_names]        
        self.assertTrue(expect.equals(actual))

    def test_choose_selection(self):

        # Select country and population columns
        actual = choose(self.table_1, 'selection', 'country, population')
        expect = self.table_1.copy()[['country', 'population']]
        self.assertTrue(expect.equals(actual))

        # Select all but the population column
        actual = choose(self.table_1, 'selection', '~population')
        expect = self.table_1.copy()[['country', 'year', 'cases']]
        self.assertTrue(expect.equals(actual))

        # Select all columns between year and population
        actual = choose(self.table_1, 'selection', 'year:population')
        expect = self.table_1.copy()[['year', 'cases', 'population']]
        self.assertTrue(expect.equals(actual))

        # Drop all columns between year and cases
        actual = choose(self.table_1, 'selection', '~year:cases')
        expect = self.table_1.copy()[['country', 'population']]
        self.assertTrue(expect.equals(actual))

        # Drop all columns between year and population, add back cases
        actual = choose(self.table_1, 'selection', '~year:population, cases')
        expect = self.table_1.copy()[['country', 'cases']]
        self.assertTrue(expect.equals(actual))


if __name__ == '__main__':
    unittest.main()