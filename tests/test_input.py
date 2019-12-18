import pandas as pd
import geopandas as gpd

from click.testing import CliRunner
import click

from tableshaper.cli import cli

# Read CSV
def test_csv():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', 'tests/data/cars.csv'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = pd.read_csv('tests/data/cars.csv')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Read TSV
def test_tsv():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', '-f', 'tsv', 'tests/data/cars.tsv'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = pd.read_csv('tests/data/cars.tsv', sep='\t')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Read pipe-delimited file
def test_dsv():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', '-f', 'dsv', '-d', '|', 'tests/data/cars.psv'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = pd.read_csv('tests/data/cars.psv', sep='|')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Read excel file
def test_excel():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', '-f', 'excel', '-s', 'cars', 'tests/data/cars.xlsx'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = pd.read_excel('tests/data/cars.xlsx', sheet_name='cars')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Read GeoJSON
# TODO: Figure out the encoding issue. This may be a problem with Fiona or the file encoding.
# def test_geojson():
#     runner = CliRunner()
#     result = runner.invoke(cli,
#         ['input', '-f', 'geojson', 'tests/data/counties-geo.json'] +
#         ['output', '-'],
#     expect = gpd.read_file('tests/data/counties-geo.json', driver='GeoJSON')
#     assert result.exit_code == 0
#     assert expect

# Read TopoJSON
def test_topojson():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', '-f', 'topojson', 'tests/data/counties-topo.json'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = gpd.read_file('tests/data/counties-topo.json', driver='TopoJSON')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output

# Read Shapefile
def test_shapefile():
    runner = CliRunner()
    result = runner.invoke(cli,
        ['input', '-f', 'shp', 'tests/data/counties.shp'] +
        ['output', '-'],
        catch_exceptions = False)
    expect = gpd.read_file('tests/data/counties.shp', driver='ESRI Shapefile')
    assert result.exit_code == 0
    assert expect.to_csv(index=False) == result.output 

# Try to read file that doesn't exist
def test_file_doesnt_exist():
    runner = CliRunner()
    result = runner.invoke(cli, ['input', 'i-dont-exist.csv'])
    assert result.exit_code == 1
    # TODO figure out how to test for the error message.
