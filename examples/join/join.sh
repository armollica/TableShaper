#!/usr/bin/env bash

ts -i cars.csv -o left.csv \
    pick 'name, mpg'

ts -i cars.csv -o right.csv \
    pick 'name, hp'

ts -i left.csv \
    join --keys name right.csv

rm -rf left.csv right.csv

ts -i cars.csv -o left.csv \
    pick 'name, mpg'

ts -i cars.csv -o right.csv \
    pick 'mpg, hp'

ts -i left.csv \
    join --bind-columns right.csv 

rm -rf left.csv right.csv

ts -i cars.csv -o top.csv \
    pick 'name, mpg' \
    sift 'mpg > 22' \
    sort 'mpg:desc'

ts -i cars.csv -o bottom.csv \
    pick 'name, mpg' \
    sift 'mpg <= 22' \
    sort 'mpg'

ts -i top.csv \
    join --bind-rows bottom.csv

rm -rf top.csv bottom.csv
