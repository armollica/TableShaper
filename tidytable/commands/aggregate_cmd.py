import click
import pandas as pd
from tidytable.util import processor, aggregate, grouped_aggregate

@click.command('aggregate')
@click.option('-g', '--group-by', type = click.STRING)
@click.argument('aggregation', type = click.STRING)
@processor
def cli(dfs, group_by, aggregation):
    '''
    Aggregate rows.
    '''
    for df in dfs:
        [column_name, expression] = map(lambda x: x.strip(), aggregation.split('<-'))
        if group_by is not None:     
            groups = map(lambda x: x.strip(), group_by.split(','))
            df = grouped_aggregate(df, groups, column_name, expression)
        else:
            df = aggregate(df, column_name, expression)
        yield df
