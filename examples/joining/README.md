# Working with multiple tables and how to do joins

This example will walk through importing multiple tables and performing joins on these tables.

We'll be working with two tables. 

The first is a table with population statistics for states in the U.S.

|   id | name                 |   population |   population_under_18 |
|-----:|:---------------------|-------------:|----------------------:|
|    1 | Alabama              |      4864680 |               1098793 |
|    2 | Alaska               |       738516 |                186138 |
|    4 | Arizona              |      6946685 |               1633783 |
|    5 | Arkansas             |      2990671 |                705943 |
|  ... | ...                  |          ... |                   ... |

The second is a table with median household income for states.

|   id | name                 |   median_household_income |
|-----:|:---------------------|--------------------------:|
|    1 | Alabama              |                     48486 |
|    2 | Alaska               |                     76715 |
|    4 | Arizona              |                     56213 |
|    5 | Arkansas             |                     45726 |
|  ... | ...                  |                       ... |

We're going to import both tables, create a new column in one of the tables and then join the two tables together. Here's the full set of commands. We'll break this down step-by-step.

```
tableshaper \
    input population.csv \
    input income.csv \
    target population \
    mutate 'percent_under_18 = population_under_18 / population' \
    join -k id,name income \
    output output.csv
```

### Importing multiple tables.

Here's how we would import both of these tables. 

```
tableshaper \
    input population.csv \
    input income.csv \
    ...
```

Unless you specify it, the tables will be named based on the file name, in this case, `population` and `income` respectively.

### "Targeting" the table you want to work on

With TableShaper you work on one table at a time. Whenever you import a table, that table becomes the active table. In our example, the active table is `income` because it was imported last.

You can use the `target` command to change the active table.

This is how we would change the active table to the `population` table.

```
target population
```

Now we could run commands on the this table. For example, we could add a column for the the percent of population under 18.

```
mutate 'percent_under_18 = population_under_18 / population'
```

That would give us this.

|   id | name                 |   population |   population_under_18 |   percent_under_18 |
|-----:|:---------------------|-------------:|----------------------:|-------------------:|
|    1 | Alabama              |      4864680 |               1098793 |           0.225872 |
|    2 | Alaska               |       738516 |                186138 |           0.252043 |
|    4 | Arizona              |      6946685 |               1633783 |           0.235189 |
|    5 | Arkansas             |      2990671 |                705943 |           0.236048 |
|   .. | ...                  |          ... |                   ... |                ... |

### Joining tables

We can use the `join` command to perform SQL-join table joins.

In this case, we want to join the tables based on the two columns they have in common, `id` and `name`. Here's the command for that.

```
join -k id,name income
```

Which gives us this.

|   id | name     |  population |   population_under_18 | percent_under_18 | median_household_income |
|-----:|:---------|------------:|----------------------:|-----------------:|------------------------:|
|    1 | Alabama  |     4864680 |               1098793 |         0.225872 |                   48486 |
|    2 | Alaska   |      738516 |                186138 |         0.252043 |                   76715 |
|    4 | Arizona  |     6946685 |               1633783 |         0.235189 |                   56213 |
|    5 | Arkansas |     2990671 |                705943 |         0.236048 |                   45726 |
|  ... |      ... |         ... |                   ... |              ... |                     ... |

Here we're joining the `income` table to the currently active table, `population`.

By default the `join` command performs a left join, but you can change this to a right, full or outer join using the `--right`, `--outer` and `--inner` flags.
