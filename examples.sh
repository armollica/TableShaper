#!/usr/bin/env bash

tt input 'cars.csv' \
    choose 'name, mpg, hp' \
    arrange 'mpg, hp:desc' \
    filter 'mpg > 25 | mpg < 15' \
    output \
    | csvlook

# Above equivalent to this
cat cars.csv \
    | tt input - \
        choose 'name, mpg, hp' \
        arrange 'mpg, hp:desc' \
        filter 'mpg > 25 | mpg < 15' \
        output \
    | csvlook

csv2json cars.csv \
    | tt input --json - \
        choose 'name, mpg, hp' \
        arrange 'mpg, hp:desc' \
        filter 'mpg > 25 | mpg < 15' \
        output \
    | csvlook
