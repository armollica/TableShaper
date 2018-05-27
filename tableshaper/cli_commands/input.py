import os, sys, glob, click
import pandas as pd

def filename_to_tablename(filename):
    basename = os.path.basename(filename)
    return os.path.splitext(basename)[0]

@click.command('input')
@click.option('-n', '--name', 'name', type=click.STRING)
@click.option('-t', '--type', 'type', default='csv',
              type=click.Choice(['csv', 'tsv', 'json']))
@click.option('-r', '--raw', 'raw', flag_value='raw',
              help = "Don't guess data types")
@click.argument('file', type=click.STRING)
@click.pass_context
def cli(context, name, type, raw, file):
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
            if type == 'json':
                return pd.read_json(file, orient='records')
            elif type == 'tsv':
                return pd.read_csv(file, sep='\t', dtype=dtype)    
            elif type == 'csv':
                return pd.read_csv(file, dtype=dtype)
        except Exception as e:
            click.echo('Could not read "{}": {}'.format(file, e), err=True)

    if file == '-':
        table = read_table(sys.stdin)
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
    
