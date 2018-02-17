import pandas as pd

def filter_dataframe(df, way, expression):
    if way == 'slice':
        [start, end] = map(lambda x: int(x.strip()), expression.split(':'))
        df = df.iloc[start:end]
    elif way == 'vectorized':
        df = df[eval(expression, df.to_dict('series'))]
    return df
