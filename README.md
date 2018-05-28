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
ts < table.csv pick 'country, continent, pop1990:pop2000`
```

Drop rows you don't need.
```bash
ts < table.csv filter 'continent == "South America"'
```

Reshape the table.
```bash
ts < table.csv reshape -k year -v population --columns pop1990:pop2000
```

Do it all in one command.
```bash
ts < table.csv \
  pick 'country, continent, pop1990:pop2000' \
  filter 'continent == "South America"' \
  reshape -k year -v population --columns pop1990:pop2000
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
    <tr><td><a href="#-ts"><code>$ ts</code></a></td><td>TableShaper program</td></tr>
    <tr><td><a href="#-ts-view"><code>$ ts view</code></a></td><td>View table.</td></tr>
    <tr><td><a href="#-ts-pick"><code>$ ts pick</code></a></td><td>Subset columns.</td></tr>
    <tr><td><a href="#-ts-rename"><code>$ ts rename</code></a></td><td>Rename columns.</td></tr>
    <tr><td><a href="#-ts-filter"><code>$ ts filter</code></a></td><td>Subset rows.</td></tr>
    <tr><td><a href="#-ts-sort"><code>$ ts sort</code></a></td><td>Sort rows.</td></tr>
    <tr><td><a href="#-ts-mutate"><code>$ ts mutate</code></a></td><td>Create new columns.</td></tr>
    <tr><td><a href="#-ts-aggregate"><code>$ ts aggregate</code></a></td><td>Aggregate rows.</td></tr>
    <tr><td><a href="#-ts-join"><code>$ ts join</code></a></td><td>Join tables.</td></tr>
    <tr><td><a href="#-ts-reshape"><code>$ ts reshape</code></a></td><td>Reshape table.</td></tr>
  <tbody>
</table>

<br/>

### `$ ts`

The TableShaper program.

`ts` command kicks off the program and is generally followed by a series of 
commands, like `pick`, `filter`, or `mutate`. Here you specify the input and
output file with the `-i, --input` and `-o, --output` arguments. By default, the
input will be `stdin` and the output will be `stdout`.

```bash
# Read CSV data from stdin, perform a few transformations and output to stdout
ts < input.csv pick 'column1:column10' filter 'column1 > 20'

# The same, but reading and writing from a file.
ts -i input.csv -o output.csv pick 'column1:column10' filter 'column1 > 20'
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

Data types for columns will be inferred automatically. To prevent this and
read everything in as strings, use the `-r, --raw` flag. You can then set
the data types explicitly in a `mutate` command.

The output file is always a CSV.

[↑ To table of contents](#reference)

<br/>

### `$ ts view`

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

### `$ ts pick`

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

### `$ ts rename`

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

### `$ ts filter`

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

### `$ ts sort`

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

### `$ ts mutate`

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

### `$ ts aggregate`

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

### `$ ts join`

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

### `$ ts reshape`

Reshape table.

There are two ways to reshape a table. The first is to go from wide to long.
The gather method takes a collection of columns and converts them
into two key-value columns.

This is the default method but can be set explicitly
with the `-g, --gather` flag. The name of the two key-value columns are
set with the `-k, --key` and `-v, --value` arguments. The columns to collect
are set with the `-c, --columns` argument which takes a *selection* of 
columns (see <a href="#-ts-pick"><code>$ ts pick</code></a> for an description
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

Test ares in the `tests/` folder. To run these, call `pytest` at the command
line from the root of this project.

## Credits

Many thanks to the people who made the [pandas](https://pandas.pydata.org/)
and [click](http://click.pocoo.org/5/) packages. This tool relies on these
immensely.

Also many thanks to the people behind these tools. You've saved me loads of time
and headache.
- [tidyverse](https://www.tidyverse.org/): R packages that make cleaning data intuitive. I stole many ideas from the `dplyr` and `tidyr` packages, in particular. Love the micro domain-specific languages in these packages, each tailored for specific tasks.
- [mapshaper](https://github.com/mbloch/mapshaper/wiki/Command-Reference): A command-line tool for editing geographic data (vector-based). I mimicked the command-line interface of this in many ways, especially the command chaining. The viewer is also great.
- [csvkit](http://csvkit.rtfd.org/): Great tool for processing tabular data. Does many of the same things this tool does. Also does many thing this tool doesn't do, like pretty print and parse Excel files.
- [visidata](http://visidata.org/): Tool to viewing and exploring tabular data at the command line.
- [jq](https://stedolan.github.io/jq/): A command-line JSON processor. Really simple and flexible.
- [ndjson-cli](https://github.com/mbostock/ndjson-cli): A command-line tool for processing newline-delimited JSON files.