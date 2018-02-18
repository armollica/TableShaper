import unittest
import pandas as pd
from tidytable.commands.reshape import reshape

class TestReshape(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'Reshape'
        cls.table_2 = pd.read_csv('tests/data/table2.csv')
        cls.table_4a = pd.read_csv('tests/data/table4a.csv')

    def test_reshape_gather(self):
        actual = reshape(self.table_4a, 'gather', 'year', 'population', '1999:2000')
        expect = (
            self.table_4a
                .copy()
                .melt(id_vars = ['country'],
                      value_vars = ['1999', '2000'],
                      var_name = 'year',
                      value_name = 'population')
        )
        self.assertTrue(expect.equals(actual))
    
    def test_reshape_spread(self):
        actual = reshape(self.table_2, 'spread', 'type', 'count', None)
        expect = (
            self.table_2
                .copy()
                .set_index(['country', 'year', 'type'])
                .unstack('type')
                .reset_index()
        )
        expect.columns = [name[1] if name[0] == 'count' else name[0] for name in expect.columns]
        self.assertTrue(expect.equals(actual))

if __name__ == '__main__':
    unittest.main()