import click
import pandas as pd
from functools import update_wrapper

CONTEXT_SETTINGS = dict(help_option_names = ['-h', '--help'])

@click.group(chain=True, context_settings = CONTEXT_SETTINGS)
def cli():
    '''
    Tidy tables stored as CSV. Operations can be chained together.

    Example:
    \b
        TODO
    '''

@cli.resultcallback()
def process_commands(processors):
    '''
    This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    '''
    # Start with an empty iterable.
    stream = ()

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)

    # Evaluate the stream and throw away the items.
    for _ in stream:
        pass

def processor(f):
    '''
    Helper decorator to rewrite a function so that it returns another
    function from it.
    '''
    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)
        return processor
    return update_wrapper(new_func, f)

def generator(f):
    '''
    Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    '''
    @processor
    def new_func(stream, *args, **kwargs):
        for item in stream:
            yield item
        for item in f(*args, **kwargs):
            yield item
    return update_wrapper(new_func, f)



# -- 
# Input command

@cli.command('input')
@click.option('-j', '--json', is_flag = True,
              help = 'Read as JSON instead of CSV')
@click.option('--json-format', default = 'records',
              type = click.Choice(['records', 'split', 'index', 'columns', 'values']),
              help = 'JSON string format.',
              show_default = True)
@click.argument('path', type = click.Path())
@generator
def input_cmd(path, json, json_format):
    '''
    Read table.
    '''

    if path == '-':
        path_or_stream = click.get_text_stream('stdin')
    else:
        path_or_stream = path

    def read_df(path):
        if json:
            return pd.read_json(path_or_stream, orient = json_format)
        else:
            return pd.read_csv(path_or_stream)
    
    try:
        df = read_df(path)
        yield df
    except Exception as e:
        click.echo('Could not read CSV "%s": %s' % (filename, e), err = True)



# -- 
# Output command

@cli.command('output')
@click.option('-f', '--file', default='-', type=click.File('wb'),
              help = 'Filename for output CSV.',
              show_default = True)
@processor
def output_cmd(dfs, file):
    '''
    Write table.
    '''
    try:
        for df in dfs:
            df.to_csv(file, index = False)
            yield df
    except Exception as e:
        click.echo('Could not write csv "%s": %s' %
                    (file, e), err = True)



# -- 
# Choose command

@cli.command('choose')
@click.argument('columns', type = click.STRING)
@processor
def choose_cmd(dfs, columns):
    '''
    Subset columns. Provide a comma-separated list of column names.
    '''
    column_list = map(lambda x: x.strip(), columns.split(','))
    for df in dfs:
        df = df[column_list]
        yield df



# -- 
# Filter command

@cli.command('filter')
@click.argument('expression', type = click.STRING)
@processor
def filter_cmd(dfs, expression):
    '''
    Subset rows. Kept rows are determined by a logical expression composed of
    column values.
    '''
    for df in dfs:
        df.query(expression, inplace = True)
        yield df



# -- 
# Arrange command

@cli.command('arrange')
@click.argument('columns', type = click.STRING)
@processor
def arrange_cmd(dfs, columns):
    '''
    Sort rows. Order is determined by values in a column (or columns).
    '''
    column_list = []
    ascending_list = []
    for column in columns.split(','):
        column = column.strip()
        ascending = True
        if column.endswith(':desc'):
            ascending = False
            column = column[:-5]
        column_list.append(column)
        ascending_list.append(ascending)
    for df in dfs:
        df = df.sort_values(by = column_list, ascending = ascending_list)
        yield df



# -- 
# Mutate command

@cli.command('mutate')
@click.argument('expressions', type = click.STRING)
@processor
def mutate_cmd(dfs, expressions):
    '''
    Create new columns. New columns are created by assigning a new variable in
    a python expression.
    '''
    expressions_list = expressions.split(',')
    for df in dfs:
        for expression in expressions_list:
            df = df.eval(expression)
        yield df



# -- 
# Gather command
@cli.command('gather')
@click.option('-k', '--key', type = click.STRING, default = 'key',
              help = 'Name of column that contains past names of gathered columns')
@click.option('-v', '--value', type = click.STRING, default = 'value',
              help = 'Name of column that contains values of gathered columns')
@click.argument('columns', type = click.STRING)
@processor
def gather_cmd(dfs, key, value, columns):
    '''
    Gather many columns into two key-value columns.
    '''
    gather_column_list = map(lambda x: x.strip(), columns.split(','))
    for df in dfs:
        all_column_list = list(df)
        id_column_list = filter(lambda x: x not in gather_column_list, all_column_list)
        df = df.melt(id_vars = id_column_list,
                     value_vars = gather_column_list,
                     var_name = key,
                     value_name = value)
        yield df
