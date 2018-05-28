import os, sys, fnmatch, click
import pandas as pd

@click.command('output')
@click.option('-t', '--tables', 'tables', type=click.STRING)
@click.option('-f', '--format', 'format', default='csv',
              type=click.Choice(['csv', 'tsv', 'json']))
@click.option('-d', '--dir', 'directory', default='.', type=click.STRING)
@click.argument('file_name', type=click.STRING)
@click.pass_context
def cli(context, tables, format, directory, file_name):
    '''
    Output a table.
    '''

    context.obj['printed'] = True
    table_names = list(context.obj['tables'].keys())
    output_names = fnmatch.filter(table_names, tables)

    if tables is None:
        output_names = [context.obj['target']]
    
    def write_table(table, file):
        if format == 'json':
            return table.to_json(file, orient='records')
        elif format == 'tsv':
            return table.to_csv(file, sep='\t', index=False)    
        elif format == 'csv':
            return table.to_csv(file, index=False)
    
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
    
    


    
