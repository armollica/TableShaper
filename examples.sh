#!/usr/bin/env bash

tidytable -i cars.csv \
    choose 'name, mpg:hp' \
    arrange 'mpg, hp:desc' \
    filter 'mpg > 25 | mpg < 15'

# equivalent to the above statement
cat cars.csv \
    | tidytable \
        choose 'name, mpg:hp' \
        arrange 'mpg, hp:desc' \
        filter 'mpg > 25 | mpg < 15' \
        output

csv2json cars.csv \
    | tidytable --json \
        choose 'name, mpg:hp' \
        output

tidytable -i population.csv \
    gather -k year -v population 1995:2013 \
    filter 'population > 200000000' \
    spread -k year -v population \
    output
