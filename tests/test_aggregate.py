import pandas as pd

from click.testing import CliRunner

from tableshaper.cli import cli

table_1 = pd.read_csv('tests/data/table1.csv')

# Aggregate
def test_aggregate():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/table1.csv'] +
        ['aggregate', '--group-by', 'country', 'population = population.sum()'] + 
        ['output', '-'],
        catch_exceptions=False)
    expect = (
        table_1
            .copy()
            .groupby(['country'])
            .sum()
            .reset_index()[['country', 'population']]
    )
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output
