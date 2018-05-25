import click
from tableshaper import sort

@click.command('sort')
@click.argument('columns', type = click.STRING)
@click.pass_context
def cli(context, columns):
    '''
    Sort rows.
    
    Order is determined by values in a column. Sort on multiple columns by
    passing in a comma-separated list of column names. Rows are sorted in
    ascending order, by default. To sort in descending order, put `:desc` after
    the column name.

    \b
    Examples:
    sort 'mpg'
    sort 'mpg:desc'
    sort 'mpg, hp:desc'

    '''
    table = context.obj['get_target']()

    column_list = map(lambda x: x.strip(), columns.split(','))
    table = sort(*column_list)(table)

    context.obj['update_target'](table)
