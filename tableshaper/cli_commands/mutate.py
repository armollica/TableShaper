import click
import pandas as pd
from tableshaper import mutate, pipe, group_by
from tableshaper.helpers import processor, parse_key_value, evaluate

def row_mutate(df, column_name, expression):
    def compute(df):
        application = lambda row: evaluate(expression, row.to_dict())
        return df.apply(application, axis = 1)
    assignment = { column_name: compute }
    return df.assign(**assignment)

@click.command('mutate')
@click.option('-r', '--row-wise', 'way', flag_value = 'row-wise',
              help = 'Row-wise transformation')
@click.option('-g', '--group-by', 'group_by_expression', type = click.STRING,
              help = 'Column(s) to group rows by')
@click.argument('mutation', type = click.STRING)
@processor
def cli(dfs, way, group_by_expression, mutation):
    '''
    Create new columns.
    
    A new column is created by assigning a new variable in
    a python expression. Mutation follow this format:

    new_column <- [python expression]
    
    Columns with the same name will be overwritten.

    \b
    By default mutation will be vector-based mutation. All columns of the
    table are put in the namespace as a pandas Series. Grouped mutations
    are possible with the --group-by option

    \b
    -g, --group-by <columns>
    Comma-separated list of columns to group by. Only applies when 
    `-r, --row-wise` flag is not active.

    \b
    Examples:
    mutate 'real_value <- value * (price / 100)'
    mutate 'touches_lake_mi <- state.isin(["WI", "MI", "IL", "IN"])'
    mutate --group-by state 'population_share <- pop / pop.sum()'

    \b
    -r, --row-wise
    Perform row-wise mutation. Each row is evaluated individually. This
    will often be slower than vectorized mutation, but is more flexible in
    some cases. Grouped mutations are not possible; the --group-by option
    is ignored. Columns in the row are put in the namespace as an
    individual value. 

    \b
    Examples:
    mutate -r 'id <- "%05d" % id'
    mutate -r 'state <- id[0:2]'

    '''
    for df in dfs:
        key_value = parse_key_value(mutation.strip())
        name = key_value['key']
        expression = key_value['value']

        if way == 'row-wise':
            yield row_mutate(df, name, expression)
        else:
            if group_by_expression is not None:  
                groups = map(lambda x: x.strip(), group_by_expression.split(','))
                print groups
                yield pipe(df)(
                    group_by(*groups)(
                        mutate(**{ name: expression })
                    )
                )
            else:
                yield mutate(**{ name: expression })(df)
