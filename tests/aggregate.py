import unittest
import pandas as pd
from tidytable.commands.aggregate import aggregate

# country  population
# Afghanistan    40582431
# Brazil   346511260
# China  2553343855

class TestAggregate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'Aggregate'
        cls.table_1 = pd.read_csv('tests/data/table1.csv')
        cls.table_2 = pd.read_csv('tests/data/table2.csv')
        cls.table_3 = pd.read_csv('tests/data/table3.csv')
        cls.table_4a = pd.read_csv('tests/data/table4a.csv')
        cls.table_4b = pd.read_csv('tests/data/table4b.csv')
        cls.table_5 = pd.read_csv('tests/data/table5.csv')

    def test_flat_aggregate(self):

        actual = aggregate(self.table_1, 'country', 'population <- population.sum()')

        expect = self.table_1.copy().groupby(['country'])
        expect = expect.sum().reset_index()[['country', 'population']]
        
        self.assertTrue(expect.equals(actual))

if __name__ == '__main__':
    unittest.main()