# TableShaper

A command-line table processor. 

- <a href="#examples">Examples</a>
- <a href="#install">Install</a>
- <a href="#reference">Reference</a>
- <a href="#develop">Develop</a>
- <a href="#credits">Credits</a>

## Examples

Grab a subset of columns from a table.
```bash
tableshaper < table.csv choose 'country, continent, pop1990:pop2000`
```

Drop rows you don't need.
```bash
tableshaper < table.csv filter 'continent == "South America"'
```

Reshape the table.
```bash
tableshaper < table.csv reshape --gather -k year -v population --columns pop1990:pop2000
```

Do it all in one command.
```bash
tableshaper < table.csv \
  choose 'country, continent, pop1990:pop2000' \
  filter 'continent == "South America"' \
  reshaper --gather -k year -v population --columns pop1990:pop2000
```

## Install

Pull down this repo and install it with `pip`.
```bash
git pull https://github.com/armollica/tableshaper.git
pip install tableshaper/
```

## Reference

<table>
  <thead>
    <tr><th colspan="2">Table of contents</th></tr>
  </thead>
  <tbody>
    <tr><td><a href="#-tableshaper"><code>> tableshaper</code></a></td><td>Tidy Table program</td></tr>
    <tr><td><a href="#-tableshaper-choose"><code>> tableshaper choose</code></a></td><td>Subset columns.</td></tr>
    <tr><td><a href="#-tableshaper-rename"><code>> tableshaper rename</code></a></td><td>Rename columns.</td></tr>
    <tr><td><a href="#-tableshaper-filter"><code>> tableshaper filter</code></a></td><td>Subset rows.</td></tr>
    <tr><td><a href="#-tableshaper-arrange"><code>> tableshaper arrange</code></a></td><td>Sort rows.</td></tr>
    <tr><td><a href="#-tableshaper-mutate"><code>> tableshaper mutate</code></a></td><td>Create new columns.</td></tr>
    <tr><td><a href="#-tableshaper-aggregate"><code>> tableshaper aggregate</code></a></td><td>Aggregate rows.</td></tr>
    <tr><td><a href="#-tableshaper-join"><code>> tableshaper join</code></a></td><td>Join tables.</td></tr>
    <tr><td><a href="#-tableshaper-reshape"><code>> tableshaper reshape</code></a></td><td>Reshape table.</td></tr>
    <tr><td><a href="#-tableshaper-exec"><code>> tableshaper exec</code></a></td><td>Execute python code.</td></tr>
  <tbody>
</table>

<br/>

### `> tableshaper`

Entry to the program.

This command kicks off the program and is generally followed by a series of 
commands, like `choose`, `filter`, or `mutate`. Here you specify the input and
output file with the `-i, --input` and `-o, --output` arguments. By default, the
input will be `stdin` and the output will be `stdout`.

```bash
# Read CSV data from stdin and output to stdout ...
tableshaper < input.csv choose 'column1:column10' filter 'column1 > 20'

# ... or read and write to and from files
tableshaper -i input.csv -o output.csv choose 'column1:column10' filter 'column1 > 20'
```

The input file can be one of several formats. The default format is CSV,
comma-separated values. It can be explicitly set with the `-c, --csv` flag.
For tab-delimited files, use the `-t, --tsv` flag.

For JSON files, use the `--json` flag. A JSON file
can be formatted several ways and can be set with the `-f, --json-format`
argument:
- records: list like [{column -> value}, ... , {column -> value}]
- split: dict like {index -> [index], columns -> [columns], data -> [values]}
- index: dict like {index -> {column -> value}}
- columns: dict like {column -> {index -> value}}
- values: just the values array

The output file is always a CSV.

###### Command-line help
```
Usage: tableshaper [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

  Tidy Table

  A pipeline of transformations to tidy your tables

Options:
  -i, --input FILENAME            Input file or - for stdin.  [default: -]
  -o, --output FILENAME           Output file or - for stdout.  [default: -]
  -c, --csv                       Read input as CSV  [default: True]
  -t, --tsv                       Read input as TSV
  -j, --json                      Read input as JSON
  -f, --json-format [records|split|index|columns|values]
                                  JSON string format.  [default: records]
  -h, --help                      Show this message and exit.

Commands:
  aggregate  Aggregate rows.
  arrange    Sort rows.
  choose     Subset columns.
  exec       Execute python code.
  filter     Subset rows.
  join       Join tables.
  mutate     Create new columns.
  rename     Rename columns.
  reshape    Reshape table.
```

[↑ To table of contents](#reference)

<br/>

### `> tableshaper choose`

Subset columns.

There are two ways to choose columns, the "selection" method and the "filter"
method.

The "selection" method is the default method (the `-s, --selection` flag sets it
explicitly). With this method you give a comma-separated list of column names
or ranges of column names. A range is specified by the starting and ending
columns separated by a colon: `start:end`. You can exclude a column or a range
by putting a tilde (~) before it.

```bash
# Assume we have a table with columns A, B, C, etc.

# Keep columns A and D through G 
choose 'A, D:G'

# Drop columns C and F
choose '~C, ~F'

# Drop columns B through G, add column E back in
choose '~B:G, E`
```

The "filter" method is set with the `-f, --filter` flag. You provide a
Python expression that is evaluated on each column name. The column
name is loaded into the namespace as `name`. If the expression evaluates
to true then the column is kept.

```bash
# Keep columns that start with "population"
choose -f 'name.startswith("population")'

# Keep columns that are numeric
choose -f 'name.isnumeric()'
```

###### Command-line help
```
Usage: tableshaper choose [OPTIONS] EXPRESSION

  Subset columns.

  -f, --filter
  A python expression on each column name. If it evaluates to `True`
  then it's kept. The column name is loaded in as `name`.

  Examples:
  choose -f '"population" in name'

  -s, --selection (default)
  Provide a comma-separated list of column "selections".
  These can be single column names or sequential ranges of columns
  defined by the first and last column name of the sequence 
  separated by a colon. The tilde character (~) drops the selection.

  Examples:
  choose 'date, country, A, B, C, D'
  choose 'date, country, A:D'
  choose '~junk_column'
  choose '~junk_column_1:junk_column_20'

Options:
  -s, --selection  Selection-based choosing
  -f, --filter     Filter-based choosing
  -h, --help       Show this message and exit.
```

[↑ To table of contents](#reference)

<br/>

### `> tableshaper rename`

Rename columns.

There are two renaming methods. The default method is to provide a
comma-separated list of column name assignments of the form: new <- old.
All other columns are retained. You can explicitly set this method with
the `-a, --assign` flag.

```bash
# Rename GEOID to id and STATE_FIPS to fips.
rename 'id <- GEOID, fips <- STATE_FIPS'
```

The second method is to provide a Python expression that gets evaluated on each
column name. The column name is loaded into the namespace as `name`. Whatever
the expression evaluates to is what the new name will be. This method is set
with the `-m, --map` flag.

```bash
# Convert column names to lowercase
rename -m 'name.lower()'

# Convert column names to snakecase
rename -m 'name.replace(' ', '_').lower()'
```

####

###### Command-line help
```
Usage: tableshaper rename [OPTIONS] EXPRESSION

  Rename columns.

  -a, --assign (default)
  A comma-separated list of column names assignment, i.e.: new <- old

  Example:
  rename 'id <- GEOID, fips <- state_fips'

  -m, --map
  A python expression evaluated on each column name.
  The column name is loaded in as `name`.

  Example:
  rename -m 'name.upper()'
  rename -m 'name.strip().lower()'
  rename -m "'_'.join(name.split(' ')).strip().lower()"

Options:
  -a, --assign  assign-based renaming (default)
  -m, --map     map-based renaming
  -h, --help    Show this message and exit.
```

[↑ To table of contents](#reference)

<br/>

### `> tableshaper filter`

Subset rows.

Rows are kept based on a logical expression (true/false) or by a range of
row indices.

The default method is to keep rows based on a Python expression that evaluates
to true or false. The columns of the table are put into the namespace as a
pandas
[Series](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html)
object. This method can be set explicitly with the `-v, --vectorized` flag.

```bash
# Keep all rows where the population column has values greater than 1000
filter 'population > 1000'

# Keep all rows where the state column has values equal to "55" or "56"
filter 'state.isin(["55", "56"])'
```

The second filtering method is to specify a range of row indexes of the
format: `start:end`. This method is set with the `-s, --slice` flag.

```bash
# Keep the first five rows
filter -s 1:5

# Keep rows 25 through 75
filter -s 1:5
```

###### Command-line help
```
Usage: tableshaper filter [OPTIONS] EXPRESSION

  Subset rows.

  Rows are kept based on a logical expression (true/false) or by a range of
  row indices.

  -v, --vectorized (default)
  Rows are kept based on a python expression that evaluates to true or false.
  The columns of the table are put into the namespace a pandas series.

  Examples:
  filter 'population > 1000'
  filter 'state == "55"'
  filter 'state.isin(["55", "56"])'

  -s, --slice
  Specify a range of indices following this format: start:end

  Examples:
  filter -s 1:5
  filter -s 25:75

Options:
  -v, --vectorized  Vectorized filtering
  -s, --slice       Slice-based filtering
  -h, --help        Show this message and exit.
```

[↑ To table of contents](#reference)

<br/>

### `> tableshaper arrange`

###### Command-line help
```
Usage: tableshaper arrange [OPTIONS] COLUMNS

  Sort rows.

  Order is determined by values in a column (or columns).

  Examples:
  arrange 'mpg'
  arrange 'mpg:desc'
  arrange 'mpg, hp:desc'

Options:
  -h, --help  Show this message and exit.
```

[↑ To table of contents](#reference)

<br/>

### `> tableshaper mutate`

###### Command-line help
```
Usage: tableshaper mutate [OPTIONS] MUTATION

  Create new columns.

  A new column is created by assigning a new variable in a python
  expression. Mutation follow this format:

  new_column <- [python expression]

  Columns with the same name will be overwritten.

  -r, --row-wise
  Row-wise mutation. Each row is evaluated individually. This will often 
  be slower than vectorized mutation, but is more flexible in some cases.
  Grouped mutations are not possible; the --group-by option is ignored.
  Columns in the row are put in the namespace as an individual value. 

  Examples:
  mutate -r 'id <- "%05d" % id'
  mutate -r 'state <- id[0:2]'

  -v, --vectorized (default)
  Vector-based mutation. All columns of the table are put in the namespace
  as a pandas Series. Grouped mutations are possible with the --group-by
  option

  Examples:
  mutate 'real_value <- value * (price / 100)'
  mutate 'touches_lake_mi <- state.isin(['WI', 'MI'])'
  mutate --group-by state 'population_share <- pop / pop.sum()'

  -g, --group-by <columns>
  Comma-separated list of columns to group by. Only applies when 
  `-v, --vectorized` flag is active (which it is by default).

Options:
  -v, --vectorized     Vectorized transformation
  -r, --row-wise       Row-wise transformation
  -g, --group-by TEXT  Column(s) to group rows by
  -h, --help           Show this message and exit.
```

[↑ To table of contents](#reference)

<br/>

### `> tableshaper aggregate`

###### Command-line help
```
Usage: tableshaper aggregate [OPTIONS] AGGREGATION

  Aggregate rows.

  Group rows based on values in one or more columns and aggregate these
  groups of rows into single values using methods like sum(), mean(),
  count(), max(), min().

  Aggregations follow this format:

  new_column <- [python expression]

  -g, --group-by <columns>
  Comma-separated list of columns to group by.

  Examples:
  aggregate -g state 'population_sum <- population.sum()'
  aggregate -g country_id,station_id 'median_wind_speed <- wind_speed.median()'

Options:
  -g, --group-by TEXT
  -h, --help           Show this message and exit.
```

[↑ To table of contents](#reference)

<br/>

### `> tableshaper join`

###### Command-line help
```
Usage: tableshaper join [OPTIONS] [RIGHT]

  Join tables.

  SQL-style joins
  -l, --left
  -r, --right
  -o, --outer
  -i, --inner
  Join two tables based on common column values.

  Examples:
  join -k id right.csv
  join -r -k id right.csv
  join -o -k 'state_id, county_id' right.csv

  Bind columns or rows
  -r, --bind-rows
  -c, --bind-columns
  Bind rows or columns from two tables together.

  Examples:
  join -r right.csv
  join -c right.csv

  -k, --keys
  Column to join tables with. Only applies to SQL-style joins.

Options:
  -l, --left          Left join
  -r, --right         Right join
  -o, --outer         Outer join
  -i, --inner         Inner join
  -r, --bind-rows     Bind rows
  -c, --bind-columns  Bind columns
  -k, --keys TEXT     Columns to join tables on
  -h, --help          Show this message and exit.
```

[↑ To table of contents](#reference)

<br/>

### `> tableshaper reshape`

###### Command-line help
```
Usage: tableshaper reshape [OPTIONS]

  Reshape table.

  -g, --gather (default)
  Go from wide to long. Gather many columns into two key-value columns.

  Examples:
  reshape -k year -v population -c 1995:2013     
  
  -s, --spread
  Go from long to wide. Spread two key-value columns to multiple columns.

  Examples:
  reshape -s -k year -v population

Options:
  -g, --gather        Go from wide to long (default)
  -s, --spread        Go from long to wide
  -k, --key TEXT      Key column
  -v, --value TEXT    Value column
  -c, --columns TEXT  Selection of columns to be gathered
  -h, --help          Show this message and exit.
```

[↑ To table of contents](#reference)

<br/>

### `> tableshaper exec`

###### Command-line help
```
Usage: tableshaper exec [OPTIONS] EXPRESSION

  Execute python code.

  The table will be in the namespace as `d`. Any changes to the `d`
  dataframe will be passed on.

  Examples:
  exec 'd["pop_per_mil"] = d["pop"] / 1000000'
  is equivalent to...
  mutate 'pop_per_mil <- pop / 1000000'

Options:
  -h, --help  Show this message and exit.
```

[↑ To table of contents](#reference)

<br/>

## Develop

Pull down this repo and move into the directory.
```bash
git pull https://github.com/armollica/TableShaper.git
cd tableshaper/
```

Create a virtual environment and activate it.
```bash
virtualenv venv
. venv/bin/activate
```

Install the package and its dependencies with the `--editable` flag. That way
changes to the source code will automatically affect the CLI program.
```bash
pip install --editable .
```

## Credits

Much love to the people who made the [pandas](https://pandas.pydata.org/)
and [click](http://click.pocoo.org/5/) packages. This tool could have been a
pain to develop, but these two packages made it a breeze.

Also much love to the people behind these tools. You've saved me loads of time
and headache. Wouldn't have made this tool without you all.
- [tidyverse](https://www.tidyverse.org/): R packages that make cleaning data intuitive. I stole many ideas from the `dplyr` and `tidyr` packages, in particular. Love the micro domain-specific languages in these packages, each tailored for specific tasks.
- [mapshaper](https://github.com/mbloch/mapshaper/wiki/Command-Reference): A command-line tool for editing geographic data (vector-based). I mimicked the command-line interface of this in many ways, especially the command chaining. The viewer is also great.
- [csvkit](http://csvkit.rtfd.org/): Great tool for processing tabular data. Does many of the same things this tool does. Also does many thing this tool doesn't do, like pretty print and parse Excel files.
- [jq](https://stedolan.github.io/jq/): A command-line JSON processor. Really simple and powerful.
- [ndjson-cli](https://github.com/mbostock/ndjson-cli): A command-line tool for processing newline-delimited JSON files.