# Tidy data

Replicating the [tidy data chapter](http://r4ds.had.co.nz/tidy-data.html) from
Hadley Wickham's book [R for Data Science](http://r4ds.had.co.nz/).

The same data can be represented in a variety of ways. Here are four versions of
the same data, just organized differently.

#### Table 1
```bash {comment, execute}
csvlook table1.csv
```
```
| country     |  year |   cases |    population |
| ----------- | ----- | ------- | ------------- |
| Afghanistan | 1,999 |     745 |    19,987,071 |
| Afghanistan | 2,000 |   2,666 |    20,595,360 |
| Brazil      | 1,999 |  37,737 |   172,006,362 |
| Brazil      | 2,000 |  80,488 |   174,504,898 |
| China       | 1,999 | 212,258 | 1,272,915,272 |
| China       | 2,000 | 213,766 | 1,280,428,583 |
```


#### Table 2
```bash {comment, execute}
csvlook table2.csv
```
```
| country     |  year | type       |         count |
| ----------- | ----- | ---------- | ------------- |
| Afghanistan | 1,999 | cases      |           745 |
| Afghanistan | 1,999 | population |    19,987,071 |
| Afghanistan | 2,000 | cases      |         2,666 |
| Afghanistan | 2,000 | population |    20,595,360 |
| Brazil      | 1,999 | cases      |        37,737 |
| Brazil      | 1,999 | population |   172,006,362 |
| Brazil      | 2,000 | cases      |        80,488 |
| Brazil      | 2,000 | population |   174,504,898 |
| China       | 1,999 | cases      |       212,258 |
| China       | 1,999 | population | 1,272,915,272 |
| China       | 2,000 | cases      |       213,766 |
| China       | 2,000 | population | 1,280,428,583 |
```


#### Table 3
```bash {comment, execute}
csvlook table3.csv
```
```
| country     |  year | rate              |
| ----------- | ----- | ----------------- |
| Afghanistan | 1,999 | 745/19987071      |
| Afghanistan | 2,000 | 2666/20595360     |
| Brazil      | 1,999 | 37737/172006362   |
| Brazil      | 2,000 | 80488/174504898   |
| China       | 1,999 | 212258/1272915272 |
| China       | 2,000 | 213766/1280428583 |
```


#### Table 4a (cases)
```bash {comment, execute}
csvlook table4a.csv
```
```
| country     |    1999 |    2000 |
| ----------- | ------- | ------- |
| Afghanistan |     745 |   2,666 |
| Brazil      |  37,737 |  80,488 |
| China       | 212,258 | 213,766 |
```


#### Table 4b (population)
```bash {comment, execute}
csvlook table4b.csv
```
| country     |          1999 |          2000 |
| ----------- | ------------- | ------------- |
| Afghanistan |    19,987,071 |    20,595,360 |
| Brazil      |   172,006,362 |   174,504,898 |
| China       | 1,272,915,272 | 1,280,428,583 |



## Example transformations

Compute rate per 10,000 people.
```bash {comment, execute}
tt -i table1.csv \
    mutate 'rate <- cases / population * 10000'
```
```
country,year,cases,population,rate
Afghanistan,1999,745,19987071,0.372740958393
Afghanistan,2000,2666,20595360,1.2944663264
Brazil,1999,37737,172006362,2.19393047799
Brazil,2000,80488,174504898,4.61236337332
China,1999,212258,1272915272,1.66749511667
China,2000,213766,1280428583,1.66948787959
```


Compute cases per year.
```bash {comment, execute}
tt -i table1.csv \
    aggregate -g year 'cases <- cases.sum()'
```
```
year,cases
1999,250740
2000,296920
```


