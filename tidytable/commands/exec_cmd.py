import click
import pandas as pd
from tidytable.util import processor

@click.command('exec')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, expression):
    '''
    Execute python code. The table will be in the name space as `d`.
    '''
    for d in dfs:
        exec(expression)
        yield d
