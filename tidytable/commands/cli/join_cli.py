import click
import pandas as pd
from tidytable.helpers import processor
from tidytable.commands.join import join

@click.command('join')
@click.option('-l', '--left', 'way', flag_value = 'left', default = True,
              help = 'Left join')
@click.option('-r', '--right', 'way', flag_value = 'right',
              help = 'Right join')
@click.option('-o', '--outer', 'way', flag_value = 'outer',
              help = 'Outer join')
@click.option('-i', '--inner', 'way', flag_value = 'inner',
              help = 'Inner join')
@click.option('-r', '--bind-rows', 'way', flag_value = 'bind-rows',
              help = 'Bind rows')
@click.option('-c', '--bind-columns', 'way', flag_value = 'bind-columns',
              help = 'Bind columns')
@click.option('-k', '--keys', type = click.STRING,
              help = 'Columns to join tables on')
@click.argument('right', default = '-', type = click.Path())
@processor
def cli(dfs, way, keys, right):
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
    Examples:
    join -k id right.csv
    join -r -k id right.csv
    join -o -k 'state_id, county_id' right.csv

    \b
    Bind columns or rows
    -r, --bind-rows
    -c, --bind-columns
    Bind rows or columns from two tables together.

    \b
    Examples:
    join -r right.csv
    join -c right.csv

    \b
    -k, --keys
    Column to join tables with. Only applies to SQL-style joins.
    '''
    for df in dfs:
        yield join(df, way, keys, right)
