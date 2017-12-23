import click
import pandas as pd
from tidytable.util import processor, parse_key_value

def aggregate(df, column_name, expression):
    return df.apply(lambda df: eval(expression, df.to_dict('series'))).reset_index().rename(columns = { 0: column_name })

def grouped_aggregate(df, groups, column_name, expression):
    return df.groupby(groups).apply(lambda df: eval(expression, df.to_dict('series'))).reset_index().rename(columns = { 0: column_name })

@click.command('aggregate')
@click.option('-g', '--group-by', type = click.STRING)
@click.argument('aggregation', type = click.STRING)
@processor
def cli(dfs, group_by, aggregation):
    '''
    Aggregate rows.
    
    Group rows based on values in one or more columns and
    aggregate these groups of rows into single values using methods like
    sum(), mean(), count(), max(), min().

    Aggregations follow this format:

    new_column <- [python expression]

    \b
    -g, --group-by <columns>
    Comma-separated list of columns to group by.

    \b
    Examples:
    aggregate -g state 'population_sum <- population.sum()'
    aggregate -g country_id,station_id 'median_wind_speed <- wind_speed.median()'

    '''
    key_value = parse_key_value(aggregation.strip())
    name = key_value['key']
    expression = key_value['value']
    for df in dfs:
        if group_by is not None:     
            groups = map(lambda x: x.strip(), group_by.split(','))
            df = grouped_aggregate(df, groups, name, expression)
        else:
            df = aggregate(df, name, expression)
        yield df
