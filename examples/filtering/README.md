# Filtering rows

This example will walk through the various ways you can filter rows using Tableshaper.

We'll be filtering rows on this table (only the first four rows shown here).

| car                 |   mpg |   cyl |   hp |
|:--------------------|------:|------:|-----:|
| Mazda RX4           |  21   |     6 |  110 |
| Mazda RX4 Wag       |  21   |     6 |  110 |
| Datsun 710          |  22.8 |     4 |   93 |
| Hornet 4 Drive      |  21.4 |     6 |  110 |
| ...                 |   ... |   ... |  ... |

### Vectorized filtering

The default behavior of the filter command is to keep rows based whether a Python expression returns `True`. The columns of the table are put into the namespace as a Pandas series.

For example, if you wanted to only keep cars with 6 cylinders you would
run this command.

```bash
filter 'cyl == 6'
```

Which returns this.

| car            |   mpg |   cyl |   hp |
|:---------------|------:|------:|-----:|
| Mazda RX4      |  21   |     6 |  110 |
| Mazda RX4 Wag  |  21   |     6 |  110 |
| Hornet 4 Drive |  21.4 |     6 |  110 |
| Valiant        |  18.1 |     6 |  105 |
| Merc 280       |  19.2 |     6 |  123 |
| Merc 280C      |  17.8 |     6 |  123 |
| Ferrari Dino   |  19.7 |     6 |  175 |

### Row-wise filtering

Sometimes it's easier to work with individual values instead of Pandas series. You can use the `-r, --row` flag to enable row-wise filtering. This can be slower than the vectorized filtering you get with Pandas series. But it can be more flexible.

For example, if you wanted to keep all the Toyotas you could run this.

```bash
filter -r '"Toyota" in car'
```

Which give you this.

| car            |   mpg |   cyl |   hp |
|:---------------|------:|------:|-----:|
| Toyota Corolla |  33.9 |     4 |   65 |
| Toyota Corona  |  21.5 |     4 |   97 |

But for string matching like this you might want to use the built-in `text_matches(string, pattern)` function which works on series.

```bash
filter 'text_matches(car, "Toyota")'
```

This will return the same table as above.

### Slicing

Sometimes you know the specific rows you want to keep or remove. You can use slice-based filtering for this.

To do this you specify a range of indexes following this format: `start:end`. It's a one-based index. The first row starts at one, not zero. Indexes are inclusive. The start row, the end row and all rows in-between will be included.

If you want to keep just the first five rows you can do this.

```bash
filter -s 1:5
```

Ranges can be open-ended. If no start index is provided, it starts from the first row. If no end index is provided, it ends at the last row of the table.

```bash
filter -s :5    # is equivalent to 1:5
filter -s 100:  # 100th to the last row
```

You can start from the back of the table too. If the start or end index begins with a tilde (~), the index will refer to that many places from the last row of the table.

```bash
filter -s ~5:      # last five rows
filter -s ~10:~5:  # from (n - 10) to (n - 5)
```

Provide multiple slices. Pass in a comma-separated list of slices and you'll get them back in that order. Warning: you can get duplicate rows this way.

```bash
filter -s '1:5, 10:15'
filter -s '1:5, ~5:'   # first five rows and last five rows
```

### Distinct rows

You can drop duplicate rows using the `-d, --distinct` option.

You can provide a selection of columns on which to check to distinctness, or use `+` to look at all columns.

```bash
filter -d +    # Look at the whole table
filter -d A:C  # Look at columns A through C for distinctness
```