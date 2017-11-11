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
            mod = __import__('tidytable.commands.' + name + '_cmd',
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli

CONTEXT_SETTINGS = dict(help_option_names = ['-h', '--help'])

@click.group(cls = CLI, chain = True, invoke_without_command = True,
             context_settings = CONTEXT_SETTINGS)
@click.option('-i', '--input', 'infile', default = '-',
              type = click.File('rb'),
              help = 'Input file.',
              show_default = True)
@click.option('-o', '--output', 'outfile', default = '-',
              type = click.File('wb'),
              help = 'Output file.',
              show_default = True)
@click.option('-j', '--json', is_flag = True,
              help = 'Read as JSON instead of CSV')
@click.option('--json-format', default = 'records',
              type = click.Choice(['records', 'split', 'index', 'columns', 'values']),
              help = 'JSON string format.',
              show_default = True)
def cli(infile, outfile, json, json_format):
    """Tidy your tables"""
    pass

@cli.resultcallback()
def process_commands(processors, infile, outfile, json, json_format):
    '''
    This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    '''
    # Input the file
    def read_df(file):
        if json:
            return pd.read_json(file, orient = json_format)
        else:
            return pd.read_csv(file)
    
    try:
        df = read_df(infile)
    except Exception as e:
        click.echo('Could not read "%s": %s' % (infile, e), err = True)
    
    # Start with an iterable dataframe.
    stream = (df,)

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)
    
    # Output the file
    def output_cmd(dfs):
        try:
            for df in dfs:
                df.to_csv(outfile, index = False)
                yield df
        except Exception as e:
            click.echo('Could not write "%s": %s' %
                        (file, e), err = True)

    stream = output_cmd(stream)

    # Evaluate the stream and throw away the items.
    for _ in stream:
        pass
