import click
from tableshaper import sift
from tableshaper.helpers import evaluate, selectify

def row_sift(expression):
    def application(row):
        return evaluate(expression, row.to_dict())
    def compute(df):
        return df[df.apply(application, axis = 1)]
    return compute

@click.command('filter')
@click.option('-r', '--row', 'way', flag_value = 'row-wise',
              help = 'Row-wise filtering')
@click.option('-s', '--slice', 'way', flag_value = 'slice',
              help = 'Slice-based filtering')
@click.option('-d', '--distinct', 'way', flag_value = 'distinct',
              help = 'Distinct rows. Provide selection or + for all columns.')
@click.argument('expression', type = click.STRING)
@click.pass_context
def cli(context, way, expression):
    '''
    Subset rows.
    
    Rows are kept based on a logical expression (true/false) or by a range of
    row indices.

    The default behavior is to keep rows based on a python expression that
    evaluates to true or false. The columns of the table are put into the
    namespace as a pandas series.

    \b
    Examples:
    filter 'population > 1000'
    filter 'state == "55"'
    filter 'state.isin(["55", "56"])'
    
    \b
    -r, --row
    Perform row-wise filtering. Each row is evaluated individually, not as a
    pandas series. This can be slower than vectorized filtering, but is more
    flexible in some cases. 

    \b
    Examples:
    filter -r 'population > 1000'
    filter -r 'state == "55"'
    filter -r 'state in ["55", "56"]'
    filter -r 're.match("^(M|m)azda", name) is not None'

    \b
    -s, --slice
    Perform slice-based filtering.

    Specify a range of indices following this format: start:end.
    It's a one-based index; the first row starts at one, not zero. Indexes are
    inclusive. The start row, the end row and all rows in-between will be
    included.

    \b
    Examples:
    filter -s 1:5
    filter -s 25:75
    
    Ranges can be open-ended. If no start index is provided, it starts from the
    first row. If no end index is provided, it ends at the last row of the
    table.
    
    \b
    Examples:
    filter -s :5    # is equivalent to 1:5
    filter -s 100:  # 100th to the last row

    You can start from the back of the table too. If the start or end
    index begins with a tilde (~), the index will refer to that many places
    from the last row of the table.

    \b
    Examples:
    filter -s ~5:      # last five rows
    filter -s ~10:~5:  # from (n - 10) to (n - 5)

    Provide multiple slices. Pass in a comma-separated list of slices and you'll
    get them back in that order. Warning: you can get duplicate rows this way.

    \b
    Examples:
    filter -s '1:5, 10:15'
    filter -s '1:5, ~5:'   # first and last five rows

    \b
    -d, --distinct
    Drop non-unique rows.

    You can provide a selection of columns on which to check to distinctness, or
    provide + which will look at all columns.

    \b
    Examples:
    filter -d +    # Look at the whole table
    filter -d A:C  # Look at columns A through C for distinctness
    '''
    table = context.obj['get_target']()
    
    if way == 'slice':
        expressions = map(lambda x: x.strip(), expression.split(','))
        indexes = []
        for expression in expressions:
            [start, end] = map(lambda x: x.strip(), expression.split(':'))

            if (start.startswith('~')):
                # If it starts with tilde (~), index from the back of the table
                start = len(table) - int(start.replace('~', ''))            
            elif (len(start) == 0):
                # An empty "start" is equivalent to 1
                start = 0
            else:
                # Slice is a one-based index, df.loc[] is zero-based
                start = int(start) - 1

            if (end.startswith('~')):
                # If it starts with tilde (~), index from the back of the table
                end = len(table) - int(end.replace('~', ''))
            elif (len(end) == 0):
                # An empty "end" is equivalent to the end of the 
                end = len(table)
            else:
                end = int(end)
            
            indexes += range(start, end)

        table = table.iloc[indexes]
    elif way == 'row-wise':
        table = row_sift(expression)(table)
    elif way == 'distinct':
        if expression == '+':
            subset = None
        else:
            subset = selectify(list(table), expression)
        table = table.drop_duplicates(subset)
    else:
        table = sift(expression)(table)
    
    context.obj['update_target'](table)
