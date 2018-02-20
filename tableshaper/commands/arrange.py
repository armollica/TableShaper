import pandas as pd

def arrange(df, columns):
    column_list = []
    ascending_list = []
    
    for column in columns.split(','):
        column = column.strip()
        ascending = True
        if column.endswith(':desc'):
            ascending = False
            column = column[:-5]
        column_list.append(column)
        ascending_list.append(ascending)
    
    return df.sort_values(by = column_list, ascending = ascending_list)
