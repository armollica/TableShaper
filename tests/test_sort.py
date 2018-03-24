import pandas as pd

from click.testing import CliRunner

from tableshaper.cli import cli

table_1 = pd.read_csv('tests/data/table1.csv')

# Sort one column (ascending)
def test_single_ascending():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['sort', 'year'],
        catch_exceptions=False)
    expect = table_1.copy().sort_values('year')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Sort one column (descending)
def test_single_descending():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['sort', 'year:desc'],
        catch_exceptions=False)
    expect = table_1.copy().sort_values('year', ascending=False)
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Sort multiple columns (ascending)
def test_multiple_ascending():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['sort', 'year, population'],
        catch_exceptions=False)
    expect = table_1.copy().sort_values(['year', 'population'])
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Sort multiple columns (descending)
def test_multiple_descending():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['sort', 'year:desc, population:desc'],
        catch_exceptions=False)
    expect = table_1.copy().sort_values(['year', 'population'], ascending=False)
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Sort multiple columns (mix)
def test_multiple_mix():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/table1.csv'] +
        ['sort', 'year, population:desc'],
        catch_exceptions=False)
    expect = (
        table_1
            .copy()
            .sort_values(['year', 'population'], ascending=[True, False])
    )
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output
