from tableshaper.helpers import invert_dictionary

def rename(**names):
    # Flip keyword arguments in dictionary:
    # rename(new_name = 'old_name') becomes { 'old_name': 'new_name' }
    columns = invert_dictionary(names)
    return lambda df: df.rename(columns = columns)