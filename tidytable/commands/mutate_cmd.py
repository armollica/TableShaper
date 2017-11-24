import click
import pandas as pd
from tidytable.util import processor

def row_mutate(df, column_name, expression):
    return df.assign(**{ column_name: lambda x: x.apply(lambda y: eval(expression, y.to_dict()), axis = 1)})

def column_mutate(df, column_name, expression):
    return df.assign(**{ column_name: lambda x: eval(expression, x.to_dict('series')) })

def column_mutate_grouped(df, groups, column_name, expression):
    def apply_func(df):
        return column_mutate(df, column_name, expression)
    return df.groupby(groups).apply(apply_func).reset_index(drop = True)

@click.command('mutate')
@click.option('-w', '--way',
              default = 'by-column',
              type = click.Choice(['by-column', 'by-row']),
              show_default = True)
@click.option('-g', '--group-by', type = click.STRING)
@click.option('-n', '--name', type = click.STRING)
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, group_by, name, way, expression):
    '''
    Create new columns. A new column is created by assigning a new variable in
    a python expression. Columns with the same name will be overwritten.

    \b
    --way by-row
    Row-wise mutation. Each row is evaluated individually. Columns in the row
    are put in the namespace as an individual value. Grouped mutations are not
    possible; the --group-by option is ignored.

    Examples:
    mutate --way by-row --name id '"%05d" % id'
    mutate --way by-row -n state 'id[0:2]' \

    \b
    --way by-column (default)
    Column-wise mutation. All columns of the table are put in the namespace
    as a pandas Series. Grouped mutations are possible with the --group-by
    option

    Examples:
    mutate --way by-column --name real_value 'value * (price / 100)'
    mutate -n touches_lake_mi 'state.isin(['WI', 'MI'])'
    mutate --group-by state -n population_share 'pop / pop.sum()'

    '''
    for df in dfs:
        if way == 'by-row':
            df = row_mutate(df, name, expression)
        if way == 'by-column':    
            if group_by is not None:     
                groups = map(lambda x: x.strip(), group_by.split(','))
                df = column_mutate_grouped(df, groups, name, expression)
            else:
                df = column_mutate(df, name, expression)
        yield df
