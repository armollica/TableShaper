# TableShaper

A command-line table processor. 

- <a href="#examples">Examples</a>
- <a href="#install">Install</a>
- <a href="#reference">Reference</a>
- <a href="#develop">Develop</a>
- <a href="#credits">Credits</a>

## ❯ Examples

Grab a subset of columns from a table.
```bash
tableshaper input table.csv pick 'country, continent, pop1990:pop2000`
```

Drop rows you don't need.
```bash
tableshaper input table.csv filter 'continent == "South America"'
```

Reshape the table.
```bash
tableshaper input table.csv reshape -k year -v population --columns pop1990:pop2000
```

Do it all in one command.
```bash
tableshaper \
  input table.csv \
  pick 'country, continent, pop1990:pop2000' \
  filter 'continent == "South America"' \
  reshape -k year -v population --columns pop1990:pop2000
```

## ❯ Install

`tableshaper` is meant to be install with Python 3.7+.

Pull down this repo and install it with `pip`.
```bash
git clone https://github.com/armollica/tableshaper.git
pip install tableshaper/
```

## ❯ Reference

### `$ tableshaper`

The TableShaper program.

`tableshaper` command kicks off the program and is generally followed by a series of 
commands, like `pick`, `filter`, or `mutate`. The first command in you'll usually run
is the `input` command and the last command will usually be the `output` command.
These read and write tables. Here are some short example commands.

```bash
# Read CSV data from a file, perform some transformations and output to a new file.
tableshaper input input.csv pick 'column1:column10' filter 'column1 > 20' output output.csv

# Same thing, but reading from stdin and writing to stdout.
tableshaper input - pick 'column1:column10' filter 'column1 > 20' output - < input.csv > output.csv
```

For examples going forward, the `tableshaper` portion of commands will be omitted
to keep things concise.

<table>
  <thead>
    <tr><th colspan="2">Table of contents</th></tr>
  </thead>
  <tbody>
    <tr><td><a href="#-input"><code>$ input</code></a></td><td>Read in a table.</td></tr>
    <tr><td><a href="#-output"><code>$ output</code></a></td><td>Write out a table.</td></tr>
    <tr><td><a href="#-view"><code>$ view</code></a></td><td>View table.</td></tr>
    <tr><td><a href="#-pick"><code>$ pick</code></a></td><td>Subset columns.</td></tr>
    <tr><td><a href="#-rename"><code>$ rename</code></a></td><td>Rename columns.</td></tr>
    <tr><td><a href="#-filter"><code>$ filter</code></a></td><td>Subset rows.</td></tr>
    <tr><td><a href="#-sort"><code>$ sort</code></a></td><td>Sort rows.</td></tr>
    <tr><td><a href="#-mutate"><code>$ mutate</code></a></td><td>Create new columns.</td></tr>
    <tr><td><a href="#-aggregate"><code>$ aggregate</code></a></td><td>Aggregate rows.</td></tr>
    <tr><td><a href="#-join"><code>$ join</code></a></td><td>Join tables.</td></tr>
    <tr><td><a href="#-reshape"><code>$ reshape</code></a></td><td>Reshape table.</td></tr>
  <tbody>
</table>

<br/>

### `$ input`

Read in a table.

The `input` command requires a filename argument that points to the file you 
want to read. If you are reading from `stdin` pass `-` as the filename.

The input file can be one of several formats. An input file format is specified
with the `-f, --format` option.

The default format is CSV, comma-separated values. You can be explicitly set it
by passing `csv` to the format option.

For tab-limited files use the `tsv` format.

For all other delimited files use the `dsv` format. You specify the delimiter
with the `-d, --delim` option. For example, a semicolon-delimited file named
`input.txt` could be read like so: `input -f dsv -d ';' input.txt`.

Excel files can be read using the `excel` format. You'll need to specify the
sheet you want to read with the `-s, --sheet` option.

For JSON files, use the `--json` flag. A JSON file
can be formatted several ways. The JSON format can be set with
the `-j, --json-format` option:
- records: list like [{column -> value}, ... , {column -> value}]
- split: dict like {index -> [index], columns -> [columns], data -> [values]}
- index: dict like {index -> {column -> value}}
- columns: dict like {column -> {index -> value}}
- values: just the values array

Geographic data can also be imported as a table. GeoJSON, TopoJSON and
ESRI Shapefiles can all be imported as tables. (`tableshaper` uses [GeoPandas](http://geopandas.org)
for processing geodata). These formats have the following parameters: `geojson`,
`topojson` and `shp`.

Other supported formats are `feather`, `parquet`, `stata` and `sas`.

When you import a table, data types for columns will be inferred automatically.
To prevent this and read everything in as text, use the `-r, --raw` flag.
You can then set the data types explicitly in a `mutate` command.

If you are reading a file without a header row, you can set column names with 
the `-c, --col-names` option. This takes a comma-separated list of column names.

Multiple tables can be imported by calling the `input` command mulitple times.
This useful for when you want to join tables.

You can specify the name of the table to be imported using the `-n, --name`
option. This is useful for when working with tables and need to reference
one. If you don't give a table a name, it will automatically be given one based
on the filename. If a table is coming from `stdin`, it will be given the name
`table`.

[↑ To table of contents](#reference)

<br/>

### `$ output`

Write out a table.

The `output` command requires a filename argument specifying where to write the
file. If you want to output to `stdout` pass `-` as the filename.

To output multiple tables pass `+` as the filename. You must also provide a 
comma-separated list of table names to the `-t, --tables` option.

You can specify the directory you want files to be put in using the `-d, --dir`
option.

You can output a table in a variety of format:
- `csv` or `tsv` for comma- or tab-delimited files
- `json` for a records-style JSON files (see [input](#-input))
- `geojson` or `shp` for GeoJSON and ESRI Shapefiles (for geodata)
- `feather` or `parquet` for efficient binary data formats
- `markdown` or `html` for display on in a markdown file or on webpage

[↑ To table of contents](#reference)

<br/>

### `$ view`

View table.

Display table in a human-readable format. Or print summary information
about the table.

Calling `view` by itself will print the first and last 30 rows of the table.

You can limit what's display to the top `n` rows with the `-n, --top` option.
```bash
view -n 5  # show the top 5 rows
```

Use the `-i, --info` flag to display a summary of the table. This includes the
number of rows and columns as well as each column's name, its data type and the
number of non-null values it has. Also displays the memory usage of the table.

Use the `-s, --stats` flag to display summary statistics on the columns in the
table.

For numbers this will includes the count, mean, standard deviation, minimum,
maximum, 25th percentile, median and 75th percentile.

For strings and timestamps it will include the count, the number of unique
values, the most common value and the number of times it occurs.
Timestamps also include the first and last items.

[↑ To table of contents](#reference)

<br/>

### `$ pick`

Subset columns.

There are two ways to pick columns, the "selection" method and the "filter"
method.

The "selection" method is the default method. With this method you give a
comma-separated list of column names or ranges of column names. A range is
specified by the starting and ending columns separated by a colon: `start:end`.
You can exclude a column or a range by putting a tilde (~) before it.

```bash
# Assume we have a table with columns A, B, C, etc.

# Keep columns A and D through G 
pick 'A, D:G'

# Drop columns C and F
pick '~C, ~F'

# Drop columns B through G, add column E back in
pick '~B:G, E`
```

The "filter" method is set with the `-f, --filter` flag. You provide a
Python expression that is evaluated on each column name. The column
name is loaded into the namespace as `name`. If the expression evaluates
to true then the column is kept.

```bash
# Keep columns that start with "population"
pick -s 'name.startswith("population")'

# Keep columns that are numeric
pick -s 'name.isnumeric()'
```

[↑ To table of contents](#reference)

<br/>

### `$ rename`

Rename columns.

There are two renaming methods. The default method is to provide a
comma-separated list of column name assignments of the form: new = old.
All other columns are retained.

```bash
# Rename GEOID to id and STATE_FIPS to fips.
rename 'id = GEOID, fips = STATE_FIPS'
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

[↑ To table of contents](#reference)

<br/>

### `$ filter`

Subset rows.

Rows are kept based on a logical expression (true/false) or by a range of
row indices.

The default method is to keep rows based on a Python expression that evaluates
to true or false. The columns of the table are put into the namespace as a
pandas
[Series](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html)
object.

```bash
# Keep all rows where the population column has values greater than 1000
filter 'population > 1000'

# Keep all rows where the state column has values equal to "55" or "56"
filter 'state.isin(["55", "56"])'
```

If you use the `-r, --row` flag, you can perform the same type of filtering
on rows individually, instead of on pandas Series as a whole. This can be more
flexible, especially when dealing with strings.

```bash
filter -r 'state in ["55", "56"]'
filter -r 're.match("^(M|m)azda", name) is not None'
```

The second filtering method is to specify a range of row indexes of the
format: `start:end`. This method is set with the `-s, --slice` flag.

```bash
# Keep the first five rows
filter -s 1:5

# Keep rows 25 through 75
filter -s 1:5
```

Ranges can be open-ended. If no start index is provided, it starts from
the first row. If no end index is provided, it ends at the last row of the
table.

```bash
filter -s :5    # is equivalent to 1:5
filter -s 100:  # 100th to the last row
```
You can start from the back of the table too. If the start or end index
begins with a tilde (~), the index will refer to that many places from the
last row of the table.

```bash
filter -s ~5:      # last five rows
filter -s ~10:~5:  # from (n - 10) to (n - 5)
```

Provide multiple slices. Pass in a comma-separated list of slices and
you'll get them back in that order. Warning: you can get duplicate rows
this way.

```bash
filter -s '1:5, 10:15'
filter -s '1:5, ~5:'   # first and last five rows
```

[↑ To table of contents](#reference)

<br/>

### `$ sort`

Sort rows.

Order is determined by values in a column. Sort on multiple columns by passing
in a comma-separated list of column names. Rows are sorted in ascending order,
by default. To sort in descending order, put `:desc` after the column name.

```bash
sort 'mpg'
sort 'mpg:desc'
sort 'mpg, hp:desc'
```

[↑ To table of contents](#reference)

<br/>

### `$ mutate`

Create new columns.

A new column is created by assigning a new variable in a python
expression. Mutation follow this format:

new_column = [python expression]

Columns with the same name will be overwritten.

The default behavior is to perform vectorized transformation. All columns of the
table are put in the namespace as a pandas Series.

```bash
mutate 'real_value = value * (price / 100)'
mutate 'touches_lake_mi = state.isin(["WI", "MI"])'
```

Multiple mutations can be made in one go by separating mutations with a
semicolon (;). The order of these mutations is not guaranteed to be consistent
with the order to provided them. Run separate `mutate` commands if the order
matters.

```bash
mutate 'price = price / 100; pop = pop * 1000'
```

Grouped mutations are possible with the `-g, --group-by` option. Pass a
comma-separated list of column names to group by multiple columns.

Grouped mutations are like aggregations except all original rows are preserved.

```bash
mutate -g state 'population_share = pop / pop.sum()'
```

Some operations like string manipulation can be difficult to deal with when
dealing with pandas Series objects. In these cases you way want to perform
row-based mutations.

Activate row-wise mutation with the `-r, --row` flag. Columns in the row are
put in the namespace as individual values.

Grouped mutations are not possible with row-wise mutation.

```bash
mutate -r 'id = "%05d" % id'
mutate -r 'state = id[0:2]'
```

[↑ To table of contents](#reference)

<br/>

### `$ aggregate`

Aggregate rows.

Group rows based on values in one or more columns and aggregate these
groups of rows into single values using methods like sum(), mean(),
count(), max(), min().

Aggregations follow this format:

new_column = [python expression]

-g, --group-by <columns>
Comma-separated list of columns to group by.

```bash
aggregate -g state 'population_sum = population.sum()'
aggregate -g country_id,station_id 'median_wind_speed = wind_speed.median()'
```

[↑ To table of contents](#reference)

<br/>

### `$ join`

Join tables.

Perform SQL-style joins with the following flags:
- Left join: `-l, --left` (default)
- Right join: `-r, --right`
- Outer join: `-o, --outer`
- Inner join: `-i, --inner`

Pass the columns to join to the `-k, --key` argument.

```bash
join -k id right.csv
join -r -k id right.csv
join -o -k 'state_id, county_id' right.csv
```

You can also bind rows or columns from two tables together with the
`--bind-rows` and `--bind-columns` flags.

```bash
join --bind-rows right.csv
join --bind-columns right.csv
```

When binding rows, any columns that exist in one table and not the other will
be filled with `NaN` values for rows in the table without that column.

[↑ To table of contents](#reference)

<br/>

### `$ reshape`

Reshape table.

There are two ways to reshape a table. The first is to go from wide to long.
The gather method takes a collection of columns and converts them
into two key-value columns.

This is the default method but can be set explicitly
with the `-g, --gather` flag. The name of the two key-value columns are
set with the `-k, --key` and `-v, --value` arguments. The columns to collect
are set with the `-c, --columns` argument which takes a *selection* of 
columns (see <a href="#-pick"><code>$ pick</code></a> for an description
of *selections*).

```bash
reshape -k year -v population -c 1995:2013
```
The second method is to go from long to wide. The spread method (set with the
`-s, --spread` flag) takes two key-value columns and spreads them out into
multiple columns where the key column is converted into the column name
and the rows are filled with the values in the *value* columns. The key-value
columns names are passed to the `-k, --key` and `-v, --value` arguments.

```bash
reshape -s -k year -v population
```

[↑ To table of contents](#reference)

<br/>

## ❯ Develop

Pull down this repo and move into the directory.
```bash
git pull https://github.com/armollica/tableshaper.git
cd tableshaper/
```

Create a virtual environment and activate it.
```bash
python -m venv venv
. venv/bin/activate
```

Install the package and its dependencies with the `--editable` flag. That way
changes to the source code will automatically affect the CLI program.
```bash
pip install --editable .
```

Test ares in the `tests/` folder. To run these, call `pytest` at the command
line from the root of this project.

## ❯ Credits

Many thanks to the people who made the [pandas](https://pandas.pydata.org/)
and [click](http://click.pocoo.org/5/) packages. This tool relies on these
immensely.

Also many thanks to the people behind these tools. You've saved me loads of time
and headache.
- [tidyverse](https://www.tidyverse.org/): I stole many ideas from the `dplyr` and `tidyr` R packages, in particular. Love the micro domain-specific languages in these packages, each tailored for specific tasks.
- [mapshaper](https://github.com/mbloch/mapshaper/wiki/Command-Reference): A command-line tool for editing geographic data (vector-based). I mimicked the command-line interface of this in many ways, especially the command chaining. The viewer is also great.
- [csvkit](http://csvkit.rtfd.org/): Great tool for processing tabular data. Does many of the same things tableshaper does. Also does many thing this tool doesn't do.
- [visidata](http://visidata.org/): Tool to viewing and exploring tabular data at the command line.
- [jq](https://stedolan.github.io/jq/): A command-line JSON processor.
- [ndjson-cli](https://github.com/mbostock/ndjson-cli): A command-line tool for processing newline-delimited JSON files.
