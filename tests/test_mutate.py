import pandas as pd

from click.testing import CliRunner

from tableshaper.cli import cli

table_1 = pd.read_csv('tests/data/table1.csv')

# Row-wise division
def test_rowwise_division():
    runner = CliRunner()
    # Note that we need to add the decimal to the one million in
    # denominator. Without it, we would be doing division with two integers
    # which throws away the remainder in standard Python evaluation. Integer
    # division with pandas objects doesn't do this. 
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['mutate', '--row', 'population_in_millions = population / 1000000.0'],
        catch_exceptions=False)
    expect = table_1.copy()
    expect['population_in_millions'] = expect['population'] / 1000000
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Row-wise number formatting
def test_rowwise_number_formatting():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['mutate', '--row', 'cases = "{:0>9.2f}".format(cases)'],
        catch_exceptions=False)
    def assign_cases(df):
        return df.cases.apply(lambda d: '{:0>9.2f}'.format(d))
    expect = (
        table_1
            .copy()
            .assign(cases = assign_cases)
    )
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Vectorized division
def test_vectorized_division():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['mutate', 'population_in_millions = population / 1000000'],
        catch_exceptions=False)
    expect = table_1.copy()
    expect['population_in_millions'] = expect['population'] / 1000000
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Vectorized addition
def test_vectorized_addition():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['mutate', 'x = population + cases'],
        catch_exceptions=False)
    expect = table_1.copy()
    expect['x'] = expect['population'] + expect['cases']
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Grouped summation
def test_grouped_summation():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['mutate', '--group-by', 'country', 'cases_sum = cases.sum()'],
        catch_exceptions=False)
    expect = table_1.copy()
    aggregated = (
        expect
            .groupby('country')
            .apply(lambda df: df.sum())[['cases']]
            .reset_index()
            .rename(columns = { 'cases': 'cases_sum' })
    )
    expect = expect.merge(aggregated, 'left', 'country')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output
