import click
import pandas as pd
from tableshaper import pipe, group_by, aggregate
from tableshaper.helpers import processor, parse_key_value

@click.command('aggregate')
@click.option('-g', '--group-by', 'group_by_expression', type = click.STRING)
@click.argument('aggregation', type = click.STRING)
@processor
def cli(dfs, group_by_expression, aggregation):
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
    groups = map(lambda x: x.strip(), group_by_expression.split(','))
    for df in dfs:
        yield pipe(df)(
            group_by(*groups)(
                aggregate(**{ name: expression })
            )
        )
