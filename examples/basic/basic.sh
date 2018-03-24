#!/usr/bin/env bash

ts -i cars.csv \
    pick 'name, mpg:hp' \
    sort 'mpg, hp:desc' \
    sift '(mpg > 25) | (mpg < 15)'

cat cars.csv \
    | ts \
        pick 'name, mpg:hp' \
        sort 'mpg, hp:desc' \
        sift '(mpg > 25) | (mpg < 15)'

# csv2json reorders columns
csv2json cars.csv \
    | ts --json \
        pick 'name,mpg,cyl,disp,hp' \
        sort 'mpg, hp:desc' \
        sift '(mpg > 25) | (mpg < 15)'

