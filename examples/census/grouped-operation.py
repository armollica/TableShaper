import pandas as pd

d = pd.read_csv('retire-age-population.csv')

d['id'] = d.apply(lambda x: '%04d' % x.id, axis = 1)
d['state'] = d.apply(lambda x: x.id[0:2], axis = 1)

expression = "pop / pop.sum()"

print d.groupby('state').apply(lambda df: df.assign(pop_share = lambda x: eval(expression, x.to_dict('series')))).reset_index(drop = True).head()