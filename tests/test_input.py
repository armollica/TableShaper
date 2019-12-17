import pandas as pd
from pprint import pprint
from click.testing import CliRunner
import click

from tableshaper.cli import cli

# Read CSV
def test_input_csv():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/cars.csv'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = pd.read_csv('tests/data/cars.csv')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Read TSV
def test_input_tsv():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', '-f', 'tsv', 'tests/data/cars.tsv'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = pd.read_csv('tests/data/cars.tsv', sep='\t')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Read pipe-delimited file
def test_input_dsv():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', '-f', 'dsv', '-d', '|', 'tests/data/cars.psv'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = pd.read_csv('tests/data/cars.psv', sep='|')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Read excel file
def test_input_excel():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', '-f', 'excel', '-s', 'cars', 'tests/data/cars.xlsx'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = pd.read_excel('tests/data/cars.xlsx', sheet_name='cars')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Try to read file that doesn't exist
def test_file_doesnt_exist():
    runner = CliRunner()
    result = runner.invoke(cli, ['input', 'i-dont-exist.csv'])
    assert result.exit_code == 1
    # TODO figure out how to test for the error message.
