import click
from tableshaper import sift
from tableshaper.helpers import processor, evaluate

def row_sift(expression):
    def application(row):
        return evaluate(expression, row.to_dict())
    def compute(df):
        return df[df.apply(application, axis = 1)]
    return compute

@click.command('sift')
@click.option('-r', '--row', 'way', flag_value = 'row-wise',
              help = 'Row-wise sifting')
@click.option('-s', '--slice', 'way', flag_value = 'slice',
              help = 'Slice-based sifting')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Subset rows.
    
    Rows are kept based on a logical expression (true/false) or by a range of
    row indices.

    The default behavior is to keep rows based on a python expression that
    evaluates to true or false. The columns of the table are put into the
    namespace as a pandas series.

    \b
    Examples:
    sift 'population > 1000'
    sift 'state == "55"'
    sift 'state.isin(["55", "56"])'
    
    \b
    -r, --row
    Perform row-wise sifting. Each row is evaluated individually, not as a
    pandas series. This can be slower than vectorized sifting, but is more
    flexible in some cases. 

    \b
    Examples:
    sift -r 'population > 1000'
    sift -r 'state == "55"'
    sift -r 'state in ["55", "56"]'
    sift -r 're.match("^(M|m)azda", name) is not None'

    \b
    -s, --slice
    Perform slice-based sifting.

    Specify a range of indices following this format: start:end.
    It's a one-based index; the first row starts at one, not zero. Indexes are
    inclusive. The start row, the end row and all rows in-between will be
    included.

    \b
    Examples:
    sift -s 1:5
    sift -s 25:75
    
    Ranges can be open-ended. If no start index is provided, it starts from the
    first row. If no end index is provided, it ends at the last row of the
    table.
    
    \b
    Examples:
    sift -s :5    # is equivalent to 1:5
    sift -s 100:  # 100th to the last row

    You can start from the back of the table too. If the start or end
    index begins with a tilde (~), the index will refer to that many places
    from the last row of the table.

    \b
    Examples:
    sift -s ~5:      # last five rows
    sift -s ~10:~5:  # from (n - 10) to (n - 5)

    Provide multiple slices. Pass in a comma-separated list of slices and you'll
    get them back in that order. Warning: you can get duplicate rows this way.

    \b
    Examples:
    sift -s '1:5, 10:15'
    sift -s '1:5, ~5:'   # first and last five rows
    '''
    for df in dfs:
        if way == 'slice':
            expressions = map(lambda x: x.strip(), expression.split(','))
            indexes = []
            for expression in expressions:
                [start, end] = map(lambda x: x.strip(), expression.split(':'))

                if (start.startswith('~')):
                    # If it starts with tilde (~), index from the back of the table
                    start = len(df) - int(start.replace('~', ''))            
                elif (len(start) == 0):
                    # An empty "start" is equivalent to 1
                    start = 0
                else:
                    # Slice is a one-based index, df.loc[] is zero-based
                    start = int(start) - 1

                if (end.startswith('~')):
                    # If it starts with tilde (~), index from the back of the table
                    end = len(df) - int(end.replace('~', ''))
                elif (len(end) == 0):
                    # An empty "end" is equivalent to the end of the 
                    end = len(df)
                else:
                    end = int(end)
                
                indexes += range(start, end)

            yield df.iloc[indexes]
        elif way == 'row-wise':
            yield row_sift(expression)(df)
        else:
            yield sift(expression)(df)
