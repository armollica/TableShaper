# Renaming columns

This example will walk through the various ways you can rename columns using Tableshaper.

We'll be renaming columns on this table (only the first four rows shown here).

| car                 |   mpg |   cyl |   hp |
|:--------------------|------:|------:|-----:|
| Mazda RX4           |  21   |     6 |  110 |
| Mazda RX4 Wag       |  21   |     6 |  110 |
| Datsun 710          |  22.8 |     4 |   93 |
| Hornet 4 Drive      |  21.4 |     6 |  110 |
| ...                 |   ... |   ... |  ... |

### Assigning new names

The most common method for renaming columns is to provide a comma-separated list of name assignments that follow this format: `<New name> = <Old name>`.

For example if we wanted to give the columns more descriptive names we could do this.

```
rename 'car_name = car, miles_per_gallon = mpg, cylinders = cyl, horse_power = hp'
```

This is what you'll get.

| car_name            |   miles_per_gallon | cylinders | horsepower |
|:--------------------|-------------------:|----------:|-----------:|
| Mazda RX4           |  21                |         6 |        110 |
| Mazda RX4 Wag       |  21                |         6 |        110 |
| Datsun 710          |  22.8              |         4 |         93 |
| Hornet 4 Drive      |  21.4              |         6 |        110 |
| ...                 |   ...              |       ... |        ... |

### Map-based renaming

Sometimes you want to rename all of the columns in some programmatic way. For example, you might want to lowercase or capitalize all of column names. This is where the `-m, --map` parameters comes in handy.

With map-based renaming you provide a python expression that is evaluated on every column names. The column name is loaded in as `name`. You can perform python string manipulations on this variable.

For example, if we wanted to uppercase all of the column names we could run this.

```
rename -m 'name.upper()'
```

And we would get this.

| CAR                 |   MPG |   CYL |   HP |
|:--------------------|------:|------:|-----:|
| Mazda RX4           |  21   |     6 |  110 |
| Mazda RX4 Wag       |  21   |     6 |  110 |
| Datsun 710          |  22.8 |     4 |   93 |
| Hornet 4 Drive      |  21.4 |     6 |  110 |
| ...                 |   ... |   ... |  ... |


### Sanitizing names

Some of these map-based operations are common enough to justify a shortcut. For example, you might want all of your columns for be in title case, where the first letter of each word is capitalized. In these cases you can use the `-s, --sanitize` parameters to convert all column names using the title case transformation.

```
rename -s title
```

This will give you these column names.

| Car                 |   Mpg |   Cyl |   Hp |
|:--------------------|------:|------:|-----:|
| Mazda RX4           |  21   |     6 |  110 |
| Mazda RX4 Wag       |  21   |     6 |  110 |
| Datsun 710          |  22.8 |     4 |   93 |
| Hornet 4 Drive      |  21.4 |     6 |  110 |
| ...                 |   ... |   ... |  ... |

Here's a list of the available sanitize transformations:
- camel    -> camelCase
- snake    -> snake_case
- kebab    -> kebab-case
- sentence -> Sentence case
- title    -> Title Case

