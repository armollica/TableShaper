import os
import sys
import click
import pandas as pd

commands_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cli_commands'))

class CLI(click.MultiCommand): 
    
    def list_commands(self, ctx):
        commands = []
        for filename in os.listdir(commands_folder):
            if filename.endswith('.py') and not (filename == '__init__.py'):
                commands.append(filename[0:-3])
        commands.sort()
        return commands
    
    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            module_name = 'tableshaper.cli_commands.' + name
            import_list = ['cli']
            module = __import__(module_name, None, None, import_list)
        except ImportError:
            return
        return module.cli

CONTEXT_SETTINGS = dict(help_option_names = ['-h', '--help'])

@click.group(cls = CLI, chain = True, context_settings = CONTEXT_SETTINGS)
@click.pass_context        
def cli(context):
    '''
    TableShaper

    Get your tables into shape.
    '''
    context.obj = {}
    context.obj['tables'] = {}
    context.obj['target'] = None

    def add_table(name, table):
        context.obj['tables'].update({ name: table })

    def update_target(table):
        target = context.obj['target']
        context.obj['tables'].update({ target: table })

    def get_target():
        return context.obj['tables'][context.obj['target']]

    def set_target(x):
        context.obj['target'] = x

    context.obj['add_table'] = add_table
    context.obj['update_target'] = update_target
    context.obj['get_target'] = get_target
    context.obj['set_target'] = set_target


@cli.resultcallback()
@click.pass_context
def finish(context, processors):
    print context.obj['get_target']()