def group_by(*names):
    def process(*operations):
        
        def operate(df, operation):
            operation.groups = names
            output = operation(df)
            operation.groups = None
            return output

        def collapse(df):
            return reduce(operate, operations, df)

        return collapse

    return process
