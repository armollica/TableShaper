import click
import pandas as pd
from tidytable.helpers import processor
from tidytable.commands.mutate import mutate

@click.command('mutate')
@click.option('-v', '--vectorized', 'way', flag_value = 'vectorized',
              default = True,
              help = 'Vectorized transformation')
@click.option('-r', '--row-wise', 'way', flag_value = 'row-wise',
              help = 'Row-wise transformation')
@click.option('-g', '--group-by', type = click.STRING,
              help = 'Column(s) to group rows by')
@click.argument('mutation', type = click.STRING)
@processor
def cli(dfs, way, group_by, mutation):
    '''
    Create new columns.
    
    A new column is created by assigning a new variable in
    a python expression. Mutation follow this format:

    new_column <- [python expression]
    
    Columns with the same name will be overwritten.

    \b
    -r, --row-wise
    Row-wise mutation. Each row is evaluated individually. This will often 
    be slower than vectorized mutation, but is more flexible in some cases.
    Grouped mutations are not possible; the --group-by option is ignored.
    Columns in the row are put in the namespace as an individual value. 

    \b
    Examples:
    mutate -r 'id <- "%05d" % id'
    mutate -r 'state <- id[0:2]'

    \b
    -v, --vectorized (default)
    Vector-based mutation. All columns of the table are put in the namespace
    as a pandas Series. Grouped mutations are possible with the --group-by
    option

    \b
    Examples:
    mutate 'real_value <- value * (price / 100)'
    mutate 'touches_lake_mi <- state.isin(['WI', 'MI'])'
    mutate --group-by state 'population_share <- pop / pop.sum()'

    \b
    -g, --group-by <columns>
    Comma-separated list of columns to group by. Only applies when 
    `-v, --vectorized` flag is active (which it is by default).
    '''
    for df in dfs:
        yield mutate(df, way, group_by, mutation)
