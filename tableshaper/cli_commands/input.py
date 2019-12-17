import os, sys, glob, json, click
import pandas as pd
import geopandas as gpd

def filename_to_tablename(filename):
    basename = os.path.basename(filename)
    return os.path.splitext(basename)[0]

format_choices = ['csv', 'tsv', 'dsv', 'json', 'excel', 'geojson', 'topojson', 'shp',
                  'feather', 'parquet', 'stata', 'sas']

json_format_choices = ['split', 'records', 'index', 'columns', 'values',
                       'other']

def encoding_is_ignored(format, json_format):
    if format == 'json' and json_format == 'other':
        return True
    if format in ['excel', 'feather', 'parquet', 'geojson', 'topojson', 'shp']:
        return True
    return False

def read_csv(file, dtype, encoding, **kwargs):
    table = pd.read_csv(file, dtype=dtype, encoding=encoding)
    return table

def read_tsv(file, dtype, encoding, **kwargs):
    return pd.read_csv(file, sep='\t', dtype=dtype, encoding=encoding, engine='python')

def read_dsv(file, dtype, encoding, delimiter, **kwargs):
    return pd.read_csv(file, sep=delimiter, dtype=dtype, encoding=encoding, engine='python')

def read_other_json(file):
    is_file = hasattr(file, 'read')
    if is_file:
        data = json.loads(file.read())
        return pd.io.json.json_normalize(data, sep='_')
    with open(file, 'rb') as f:
        data = json.loads(f.read())
        return pd.io.json.json_normalize(data, sep='_')

def read_json(file, json_format, encoding, **kwargs):
    if json_format != 'other':
        return pd.read_json(file, orient=json_format, encoding=encoding)
    return read_other_json(file)

def read_excel(file, sheet, **kwargs):
    if sheet is None:
        click.echo('Must specify a sheet when reading an Excel file.', err=True)
    return pd.read_excel(file, sheet_name=sheet)

def read_feather(file, **kwargs):
    return pd.read_feather(file)

def read_parquet(file, **kwargs):
    return pd.read_parquet(file)

def read_stata(file, encoding, **kwargs):
    return pd.read_stata(file, encoding=encoding)

def read_sas(file, encoding, **kwargs):
    return pd.read_sas(file, encoding=encoding)

def read_geojson(file, **kwargs):
    return gpd.read_file(file, driver='GeoJSON')

def read_topojson(file, **kwargs):
    return gpd.read_file(file, driver='TopoJSON')

def read_shapefile(file, **kwargs):
    return gpd.read_file(file, driver='ESRI Shapefile')

def read_table(file, format, dtype, encoding, delimiter, sheet, json, json_format):
    params = {
        'file': file,
        'dtype': dtype,
        'encoding': encoding,
        'delimiter': delimiter,
        'sheet': sheet,
        'json': json,
        'json_format': json_format
    }

    reader = {
        'csv': read_csv,
        'tsv': read_tsv,
        'dsv': read_dsv,
        'json': read_json,
        'excel': read_excel,
        'feather': read_feather,
        'parquet': read_parquet,
        'stata': read_stata,
        'sas': read_sas,
        'geojson': read_geojson,
        'topojson': read_topojson,
        'shp': read_shapefile
    }[format]

    try:
        return reader(**params)
    except Exception as error:
        click.echo(f'Could not read "{file}": {error}', err=True)

@click.command('input')
@click.option('-n', '--name', 'name', type=click.STRING)
@click.option('-f', '--format', 'format', default='csv',
              type=click.Choice(format_choices))
@click.option('-j', '--json-format', 'json_format', default='records',
              type=click.Choice(json_format_choices))
@click.option('-r', '--raw', 'raw', flag_value='raw',
              help = "Don't guess data types")
@click.option('-d', '--delim', 'delimiter', default=',',
              help = "What delimiter to use for parsing DSV file")
@click.option('-s', '--sheet', 'sheet', 
              help = "What sheet to read from Excel file")
@click.option('-c', '--col-names', 'col_names', type=click.STRING)
@click.option('-e', '--encoding', 'encoding', type=click.STRING, default = None)
@click.argument('file', type=click.STRING)
@click.pass_context
def cli(context, name, format, json_format, raw, delimiter, sheet, col_names, encoding, file):
    '''
    Read in a table.
    '''

    # Should we guess at the data types of columns?
    dtype = None
    if raw:
        dtype = str
    
    def update_col_names(table):
        if col_names:
            names = list(map(lambda x: x.strip(), col_names.split(',')))
            n = len(names) 
            m = len(table.columns)
            if n != m:
                click.echo(f"Number of columns names doesn't match number of columns: {n} names provided, {m} columns in table.", err=True)
            table.columns = names

    params = {
        'format': format,
        'dtype': dtype,
        'encoding': encoding,
        'delimiter': delimiter,
        'sheet': sheet,
        'json': json,
        'json_format': json_format,
    }

    if encoding is not None:
        if encoding_is_ignored(**params):
            click.echo('Encoding parameters is being ignored.')
    
    if file == '-':
        params.update({ 'file': sys.stdin })
        table = read_table(**params)
        update_col_names(table)
        
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

        if n == 0:
            click.echo(f'Filename `{file}` not found', err=True)

        for i, filename in enumerate(filenames):
            params.update({ 'file': filename })
            table = read_table(**params)
            update_col_names(table)
                
            # Determine what to name the table
            if name:
                if n == 1:
                    tablename = name
                else:
                    tablename = f'{name}-{i}'
            else:
                tablename = filename_to_tablename(filename)
            
            # Add the table to the list and make it the current target
            context.obj['add_table'](tablename, table)
            context.obj['set_target'](tablename)
    
