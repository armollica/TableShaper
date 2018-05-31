import click
import pandas as pd

@click.command('target')
@click.option('-d', '--duplicate', 'table', type=click.STRING,
              help = 'Duplicate table and make it the target.')
@click.argument('target', type=click.STRING)
@click.pass_context
def cli(context, table, target):
    '''
    Set the target table.

    Provide a table name and it will be set as the "target" table. Subsequent
    commands will be performed on the target table.

    \b
    Examples:
    target target_table_name

    \b
    -d, --duplicate
    Clone the specified table and make this clone the target. The option
    takes the name of the table to be cloned. You provide the name of the 
    new cloned table after that.

    \b
    Examples:
    filter -d old_table new_table
    '''
    if table:
        table = context.obj['tables'][table]
        clone = table.copy()
        context.obj['add_table'](target, clone)
    context.obj['set_target'](target)
