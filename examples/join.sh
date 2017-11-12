#!/usr/bin/env bash

cd data

tidytable -i cars.csv -o left.csv \
    choose 'name, mpg'

tidytable -i cars.csv -o right.csv \
    choose 'name, hp'

tidytable -i left.csv \
    join --keys name right.csv \
    | csvlook

rm -rf left.csv right.csv
