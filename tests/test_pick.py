import sys
import logging
import pandas as pd

from click.testing import CliRunner

from tableshaper.cli import cli

# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

table_1 = pd.read_csv('tests/data/table1.csv')

# Sift-based picking: column name is one of two string
def test_pick_sift_1():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['pick', '--sift', 'name == "country" or name == "population"'],
        catch_exceptions=False)
    expect = table_1.copy()
    column_names = filter(lambda name: name == "country" or name == "population", list(expect))
    expect = expect[column_names]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Sift-based picking: column name is less that six characters long
def test_pick_sift_2():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['pick', '--sift', 'len(name) < 6'],
        catch_exceptions=False)
    expect = table_1.copy()
    column_names = filter(lambda name: len(name) < 6, list(expect))
    expect = expect[column_names]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Pick columns with comma-separated list
def test_pick_list():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['pick', 'country, population'],
        catch_exceptions=False)
    expect = table_1.copy()[['country', 'population']]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Drop a single column
def test_pick_exclude():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['pick', '~population'],
        catch_exceptions=False)
    expect = table_1.copy()[['country', 'year', 'cases']]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Pick all columns in a range
def test_pick_range():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['pick', 'year:population'],
        catch_exceptions=False)
    expect = table_1.copy()[['year', 'cases', 'population']]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Drop a range of columns
def test_pick_range_exclude():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['pick', '~year:cases'],
        catch_exceptions=False)
    expect = table_1.copy()[['country', 'population']]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Drop a range of columns and add one back in
def test_pick_range_exclude_add():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['pick', '~year:population, cases'],
        catch_exceptions=False)
    expect = table_1.copy()[['country', 'cases']]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output
