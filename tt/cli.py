import os
import sys
import click
import pandas as pd

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))

class CLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('_cmd.py'):
                rv.append(filename[0:-7])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('tt.commands.' + name + '_cmd',
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli

CONTEXT_SETTINGS = dict(help_option_names = ['-h', '--help'])

@click.group(cls = CLI, chain = True, context_settings = CONTEXT_SETTINGS)
def cli():
    """Tidy your tables.."""
    pass

@cli.resultcallback()
def process_commands(processors):
    '''
    This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    '''
    # Start with an empty iterable.
    stream = ()

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)

    # Evaluate the stream and throw away the items.
    for _ in stream:
        pass
