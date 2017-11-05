#!/usr/bin/env bash

tt input cars.csv \
    choose 'name, mpg:hp' \
    arrange 'mpg, hp:desc' \
    filter 'mpg > 25 | mpg < 15' \
    output

# equivalent to the above statement
cat cars.csv \
    | tt input - \
        choose 'name, mpg:hp' \
        arrange 'mpg, hp:desc' \
        filter 'mpg > 25 | mpg < 15' \
        output

csv2json cars.csv \
    | tt input --json - \
        choose 'name, mpg:hp' \
        output

tt input population.csv \
    gather -k year -v population 1995:2013 \
    filter 'population > 200000000' \
    spread -k year -v population \
    output
