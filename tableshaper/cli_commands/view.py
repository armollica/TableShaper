import click
import pandas as pd

@click.command('view')
@click.option('-a', '--all', is_flag=True,
              help = 'Display info on all tables')
@click.option('-i', '--info', 'way', flag_value='info',
              help = 'Display info on a table',
              default=True)
@click.option('-s', '--stats', 'way', flag_value='stats',
              help = 'Display summary stats on the columns')
@click.option('-t', '--tables', 'way', flag_value='tables',
              help = 'Display table names')
@click.pass_context
def cli(context, all, way):
    '''
    View info on tables.
    '''
    context.obj['printed'] = True
    target = context.obj['target']
    tables = context.obj['tables']

    def view(key):
        table = tables[key]
        if way == 'info':
            click.echo('')
            click.echo('{table}:'.format(table=key))
            table.info(verbose=True, null_counts=True)
            click.echo('')
        elif way == 'stats':
            click.echo('')
            click.echo('{table}:'.format(table=key))
            with pd.option_context('display.max_rows', None):
                click.echo(table.describe(include='all').transpose())
            click.echo('')
    
    if way == 'tables':
        click.echo('')
        click.echo('Available tables:')
        for key in tables:
            is_active = target == key
            active = ''
            if is_active:
                active = '[target]'
            click.echo('{table} {active}'.format(table=key, active=active))
        click.echo('')
    elif all:
        for key in tables:
            view(key)
    else:
        view(target)
            
        
    