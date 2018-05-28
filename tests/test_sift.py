import pandas as pd

from click.testing import CliRunner

from tableshaper.cli import cli

table_1 = pd.read_csv('tests/data/table1.csv')
cars = pd.read_csv('tests/data/cars.csv')

# Vectorized with number comparator
def test_vectorized_number():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/table1.csv'] +
        ['sift', 'population < 173000000'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = table_1.copy()
    expect = expect[expect.population < 173000000]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Vectorized with string operator
def test_vectorized_string():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/table1.csv'] +
        ['sift', 'country.isin(["Afghanistan", "China"])'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = table_1.copy()
    expect = expect[expect.country.isin(["Afghanistan", "China"])]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Row-wise with number comparator
def test_rowwise_number():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/table1.csv'] +
        ['sift', '--row', 'population > 173000000'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = table_1.copy()
    expect = expect[expect.population > 173000000]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Row-wise with string comparator
def test_rowwise_string():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/table1.csv'] +
        ['sift', '--row', 'country in ["Afghanistan", "China"]'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = table_1.copy()
    expect = expect[expect.country.isin(["Afghanistan", "China"])]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Slice first 5
def test_slice_first_5():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/cars.csv'] +
        ['sift', '--slice', ':5'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = cars.copy().iloc[0:5]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Slice last 5
def test_slice_last_5():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/cars.csv'] +
        ['sift', '--slice', '~5:'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = cars.copy()
    n = len(expect)
    i0 = n - 5
    i1 = n
    expect = expect.iloc[i0:i1]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Slice inner range
def test_slice_inner_range():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/cars.csv'] +
        ['sift', '--slice', '3:6'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = cars.copy().iloc[2:6]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Slice inner range from back
def test_slice_inner_range_from_back():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/cars.csv'] +
        ['sift', '--slice', '~6:~3'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = cars.copy()
    n = len(expect)
    i0 = n - 6
    i1 = n - 3
    expect = expect.iloc[i0:i1]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Slice multiple ranges
def test_slice_multiple():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/cars.csv'] +
        ['sift', '--slice', ':5, 7:9'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = cars.copy().iloc[range(0, 5) + range(6, 9)]
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output
