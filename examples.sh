#!/usr/bin/env bash

tidytable -i cars.csv \
    choose 'name, mpg:hp' \
    arrange 'mpg, hp:desc' \
    filter 'mpg > 25 | mpg < 15'

# same as above
cat cars.csv \
    | tidytable \
        choose 'name, mpg:hp' \
        arrange 'mpg, hp:desc' \
        filter 'mpg > 25 | mpg < 15' 

# same as above (ish)
csv2json cars.csv \
    | tidytable --json \
        choose 'name, mpg:hp'

tidytable -i population.csv \
    gather -k year -v population 1995:2013 \
    filter 'population > 200000000' \
    spread -k year -v population

# same as above
tidytable -i population.csv \
    gather -k year -v population '~country' \
    filter 'population > 200000000' \
    spread -k year -v population
