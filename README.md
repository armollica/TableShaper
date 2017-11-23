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

## Install

Pull down this repo and install it with `pip`.
```bash
git pull https://github.com/armollica/TidyTable.git
pip install TidyTable/
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
