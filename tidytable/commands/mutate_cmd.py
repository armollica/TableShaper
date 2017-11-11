import click
import pandas as pd
from tidytable.util import processor

@click.command('mutate')
@click.argument('expressions', type = click.STRING)
@processor
def cli(dfs, expressions):
    '''
    Create new columns. New columns are created by assigning a new variable in
    a python expression.
    '''
    expressions_list = expressions.split(',')
    for df in dfs:
        for expression in expressions_list:
            df = df.eval(expression)
        yield df