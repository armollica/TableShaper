from tableshaper.helpers import selectify

def choose(*names):
    expression = ','.join(names)
    def process(df):
        column_list = selectify(list(df), expression)
        return df[column_list]
    return process
