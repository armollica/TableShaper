import pandas as pd
from tableshaper.helpers import parse_key_value

def grouped_aggregate(df, groups, column_name, expression):
    return df.groupby(groups).apply(lambda df: eval(expression, df.to_dict('series'))).reset_index().rename(columns = { 0: column_name })

def aggregate(df, group_by, aggregation):
    key_value = parse_key_value(aggregation.strip())
    name = key_value['key']
    expression = key_value['value']
    groups = map(lambda x: x.strip(), group_by.split(','))
    return grouped_aggregate(df, groups, name, expression)
