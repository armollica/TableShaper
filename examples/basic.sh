#!/usr/bin/env bash

cd data

tidytable -i cars.csv \
    choose 'name, mpg:hp' \
    arrange 'mpg, hp:desc' \
    filter 'mpg > 25 | mpg < 15'

cat cars.csv \
    | tidytable \
        choose 'name, mpg:hp' \
        arrange 'mpg, hp:desc' \
        filter 'mpg > 25 | mpg < 15'

# csv2json reorders columns
csv2json cars.csv \
    | tidytable --json \
        choose 'name,mpg,cyl,disp,hp' \
        arrange 'mpg, hp:desc' \
        filter 'mpg > 25 | mpg < 15'
