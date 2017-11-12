import click
import re
import pandas as pd
from tidytable.util import processor

@click.command('rename')
@click.option('-m', '--map', 'map_expression', type = click.STRING)
@click.option('-a', '--assign', type = click.STRING)
@processor
def cli(dfs, assign, map_expression):
    '''
    Rename columns. Provide a comma-separated list of column names mappings, e.g., NEW <- OLD.
    '''
    for df in dfs:
        if map_expression is not None:
            df.columns = map(eval('lambda d: ' + map_expression), df.columns)
        if assign is not None:
            columns = dict()
            for chunk in assign.split(','):
                names = chunk.split('<-')
                columns[names[1].strip()] = names[0].strip()
            df = df.rename(columns = columns)
        yield df
