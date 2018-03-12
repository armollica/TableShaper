from tableshaper.helpers import evaluate

def sift(*expressions):
    def limit_rows(df, statement):
        return df[evaluate(statement, df.to_dict('series'))]
    return lambda df: reduce(limit_rows, expressions, df)
