import re, datetime, inflection
import pandas as pd

def merge_dicts(a, b):
    output = a.copy()
    output.update(b)
    return output

# Make a simple function accept a Pandas Series as input 
def seriesify(func):
    def seriesified(series, *args, **kwargs):
        if isinstance(series, pd.Series):
            return series.apply(lambda x: func(x, *args, **kwargs))
        return func(series, *args, **kwargs)
    return seriesified

# ______________________________________________________________________________
# Functions that will be usable in evaluate() contexts
eval_dict = {}

# ______________________________________________________________________________
# Inflection-based functions
camelize = seriesify(inflection.camelize)
dasherize = seriesify(inflection.dasherize)
humanize = seriesify(inflection.humanize)
ordinal = seriesify(inflection.ordinal)
ordinalize = seriesify(inflection.ordinalize)
parameterize = seriesify(inflection.parameterize)
pluralize = seriesify(inflection.pluralize)
singularize = seriesify(inflection.singularize)
tableize = seriesify(inflection.tableize)
titleize = seriesify(inflection.titleize)
transliterate = seriesify(inflection.transliterate)
underscore = seriesify(inflection.underscore)

eval_dict.update({
    'camelize': camelize,
    'dasherize': dasherize,
    'humanize': humanize,
    'ordinalize': ordinalize,
    'ordinal': ordinal,
    'parameterize': parameterize,
    'pluralize': pluralize,
    'singularize': singularize,
    'tableize': tableize,
    'titleize': titleize,
    'transliterate': transliterate,
    'underscore': underscore
})

# ______________________________________________________________________________
# Regex functions

def extract_text(string, regex):
    match = re.search(regex, string)
    if match:
        return match.group(1)
    return None

def text_matches(string, regex):
    match = re.search(regex, string)
    if match:
        return True
    return False

def starts_with(string, starter):
    return text_matches(string, r'^{}'.format(starter))

def ends_with(string, ender):
    return text_matches(string, r'{}$'.format(ender))

eval_dict.update({
    'extract_text': seriesify(extract_text),
    'text_matches': seriesify(text_matches),
    'starts_with': seriesify(starts_with),
    'ends_with': seriesify(ends_with)
})

# ______________________________________________________________________________
# Parsing functions (string -> another data type)

def parse_datetime(string, format_string):
    return datetime.datetime.strptime(string, format_string)

def parse_int(string):
    return int(string)

def parse_float(string):
    return float(string)

def parse_bool(string):
    return string.lower() in ['true', '1', 't', 'y', 'yes']

eval_dict.update({
    'parse_datetime': seriesify(parse_datetime),
    'parse_int': seriesify(parse_int),
    'parse_float': seriesify(parse_float),
    'parse_bool': seriesify(parse_bool)
})

# ______________________________________________________________________________
# format_text()

def get_format_text(namespace):
    def format_text(string):
        return string.format(**namespace)
    return format_text

# ______________________________________________________________________________
# evaluate()
#
# Basically eval() but with some default functions loaded in
def evaluate(expression, globals_dict = {}, locals_dict = {}): 
    new_global_dicts = merge_dicts(eval_dict, globals_dict)
    
    # Add format_text() function (requires namespace)
    format_namespace = merge_dicts(new_global_dicts, locals_dict)
    format_text = get_format_text(format_namespace)
    new_global_dicts.update({ 'format_text': format_text })

    return eval(expression, new_global_dicts, locals_dict)
