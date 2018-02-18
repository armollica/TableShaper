# Tidy Table

Command-line table processor. 

- <a href="#examples">Examples</a>
- <a href="#install">Install</a>
- <a href="#reference">Reference</a>
- <a href="#develop">Develop</a>
- <a href="#credits">Credits</a>

## Examples

Grab a subset of columns from a table.
```bash
tt < table.csv choose 'country, continent, pop1990:pop2000`
```

Drop rows you don't need.
```bash
tt < table.csv filter 'continent == "South America"'
```

Reshape the table.
```bash
tt < table.csv reshape --gather -k year -v population --columns pop1990:pop2000
```

Do it all in one command.
```bash
tt < table.csv \
  choose 'country, continent, pop1990:pop2000' \
  filter 'continent == "South America"' \
  reshaper --gather -k year -v population --columns pop1990:pop2000
```

## Install

Pull down this repo and install it with `pip`.
```bash
git pull https://github.com/armollica/TidyTable.git
pip install TidyTable/
```

## Reference

<table>
  <thead>
    <tr><th colspan="2">Table of contents</th></tr>
  </thead>
  <tbody>
    <tr><td><a href="#-tt"><code>> tt</code></a></td><td>Tidy Table program</td></tr>
    <tr><td><a href="#-tt-choose"><code>> tt choose</code></a></td><td>Subset columns.</td></tr>
    <tr><td><a href="#-tt-rename"><code>> tt rename</code></a></td><td>Rename columns.</td></tr>
    <tr><td><a href="#-tt-filter"><code>> tt filter</code></a></td><td>Subset rows.</td></tr>
    <tr><td><a href="#-tt-arrange"><code>> tt arrange</code></a></td><td>Sort rows.</td></tr>
    <tr><td><a href="#-tt-mutate"><code>> tt mutate</code></a></td><td>Create new columns.</td></tr>
    <tr><td><a href="#-tt-aggregate"><code>> tt aggregate</code></a></td><td>Aggregate rows.</td></tr>
    <tr><td><a href="#-tt-join"><code>> tt join</code></a></td><td>Join tables.</td></tr>
    <tr><td><a href="#-tt-reshape"><code>> tt reshape</code></a></td><td>Reshape table.</td></tr>
    <tr><td><a href="#-tt-exec"><code>> tt exec</code></a></td><td>Execute python code.</td></tr>
  <tbody>
</table>

<br/>

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

[↑ To table of contents](#reference)

<br/>

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

[↑ To table of contents](#reference)

<br/>

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

[↑ To table of contents](#reference)

<br/>

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

[↑ To table of contents](#reference)

<br/>

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

[↑ To table of contents](#reference)

<br/>

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

[↑ To table of contents](#reference)

<br/>

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

[↑ To table of contents](#reference)

<br/>

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

[↑ To table of contents](#reference)

<br/>

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

[↑ To table of contents](#reference)

<br/>

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

[↑ To table of contents](#reference)

<br/>

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