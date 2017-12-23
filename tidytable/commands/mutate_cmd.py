import click
import pandas as pd
from tidytable.util import processor, parse_key_value

def row_mutate(df, column_name, expression):
    return df.assign(**{ column_name: lambda x: x.apply(lambda y: eval(expression, y.to_dict()), axis = 1)})

def column_mutate(df, column_name, expression):
    return df.assign(**{ column_name: lambda x: eval(expression, x.to_dict('series')) })

def column_mutate_grouped(df, groups, column_name, expression):
    def apply_func(df):
        return column_mutate(df, column_name, expression)
    return df.groupby(groups).apply(apply_func).reset_index(drop = True)

@click.command('mutate')
@click.option('-v', '--vectorized', 'way', flag_value = 'vectorized', default = True)
@click.option('-r', '--row-wise', 'way', flag_value = 'row-wise')
@click.option('-g', '--group-by', type = click.STRING)
@click.argument('mutation', type = click.STRING)
@processor
def cli(dfs, way, group_by, mutation):
    '''
    Create new columns. A new column is created by assigning a new variable in
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
    mutate -r 'state <- id[0:2]' \

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
    key_value = parse_key_value(mutation.strip())
    name = key_value['key']
    expression = key_value['value']
    for df in dfs:
        if way == 'row-wise':
            df = row_mutate(df, name, expression)
        elif way == 'vectorized':    
            if group_by is not None:     
                groups = map(lambda x: x.strip(), group_by.split(','))
                df = column_mutate_grouped(df, groups, name, expression)
            else:
                df = column_mutate(df, name, expression)
        yield df
