# TidyTables

## Commands

```
Usage: tt [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

  Tidy tables stored as CSV. Operations can be chained together.

  Example:     TODO

Options:
  -h, --help  Show this message and exit.

Commands:
  arrange  Sort rows.
  choose   Subset columns.
  filter   Subset rows.
  gather   Gather many columns into two key-value...
  input    Read table.
  mutate   Create new columns.
  output   Write table.
```

#### tk
* `tt rename`: Rename columns (keeps all columns)
* `tt spread`: Convert two key-value column into multiple rows
* `tt join`: Join two tables based on common key values
* `tt group`: Group pandas table based on key values
* `tt summarize`: Aggregate rows
