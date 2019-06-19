import os, sys, fnmatch, click
import pandas as pd
from tabulate import tabulate

format_choices = ['csv', 'tsv', 'json',  'geojson', 'shp', 'markdown', 'html',
                  'feather', 'parquet']

@click.command('output')
@click.option('-t', '--tables', 'tables', type=click.STRING)
@click.option('-f', '--format', 'format', default='csv',
              type=click.Choice(format_choices))
@click.option('-d', '--dir', 'directory', default='.', type=click.STRING)
@click.argument('file_name', type=click.STRING)
@click.pass_context
def cli(context, tables, format, directory, file_name):
    '''
    Write out a table.
    '''

    context.obj['printed'] = True
    table_names = list(context.obj['tables'].keys())

    output_names = []
    if tables is None:
        output_names = [context.obj['target']]
    else:
        output_names = fnmatch.filter(table_names, tables)

    def write_table(table, file):
        if format == 'json':
            table.to_json(file, orient='records')
        elif format == 'tsv':
            table.to_csv(file, sep='\t', index=False)    
        elif format == 'csv':
            table.to_csv(file, index=False)
        elif format == 'geojson':
            table.to_file(file, driver='GeoJSON')
        elif format == 'shp':
            table.to_file(file, driver='ESRI Shapefile')
        elif format == 'markdown':
            data = tabulate(table.values, list(table), tablefmt='pipe') + '\n'
            is_stdout = hasattr(file, 'write')
            if is_stdout:
                file.write(data)
            else:
                with open(file, 'w') as f:
                    f.write(data)
        elif format == 'html':
            data = tabulate(table.values, list(table), tablefmt='html') + '\n'
            is_stdout = hasattr(file, 'write')
            if is_stdout:
                file.write(data)
            else:
                with open(file, 'w') as f:
                    f.write(data)
        elif format == 'parquet':
            table.to_parquet(file)
        elif format == 'feather':
            table.to_feather(file)
    
    n = len(output_names)

    if n == 0:
        click.echo("No table matches '{}' in output command.".format(tables), err=True)
    elif n == 1:
        output_name = output_names[0]
        if file_name == '*':
            file_name = '{name}.{ext}'.format(name=output_name, ext=format)
        file_path = '{directory}/{file_name}'.format(
            directory=directory,
            file_name=file_name,
        )
        if file_name == '-':
            file_path = sys.stdout
        table = context.obj['tables'][output_name]
        try:
            write_table(table, file_path)
        except Exception as e:
            click.echo('Could not write "{}": {}'.format(output_name, e), err=True)
    else:
        if file_name != '+':
            click.echo("Must use '+' filename when outputting multiple tables.", err=True)
        for output_name in output_names:
            file_path = '{directory}/{name}.{ext}'.format(
                directory=directory,
                name=output_name,
                ext=format
            )
            table = context.obj['tables'][output_name]
            try:
                write_table(table, file_path)
            except Exception as e:
                click.echo('Could not write "{}": {}'.format(output_name, e), err=True)
    
    


    
