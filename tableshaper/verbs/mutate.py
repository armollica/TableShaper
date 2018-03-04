def mutate(**expressions):
    # Return generator of { name: assignment } dictionaries
    def assignments():
        for name, expression in expressions.iteritems():
            yield { name: lambda df: eval(expression, df.to_dict('series')) }
    
    # Refactor pandas assign() method as a function
    def assign(df, assignment):
        return df.assign(**assignment)
    
    # Chain assign() method calls, one for each assignment.
    # Perform grouping, if applicable.
    def process(df):

        def call_assignments(df):
            return reduce(assign, assignments(), df)

        if (hasattr(process, 'groups')):
            return (
                df.groupby(process.groups)
                  .apply(call_assignments)
                  .reset_index(drop = True)
            )
        else:
            return call_assignments(df)
    
    return process