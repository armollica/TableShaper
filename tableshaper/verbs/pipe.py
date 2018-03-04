def pipe(indata):
    
    # Data that will be processed through the pipeline
    class local:
        data = indata

    # Generator with instructions on how to process the pipeline
    def generate(functions):
        for function in functions:
            yield function(local.data)
    
    # Process the pipeline of functions
    def process(*functions):
        for d in generate(functions):
            local.data = d
        return local.data
    
    return process