#!/usr/bin/env bash

tt -i cars.csv -o left.csv \
    choose -c 'name, mpg'

tt -i cars.csv -o right.csv \
    choose -c 'name, hp'

tt -i left.csv \
    join --keys name right.csv \
    | csvlook

rm -rf left.csv right.csv
