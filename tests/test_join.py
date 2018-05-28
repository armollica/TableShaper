import pandas as pd

from click.testing import CliRunner

from tableshaper.cli import cli

joinable_1 = pd.read_csv('tests/data/joinable1.csv')
joinable_2 = pd.read_csv('tests/data/joinable2.csv')

# Left join
def test_left():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/joinable1.csv'] +
        ['input', 'tests/data/joinable2.csv'] +
        ['target', 'joinable1'] +
        ['join', '--left', '--keys', 'id', 'joinable2'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = joinable_1.copy().merge(joinable_2, 'left', 'id')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Right join
def test_right():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/joinable1.csv'] +
        ['input', 'tests/data/joinable2.csv'] +
        ['target', 'joinable1'] +
        ['join', '--right', '--keys', 'id', 'joinable2'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = joinable_1.copy().merge(joinable_2, 'right', 'id')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Inner join
def test_inner():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/joinable1.csv'] +
        ['input', 'tests/data/joinable2.csv'] +
        ['target', 'joinable1'] +
        ['join', '--inner', '--keys', 'id', 'joinable2'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = joinable_1.copy().merge(joinable_2, 'inner', 'id')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Outer join
def test_outer():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/joinable1.csv'] +
        ['input', 'tests/data/joinable2.csv'] +
        ['target', 'joinable1'] +
        ['join', '--outer', '--keys', 'id', 'joinable2'] +
        ['output', '-'],
        catch_exceptions=False)
    expect = joinable_1.copy().merge(joinable_2, 'outer', 'id')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output
