import unittest
import pandas as pd
from tableshaper.commands.mutate import mutate

class TestMutate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'Mutate'
        cls.table_1 = pd.read_csv('tests/data/table1.csv')
        cls.table_2 = pd.read_csv('tests/data/table2.csv')
        cls.table_3 = pd.read_csv('tests/data/table3.csv')
        cls.table_4a = pd.read_csv('tests/data/table4a.csv')
        cls.table_4b = pd.read_csv('tests/data/table4b.csv')
        cls.table_5 = pd.read_csv('tests/data/table5.csv')

    def test_mutate_rowwise(self):
        
        # Division
        actual = mutate(self.table_1, 'row-wise', None, 'population_in_millions <- population / 1000000.0')
        expect = self.table_1.copy()
        expect['population_in_millions'] = expect['population'] / 1000000
        self.assertTrue(expect.equals(actual))

        # Note that we needed to add the decimal to the one million in
        # denominator. Without it, we would be doing division with two integers
        # which throws away the remainder in standard Python evaluation. Integer
        # division with pandas objects doesn't do this. 

        # Number formatting
        actual = mutate(self.table_1, 'row-wise', None, 'cases <- "{:0>9.2f}".format(cases)')
        expect = self.table_1.copy()
        expect = expect.assign(cases = lambda df: df.cases.apply(lambda d: '{:0>9.2f}'.format(d)))
        self.assertTrue(expect.equals(actual))

    def test_mutate_vectorized(self):
        
        # Division
        actual = mutate(self.table_1, 'vectorized', None, 'population_in_millions <- population / 1000000')
        expect = self.table_1.copy()
        expect['population_in_millions'] = expect['population'] / 1000000
        self.assertTrue(expect.equals(actual))

        # Addition
        actual = mutate(self.table_1, 'vectorized', None, 'x <- population + cases')
        expect = self.table_1.copy()
        expect['x'] = expect['population'] + expect['cases']
        self.assertTrue(expect.equals(actual))

    def test_mutate_grouped(self):
        
        # Summation
        actual = mutate(self.table_1, 'vectorized', 'country', 'cases_sum <- cases.sum()')
        expect = self.table_1.copy()
        aggregated = (
            expect
                .groupby('country')
                .apply(lambda df: df.sum())[['cases']]
                .reset_index()
                .rename(columns = { 'cases': 'cases_sum' })
        )
        expect = expect.merge(aggregated, 'left', 'country')
        self.assertTrue(expect.equals(actual))


if __name__ == '__main__':
    unittest.main()