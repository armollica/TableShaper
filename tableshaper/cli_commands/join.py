import click
import pandas as pd

def join(df, way, keys, right):
    if right == '-':
        right_df = pd.read_csv(click.get_text_stream('stdin'))
    else:
        right_df = pd.read_csv(right)
    
    if way == 'bind-rows':
        df = pd.concat([df, right_df])
    elif way == 'bind-columns':
        df = pd.concat([df, right_df], axis = 1)
    else:
        keys_list = map(lambda x: x.strip(), keys.split(','))
        df = df.merge(right_df, on = keys_list, how = way)
    
    return df

@click.command('join')
@click.option('-l', '--left', 'way', flag_value = 'left', default = True,
              help = 'Left join')
@click.option('-r', '--right', 'way', flag_value = 'right',
              help = 'Right join')
@click.option('-o', '--outer', 'way', flag_value = 'outer',
              help = 'Outer join')
@click.option('-i', '--inner', 'way', flag_value = 'inner',
              help = 'Inner join')
@click.option('--bind-rows', 'way', flag_value = 'bind-rows',
              help = 'Bind rows')
@click.option('--bind-columns', 'way', flag_value = 'bind-columns',
              help = 'Bind columns')
@click.option('-k', '--keys', type = click.STRING,
              help = 'Columns to join tables on')
@click.argument('right', default = '-', type = click.Path())
@click.pass_context
def cli(context, way, keys, right):
    '''
    Join tables.

    \b
    SQL-style joins
    -l, --left
    -r, --right
    -o, --outer
    -i, --inner
    Join two tables based on common column values.

    \b
    -k, --keys
    Column to join tables with. Only applies to SQL-style joins.
    
    \b
    Examples:
    join -k id right.csv
    join -r -k id right.csv
    join -o -k 'state_id, county_id' right.csv

    \b
    Bind columns or rows
    --bind-rows
    --bind-columns
    Bind rows or columns from two tables together.

    \b
    Examples:
    join -bind-rows right.csv
    join -bind-columns right.csv

    '''
    table = context.obj['get_target']()

    table = join(table, way, keys, right)
    
    context.obj['update_target'](table)
