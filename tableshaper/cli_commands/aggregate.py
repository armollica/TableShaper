import click
import pandas as pd
from tableshaper import pipe, group_by, aggregate
from tableshaper.helpers import parse_key_value

@click.command('aggregate')
@click.option('-g', '--group-by', 'group_by_expression', type = click.STRING)
@click.argument('aggregation', type = click.STRING)
@click.pass_context
def cli(context, group_by_expression, aggregation):
    '''
    Aggregate rows.
    
    Group rows based on values in one or more columns and
    aggregate these groups of rows into single values using methods like
    sum(), mean(), count(), max(), min().

    Aggregations follow this format:

    name = expression

    Multiple mutations can be done at once. Mutations are separated
    by a semicolon like this:

    name = [expression]; name = expression; and so on ...

    \b
    -g, --group-by <columns>
    Comma-separated list of columns to group by.

    \b
    Examples:
    aggregate -g state 'population_sum = population.sum()'
    aggregate -g country_id,station_id 'median_wind_speed = wind_speed.median()'

    '''
    table = context.obj['get_target']()

    key_value = parse_key_value(aggregation.strip())
    name = key_value['key']
    expression = key_value['value']
    groups = list(map(lambda x: x.strip(), group_by_expression.split(',')))
    table = pipe(table)(group_by(*groups)(aggregate(**{name: expression})))
    
    context.obj['update_target'](table)
