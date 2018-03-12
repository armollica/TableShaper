import click
import pandas as pd
from tableshaper.helpers import processor

@click.command('exec')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, expression):
    '''
    Execute python code.
    
    The table will be in the namespace as `d`. Any
    changes to the `d` dataframe will be passed on.

    \b
    Examples:
    exec 'd["pop_per_mil"] = d["pop"] / 1000000'
    is equivalent to...
    mutate 'pop_per_mil = pop / 1000000'
    '''
    for d in dfs:
        exec(expression)
        yield d
