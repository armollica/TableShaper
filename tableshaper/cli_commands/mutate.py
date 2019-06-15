import click
import pandas as pd
from tableshaper import mutate, pipe, group_by
from tableshaper.helpers import parse_key_value, selectify, evaluate

def row_mutate(column_name, expression):
    def compute(df):
        application = lambda row: evaluate(expression, row.to_dict())
        return df.apply(application, axis = 1)
    def assign(df):
        return df.assign(**{ column_name: compute })
    return assign

def cast(series, datatype):
    if datatype == 'int':
        return series.astype(int)
    elif datatype == 'float':
        return series.astype(float)
    elif datatype == 'str':
        return series.astype(str)
    elif datatype == 'bool':
        return series.apply(lambda x: str(x).lower() in ['true', '1', 't', 'y', 'yes'])
    else:
        raise ValueError('Invalid dataype: {}. Must be int, float, str or bool.'.format(datatype))

@click.command('mutate')
@click.option('-r', '--row', 'way', flag_value = 'row-wise',
              help = 'Row-wise transformation')
@click.option('-c', '--cast', 'way', flag_value = 'cast',
              help = 'Cast columns to a different data types')
@click.option('-g', '--group-by', 'group_by_expression', type = click.STRING,
              help = 'Column(s) to group rows by')
@click.argument('mutations', type = click.STRING)
@click.pass_context
def cli(context, way, group_by_expression, mutations):
    '''
    Create new columns.
    
    A new column is created by assigning a new variable in
    a python expression. Mutation follow this format:

    name = expression
    
    Columns with the same name will be overwritten.

    Multiple mutations can be done at once. Mutations are separated
    by a semicolon like this:

    name = [expression]; name = expression; and so on ...

    \b
    By default mutation will be vector-based mutation. All columns of the
    table are put in the namespace as a pandas Series. Grouped mutations
    are possible with the --group-by option.

    \b
    -g, --group-by <columns>
    Comma-separated list of columns to group by. Only applies when 
    `-r, --row-wise` flag is not active.

    \b
    Examples:
    mutate 'real_value = value * (price / 100)'
    mutate 'touches_lake_mi = state.isin(["WI", "MI", "IL", "IN"])'
    mutate --group-by state 'population_share = pop / pop.sum()'

    \b
    -r, --row
    Perform row-wise mutation.
    
    Each row is evaluated individually. This
    will often be slower than vectorized mutation, but is more flexible in
    some cases. Grouped mutations are not possible; the --group-by option
    is ignored. Columns in the row are put in the namespace as an
    individual value. 

    \b
    Examples:
    mutate -r 'id = "%05d" % id'
    mutate -r 'state = id[0:2]'

    \b
    -c, --cast
    Cast columns to different data types.

    Provide a selection of columns followed by a datatype. One of: int, float,
    str and bool. You can cast multiple groups of columns by separating these
    selection-datatype pairs with a semicolon (;).

    \b
    Examples:
    mutate -c 'A float'          # Convert column A to a float
    mutate -c 'C:F int'          # Convert C through F to an integer
    mutate -c 'J,N str; E bool'  # Convert J and N to a string 
                                 # and convert E to a boolean.
    '''
    table = context.obj['get_target']()

    mutations = map(lambda x: x.strip(), mutations.split(';'))
    
    if way == 'cast':
        for mutation in mutations:
            selection, datatype = mutation.split(' ')
            columns = selectify(list(table), selection)
            for column in columns:
                table[column] = cast(table[column], datatype)
    else:
        operations = {}
        for mutation in mutations:
            key_value = parse_key_value(mutation.strip())
            name = key_value['key']
            expression = key_value['value']
            operations.update({ name: expression })
        if way == 'row-wise':
            row_mutations = []
            for name, expression in operations.items():
                row_mutations.append(row_mutate(name, expression))
            table = pipe(table)(*row_mutations)
        else:
            if group_by_expression is not None:  
                groups = list(map(lambda x: x.strip(), group_by_expression.split(',')))
                table = pipe(table)(group_by(*groups)(mutate(**operations)))
            else:
                table = mutate(**operations)(table)
    
    context.obj['update_target'](table)
