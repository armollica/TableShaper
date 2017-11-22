#!/usr/bin/env bash

tt -i cars.csv -o left.csv \
    choose -c 'name, mpg'

tt -i cars.csv -o right.csv \
    choose -c 'name, hp'

tt -i left.csv \
    join --keys name right.csv \
    | csvlook

rm -rf left.csv right.csv

tt -i cars.csv -o left.csv \
    choose -c 'name, mpg'

tt -i cars.csv -o right.csv \
    choose -c 'mpg, hp'

tt -i left.csv \
    join --how bind-columns right.csv \
    | csvlook

rm -rf left.csv right.csv

tt -i cars.csv -o top.csv \
    choose -c 'name, mpg' \
    filter 'mpg > 22' \
    arrange 'mpg:desc'

tt -i cars.csv -o bottom.csv \
    choose -c 'name, mpg' \
    filter 'mpg <= 22' \
    arrange 'mpg'

tt -i top.csv \
    join --how bind-rows bottom.csv \
    | csvlook

rm -rf top.csv bottom.csv
