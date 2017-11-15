import pandas as pd

d = pd.read_csv('retire-age-population.csv')

def mutate(df, column_name, expression):
    return df.assign(**{ column_name: lambda x: eval(expression, x.to_dict('series')) })

def grouped_mutate(df, groups, column_name, expression):
    def apply_func(df):
        return mutate(df, column_name, expression)
    return df.groupby(groups).apply(apply_func).reset_index(drop = True)

d = mutate(d, 'id', 'id.apply(lambda x: "%05d" % x)')
d = mutate(d, 'state', 'id.apply(lambda x: x[0:2])')
d = grouped_mutate(d, ['state'], 'pop_share', 'pop / pop.sum()')
d = grouped_mutate(d, ['state'], 'pop_shit', 'pop * pop_share / pop.mean()')
d = mutate(d, 'pop_shoot', 'pop * pop_share')

print d.head()
