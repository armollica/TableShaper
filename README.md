# TidyTable

## Commands

```
Usage: tt [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

  Tidy your tables

Options:
  -i, --input FILENAME            Input file.  [default: -]
  -o, --output FILENAME           Output file.  [default: -]
  -j, --json                      Read as JSON instead of CSV
  --json-format [records|split|index|columns|values]
                                  JSON string format.  [default: records]
  -h, --help                      Show this message and exit.

Commands:
  arrange  Sort rows.
  choose   Subset columns.
  exec     Execute python code.
  filter   Subset rows.
  gather   Reshape wide-to-long.
  join     Join tables.
  mutate   Create new columns.
  rename   Rename columns.
  spread   Reshape long-to-wide.
```

## Develop

Create a virtual environment and activate it.
```bash
virtualenv venv
. venv/bin/activate
```

Install the package and its dependencies. Use the `--editable` flag so that
changes to the source code will automatically affect the CLI program.
```bash
pip install --editable .
```
