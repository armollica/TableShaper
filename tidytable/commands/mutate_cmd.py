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
              default = 'column',
              type = click.Choice(['column', 'row']),
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
    -n, --name <column name>
    Name of the new column.

    \b
    -g, --group-by <columns>
    Comma-separated list of columns to group by. Only applies when 
    `--way columns` is in effect.

    \b
    -w row / --way row
    Row-wise mutation. Each row is evaluated individually. Columns in the row
    are put in the namespace as an individual value. Grouped mutations are not
    possible; the --group-by option is ignored.

    \b
    Examples:
    mutate --way row --name id '"%05d" % id'
    mutate --way row -n state 'id[0:2]' \

    \b
    -w column / --way column (default)
    Column-wise mutation. All columns of the table are put in the namespace
    as a pandas Series. Grouped mutations are possible with the --group-by
    option

    \b
    Examples:
    mutate --way column --name real_value 'value * (price / 100)'
    mutate -n touches_lake_mi 'state.isin(['WI', 'MI'])'
    mutate --group-by state -n population_share 'pop / pop.sum()'

    '''
    for df in dfs:
        if way == 'row':
            df = row_mutate(df, name, expression)
        elif way == 'column':    
            if group_by is not None:     
                groups = map(lambda x: x.strip(), group_by.split(','))
                df = column_mutate_grouped(df, groups, name, expression)
            else:
                df = column_mutate(df, name, expression)
        yield df
