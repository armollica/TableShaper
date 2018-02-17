# Tidy Table

Command-line table processor.  A pipeline of transformations to tidy tabular
data.

- <a href="#install">Install</a>
- <a href="#reference">Reference</a>
- <a href="#develop">Develop</a>

## Install

Pull down this repo and install it with `pip`.
```bash
git pull https://github.com/armollica/TidyTable.git
pip install TidyTable/
```

## Reference

- <a href="#-tt">`tt`</a>: Tidy Table program
- <a href="#-tt-choose">`tt choose`</a>: Subset columns.
- <a href="#-tt-rename">`tt rename`</a>: Rename columns.
- <a href="#-tt-filter">`tt filter`</a>: Subset rows.
- <a href="#-tt-arrange">`tt arrange`</a>: Sort rows.
- <a href="#-tt-mutate">`tt mutate`</a>: Create new columns.
- <a href="#-tt-aggregate">`tt aggregate`</a>: Aggregate rows.
- <a href="#-tt-join">`tt join`</a>: Join tables.
- <a href="#-tt-reshape">`tt reshape`</a>: Reshape table.
- <a href="#-tt-exec">`tt exec`</a>: Execute python code.

### `> tt`

This is the entry to the program. It is nearly always followed by a series of 
commands, like `choose`, `filter`, or `mutate`.

It's at this entry point that you specify the input and output file with
the `-i, --input` and `-o, --output` arguments. By default, the input
will be `stdin` and the output will be `stdout`.

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
Usage: tt [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

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

### `> tt choose`
```
Usage: tt choose [OPTIONS] EXPRESSION

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

### `> tt rename`

```
Usage: tt rename [OPTIONS] EXPRESSION

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

### `> tt filter`

```
Usage: tt filter [OPTIONS] EXPRESSION

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

### `> tt arrange`

```
Usage: tt arrange [OPTIONS] COLUMNS

  Sort rows.

  Order is determined by values in a column (or columns).

  Examples:
  arrange 'mpg'
  arrange 'mpg:desc'
  arrange 'mpg, hp:desc'

Options:
  -h, --help  Show this message and exit.
```

### `> tt mutate`

```
Usage: tt mutate [OPTIONS] MUTATION

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

### `> tt aggregate`

```
Usage: tt aggregate [OPTIONS] AGGREGATION

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

### `> tt join`

```
Usage: tt join [OPTIONS] [RIGHT]

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

### `> tt reshape`

```
Usage: tt reshape [OPTIONS]

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

### `> tt exec`

```
Usage: tt exec [OPTIONS] EXPRESSION

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

## Develop

Pull down this repo and move into the directory.
```bash
git pull https://github.com/armollica/TidyTable.git
cd TidyTable/
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