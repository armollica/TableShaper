from pandas import merge
from functools import reduce
from tableshaper.helpers import evaluate, dataframe_to_dict

def aggregate(**expressions):
    
    def applications(groups):
        for name, expression in expressions.items():
            def process(df):
                return (
                    df.groupby(groups)
                        .apply(lambda df: evaluate(expression, dataframe_to_dict(df)))
                        .reset_index()
                        .rename(columns = { 0: name })
                )
            yield process

    def process(df):

        assert hasattr(process, 'groups')

        def merge(df0, df1):
            return merge(df0, df1, how = 'outer', on = process.groups)
        
        def apply_function(application):
            return application(df)
        
        dfs = map(apply_function, applications(list(process.groups)))

        return reduce(merge, dfs)
    
    return process
