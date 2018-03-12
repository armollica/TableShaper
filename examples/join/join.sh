#!/usr/bin/env bash

tableshaper -i cars.csv -o left.csv \
    choose 'name, mpg'

tableshaper -i cars.csv -o right.csv \
    choose 'name, hp'

tableshaper -i left.csv \
    join --keys name right.csv

rm -rf left.csv right.csv

tableshaper -i cars.csv -o left.csv \
    choose 'name, mpg'

tableshaper -i cars.csv -o right.csv \
    choose 'mpg, hp'

tableshaper -i left.csv \
    join --bind-columns right.csv 

rm -rf left.csv right.csv

tableshaper -i cars.csv -o top.csv \
    choose 'name, mpg' \
    sift 'mpg > 22' \
    sort 'mpg:desc'

tableshaper -i cars.csv -o bottom.csv \
    choose 'name, mpg' \
    sift 'mpg <= 22' \
    sort 'mpg'

tableshaper -i top.csv \
    join --bind-rows bottom.csv

rm -rf top.csv bottom.csv
