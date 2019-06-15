import fnmatch, click
import pandas as pd

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
@click.argument('right', default = '-', type = click.STRING)
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
    tables = context.obj['tables']

    if way in ['bind-rows', 'bind-columns']:    
        table_names = list(tables.keys())
        right_names = fnmatch.filter(table_names, right)
        right_tables = []
        for right_name in right_names:
            right_tables.append(tables[right_name])
        if way == 'bind-rows':
            table = pd.concat([table] + right_tables)
        elif way == 'bind-columns':
            table = pd.concat([table] + right_tables, axis = 1)
    else:
        keys_list = list(map(lambda x: x.strip(), keys.split(',')))
        right_table = tables[right]
        table = table.merge(right_table, on = keys_list, how = way)
    
    context.obj['update_target'](table)
