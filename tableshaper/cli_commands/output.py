import os
import click
import pandas as table

@click.command('output')
@click.option('-n', '--name', 'name', type=click.STRING)
@click.option('-f', '--format', 'format', default='csv',
              type=click.Choice(['csv', 'tsv', 'json']))
@click.argument('file', type=click.File('wb'))
@click.pass_context
def cli(context, name, format, file):
    '''
    Output a table.
    '''

    context.obj['output_called'] = True

    if name:
        table = context.obj['tables'][name]
    else:
        table = context.obj['get_target']()
    
    def write_table(table, file):
        if format == 'json':
            return table.to_json(file, orient='records')
        elif format == 'tsv':
            return table.to_csv(file, sep='\t', index=False)    
        elif format == 'csv':
            return table.to_csv(file, index=False)
    try:
        write_table(table, file)
    except Exception as e:
        click.echo('Could not write "{}": {}'.format(file.name, e), err=True)
