import pandas as pd

from click.testing import CliRunner

from tableshaper.cli import cli

table_2 = pd.read_csv('tests/data/table2.csv')
table_4a = pd.read_csv('tests/data/table4a.csv')

# Gather
def test_gather():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/table4a.csv'] +
        ['reshape', '--gather'] +
            ['--key', 'year'] +
            ['--value', 'population'] +
            ['--columns', '1999:2000'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = (
        table_4a
            .copy()
            .melt(id_vars=['country'],
                  value_vars=['1999', '2000'],
                  var_name='year',
                  value_name='population')
    )
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Spread
def test_spread():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/table2.csv'] +
        ['reshape', '--spread'] +
            ['--key', 'type'] +
            ['--value', 'count'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = (
        table_2
            .copy()
            .set_index(['country', 'year', 'type'])
            .unstack('type')
            .reset_index()
    )
    expect.columns = [name[1] if name[0] == 'count' else name[0] for name in expect.columns]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output
