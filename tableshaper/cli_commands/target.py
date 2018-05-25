import click
import pandas as pd

@click.command('target')
@click.argument('target', type=click.STRING)
@click.pass_context
def cli(context, target):
    '''
    Set the target table.
    '''
    context.obj['set_target'](target)
