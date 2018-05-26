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

# Make a str manipulating function cast the input as unicode first
def unicodeify(func):
    def unicodeified(string, *args, **kwargs):
        return func(unicode(string), *args, **kwargs)
    return unicodeified

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
parameterize = seriesify(unicodeify(inflection.parameterize))
pluralize = seriesify(inflection.pluralize)
singularize = seriesify(inflection.singularize)
tableize = seriesify(inflection.tableize)
titleize = seriesify(inflection.titleize)
transliterate = seriesify(unicodeify(inflection.transliterate))
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
# evaluate()
#
# Basically eval() but with some default functions loaded in
def evaluate(expression, globals_dict = {}, locals_dict = {}): 
    new_global_dicts = merge_dicts(eval_dict, globals_dict)
    return eval(expression, new_global_dicts, locals_dict)
