import click
import pandas as pd
from tidytable.util import processor, mutate, grouped_mutate

@click.command('mutate')
@click.option('-g', '--group-by', type = click.STRING)
@click.argument('mutation', type = click.STRING)
@processor
def cli(dfs, group_by, mutation):
    '''
    Create new columns. New columns are created by assigning a new variable in
    a python expression.
    '''
    for df in dfs:
        [column_name, expression] = map(lambda x: x.strip(), mutation.split('<-'))
        if group_by is not None:     
            groups = map(lambda x: x.strip(), group_by.split(','))
            df = grouped_mutate(df, groups, column_name, expression)
        else:
            df = mutate(df, column_name, expression)
        yield df
