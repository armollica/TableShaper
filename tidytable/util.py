from functools import update_wrapper

def processor(f):
    '''
    Helper decorator to rewrite a function so that it returns another
    function from it.
    '''
    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)
        return processor
    return update_wrapper(new_func, f)

def generator(f):
    '''
    Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    '''
    @processor
    def new_func(stream, *args, **kwargs):
        for item in stream:
            yield item
        for item in f(*args, **kwargs):
            yield item
    return update_wrapper(new_func, f)

def selectify(string_list, selection_string):
    '''
    Perform subsetting and reordering on a list of strings
    in the vein of dplyr's select() function.
    '''
    # Character that identifies a set of columns should be excluded
    exclude_chr = '~'

    # Split and trim the selection "chunks"
    chunks = map(lambda x: x.strip(), selection_string.split(','))

    # If first selection chunk is an exclusion, start with all
    # keys included. Otherwise, state with none.
    if chunks[0].startswith(exclude_chr):
        selection = list(string_list)
    else:
        selection = []

    def add(key):
        if key not in string_list:
            raise ValueError('Column \'{}\' not in table'.format(key))
        if key in selection:
            selection.remove(key)
        selection.append(key)

    def remove(key):
        if key not in string_list:
            raise ValueError('Column \'{}\' not in table'.format(key))
        if key in selection:
            selection.remove(key)
    
    def key_range(chunk):
        x0, x1 = chunk.split(':')
        i0 = string_list.index(x0)
        i1 = string_list.index(x1)
        r = []
        for i in range(i0, i1 + 1):
            r.append(string_list[i])
        return r
    
    for chunk in chunks:
        if chunk.startswith(exclude_chr):
            if ':' in chunk:
                for key in key_range(chunk[1:]):
                    remove(key)
            else:
                remove(chunk[1:])
        else:
            if ':' in chunk:
                for key in key_range(chunk):
                    add(key)
            else:
                add(chunk)
    
    return selection
