# Tidy data

Replicating the [tidy data chapter](http://r4ds.had.co.nz/tidy-data.html) from
Hadley Wickham's book [R for Data Science](http://r4ds.had.co.nz/).

The same data can be represented in a variety of ways. Here are four versions of
the same data, just organized differently.

#### Table 1
```bash {comment, execute}
csvlook table1.csv
```

#### Table 2
```bash {comment, execute}
csvlook table2.csv
```

#### Table 3
```bash {comment, execute}
csvlook table3.csv
```

#### Table 4a (cases)
```bash {comment, execute}
csvlook table4a.csv
```

#### Table 4b (population)
```bash {comment, execute}
csvlook table4b.csv
```

## Example transformations

Compute rate per 10,000 people.
```bash {comment, execute}
tt -i table1.csv \
    mutate 'rate <- cases / population * 10000'
```

Compute cases per year.
```bash {comment, execute}
tt -i table1.csv \
    aggregate -g year 'cases <- cases.sum()'
```
