import os
import click
import pandas as table

@click.command('output')
@click.option('-n', '--name', 'name', type=click.STRING)
@click.option('-t', '--type', 'type', default='csv',
              type=click.Choice(['csv', 'tsv', 'json']))
@click.argument('file', type=click.File('wb'))
@click.pass_context
def cli(context, name, type, file):
    '''
    Output a table.
    '''

    context.obj['output_called'] = True

    if name:
        table = context.obj['tables'][name]
    else:
        table = context.obj['get_target']()
    
    def write_table(table, file):
        if type == 'json':
            return table.to_json(file, orient='records')
        elif type == 'tsv':
            return table.to_csv(file, sep='\t', index=False)    
        elif type == 'csv':
            return table.to_csv(file, index=False)
    try:
        write_table(table, file)
    except Exception as e:
        click.echo('Could not write "{}": {}'.format(file.name, e), err=True)

