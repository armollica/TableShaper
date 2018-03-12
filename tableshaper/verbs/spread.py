def spread(key, value):
    def process(df):
        indexes = list(df.columns.drop(value))
        df = df.set_index(indexes).unstack(key).reset_index()
        df.columns = [i[1] if i[0] == value else i[0] for i in df.columns]
        return df
    return process
