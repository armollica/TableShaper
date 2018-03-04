from tableshaper.helpers import selectify

def gather(key, value, columns):
    def process(df):
        all_column_list = list(df)
        gather_column_list = selectify(list(df), columns)
        id_column_list = filter(lambda x: x not in gather_column_list, all_column_list)
        return df.melt(id_vars = id_column_list,
                       value_vars = gather_column_list,
                       var_name = key,
                       value_name = value)
    return process
