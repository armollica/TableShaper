from tableshaper.helpers import evaluate, dataframe_to_dict

def sift(*expressions):
    def limit_rows(df, statement):
        return df[evaluate(statement, dataframe_to_dict(df))]
    return lambda df: reduce(limit_rows, expressions, df)
