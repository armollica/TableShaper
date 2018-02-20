#!/usr/bin/env bash

tableshaper -i cars.csv -o left.csv \
    choose 'name, mpg'

tableshaper -i cars.csv -o right.csv \
    choose 'name, hp'

tableshaper -i left.csv \
    join --keys name right.csv \
    | csvlook

rm -rf left.csv right.csv

tableshaper -i cars.csv -o left.csv \
    choose 'name, mpg'

tableshaper -i cars.csv -o right.csv \
    choose 'mpg, hp'

tableshaper -i left.csv \
    join --bind-columns right.csv \
    | csvlook

rm -rf left.csv right.csv

tableshaper -i cars.csv -o top.csv \
    choose 'name, mpg' \
    filter 'mpg > 22' \
    arrange 'mpg:desc'

tableshaper -i cars.csv -o bottom.csv \
    choose 'name, mpg' \
    filter 'mpg <= 22' \
    arrange 'mpg'

tableshaper -i top.csv \
    join --bind-rows bottom.csv \
    | csvlook

rm -rf top.csv bottom.csv
