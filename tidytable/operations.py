import pandas as pd
from tidytable.util import selectify

def row_mutate(df, column_name, expression):
    return df.assign(**{ column_name: lambda x: x.apply(lambda y: eval(expression, y.to_dict()), axis = 1)})

def column_mutate(df, column_name, expression):
    return df.assign(**{ column_name: lambda x: eval(expression, x.to_dict('series')) })

def column_mutate_grouped(df, groups, column_name, expression):
    def apply_func(df):
        return column_mutate(df, column_name, expression)
    return df.groupby(groups).apply(apply_func).reset_index(drop = True)

def aggregate(df, column_name, expression):
    return df.apply(lambda df: eval(expression, df.to_dict('series'))).reset_index().rename(columns = { 0: column_name })

def grouped_aggregate(df, groups, column_name, expression):
    return df.groupby(groups).apply(lambda df: eval(expression, df.to_dict('series'))).reset_index().rename(columns = { 0: column_name })

def gather(df, key, value, columns):
    all_column_list = list(df)
    gather_column_list = selectify(list(df), columns)
    id_column_list = filter(lambda x: x not in gather_column_list, all_column_list)
    return df.melt(id_vars = id_column_list,
                   value_vars = gather_column_list,
                   var_name = key,
                   value_name = value)

def spread(df, key, value):
    indexes = list(df.columns.drop(value))
    df = df.set_index(indexes).unstack(key).reset_index()
    df.columns = [i[1] if i[0] == value else i[0] for i in df.columns]
    return df
