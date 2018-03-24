import pandas as pd

from click.testing import CliRunner

from tableshaper.cli import cli

table_1 = pd.read_csv('tests/data/table1.csv')

# Assigning columns
def test_assign():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['rename', 'n = cases, pop = population'],
        catch_exceptions=False)
    expect = (
        table_1
            .copy()
            .rename(columns = { 'cases': 'n', 'population': 'pop' })
    )
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Mapping columns
def test_map():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['rename', '--map', 'name.upper()'],
        catch_exceptions=False)
    expect = (
        table_1
            .copy()
            .rename(columns = lambda name: name.upper())
    )
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output
