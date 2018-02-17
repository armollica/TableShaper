import pandas as pd

def join(df, way, keys, right):
    if right == '-':
        right_df = pd.read_csv(click.get_text_stream('stdin'))
    else:
        right_df = pd.read_csv(right)
    
    if way == 'bind-rows':
        df = pd.concat([df, right_df])
    elif way == 'bind-columns':
        df = pd.concat([df, right_df], axis = 1)
    else:
        keys_list = map(lambda x: x.strip(), keys.split(','))
        df = df.merge(right_df, on = keys_list, how = way)
    
    return df
