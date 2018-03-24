import sys
import logging
import pandas as pd

from click.testing import CliRunner

from tableshaper.cli import cli

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

joinable_1 = pd.read_csv('tests/data/joinable1.csv')
joinable_2 = pd.read_csv('tests/data/joinable2.csv')

# Left join
def test_left():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/joinable1.csv'] +
        ['join', '--left', '--keys', 'id', 'tests/data/joinable2.csv'],
        catch_exceptions=False)
    expect = joinable_1.copy().merge(joinable_2, 'left', 'id')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Right join
def test_right():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/joinable1.csv'] +
        ['join', '--right', '--keys', 'id', 'tests/data/joinable2.csv'],
        catch_exceptions=False)
    expect = joinable_1.copy().merge(joinable_2, 'right', 'id')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Inner join
def test_inner():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/joinable1.csv'] +
        ['join', '--inner', '--keys', 'id', 'tests/data/joinable2.csv'],
        catch_exceptions=False)
    expect = joinable_1.copy().merge(joinable_2, 'inner', 'id')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Outer join
def test_outer():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['--input', 'tests/data/joinable1.csv'] +
        ['join', '--outer', '--keys', 'id', 'tests/data/joinable2.csv'],
        catch_exceptions=False)
    expect = joinable_1.copy().merge(joinable_2, 'outer', 'id')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output
