import click
import re
import pandas as pd
import inflection
from tidytable.util import processor

sanitizers = {
    'snake-case': inflection.underscore,
    'camel-case': inflection.camelize,
    'humanize': inflection.humanize,
    'titleize': inflection.titleize
}

@click.command('rename')
@click.option('-f', '--find', type = click.STRING)
@click.option('-r', '--replace', type = click.STRING)
@click.option('-s', '--sanitize',
              type = click.Choice(['snake-case', 'camel-case', 'humanize', 'titleize']))
@click.option('-m', '--mapping', type = click.STRING)
@processor
def cli(dfs, find, replace, sanitize, mapping):
    '''
    Rename columns. Provide a comma-separated list of column names mappings, e.g., NEW = OLD.
    '''
    for df in dfs:
        if (find is not None) and (replace is not None):
            df.columns = map(lambda column: re.sub(find, replace, column), df.columns)

        if sanitize is not None:
            sanitizer = sanitizers[sanitize]
            df.columns = map(lambda column: sanitizer(column), df.columns)
        
        if mapping is not None:
            columns = dict()
            for chunk in mapping.split(','):
                names = chunk.split('=')
                columns[names[1].strip()] = names[0].strip()
            df = df.rename(columns = columns)
        
        yield df
