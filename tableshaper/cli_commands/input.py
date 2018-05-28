import os, sys, glob, json, click
import pandas as pd
import geopandas as gpd

def filename_to_tablename(filename):
    basename = os.path.basename(filename)
    return os.path.splitext(basename)[0]

def read_other_json(file):
    is_file = hasattr(file, 'read')
    if is_file:
        data = json.loads(file.read())
        return pd.io.json.json_normalize(data, sep='_')
    with open(file, 'rb') as f:
        data = json.loads(f.read())
        return pd.io.json.json_normalize(data, sep='_')

format_choices = ['csv', 'tsv', 'json', 'excel', 'geojson', 'topojson', 'shp',
                  'feather', 'parquet', 'stata', 'sas', 'html']

json_format_choices = ['split', 'records', 'index', 'columns', 'values',
                       'other']

@click.command('input')
@click.option('-n', '--name', 'name', type=click.STRING)
@click.option('-f', '--format', 'format', default='csv',
              type=click.Choice(format_choices))
@click.option('-j', '--json-format', 'json_format', default='records',
              type=click.Choice(json_format_choices))
@click.option('-r', '--raw', 'raw', flag_value='raw',
              help = "Don't guess data types")
@click.option('-s', '--sheet', 'sheet', 
              help = "What sheet to read from Excel file")
@click.argument('file', type=click.STRING)
@click.pass_context
def cli(context, name, format, json_format, raw, sheet, file):
    '''
    Read in a table.
    '''
    
    # Should we guess at the data types of columns?
    dtype = None
    if raw:
        dtype = str

    # Read the table
    def read_table(file):
        try:
            if format == 'csv':
                return pd.read_csv(file, dtype=dtype)
            elif format == 'tsv':
                return pd.read_csv(file, sep='\t', dtype=dtype)    
            elif format == 'json':
                if json_format != 'other':
                    return pd.read_json(file, orient=json_format)
                return read_other_json(file)
            elif format == 'excel':
                if sheet is None:
                    click.echo('Must specify a sheet when reading an Excel file.', err=True)
                return pd.read_excel(file, sheet_name=sheet)
            elif format == 'feather':
                return pd.read_feather(file)
            elif format == 'parquet':
                return pd.read_parquet(file)
            elif format == 'stata':
                return pd.read_stata(file)
            elif format == 'sas':
                return pd.read_sas(file)
            elif format == 'geojson':
                return gpd.read_file(file, driver='GeoJSON')
            elif format == 'topojson':
                return gpd.read_file(file, driver='TopoJSON')
            elif format == 'shp':
                return gpd.read_file(file, driver='ESRI Shapefile')
        except Exception as e:
            click.echo('Could not read "{}": {}'.format(file, e), err=True)

    if file == '-':
        table = read_table(sys.stdin)

        # Determine what to name the table
        tablename = 'table'
        if name:
            tablename = name    
        
        # Add the table to the list and make it the current target
        context.obj['add_table'](tablename, table)
        context.obj['set_target'](tablename)
    else:
        filenames = glob.glob(file)
        n = len(filenames)
        for i, filename in enumerate(filenames):
            table = read_table(filename)
            
            # Determine what to name the table
            if name:
                if n == 1:
                    tablename = name
                else:
                    tablename = '{name}-{i}'.format(name=name, i=i)
            else:
                tablename = filename_to_tablename(filename)
            
            # Add the table to the list and make it the current target
            context.obj['add_table'](tablename, table)
            context.obj['set_target'](tablename)
    
