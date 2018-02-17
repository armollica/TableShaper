import click
from tidytable.helpers import processor
from tidytable.commands.aggregate import aggregate

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
    for df in dfs:
        yield aggregate(df, group_by, aggregation)

