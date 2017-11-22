#!/usr/bin/env bash

tt -i cars.csv \
    choose -c 'name, mpg:hp' \
    arrange 'mpg, hp:desc' \
    filter '(mpg > 25) | (mpg < 15)'

cat cars.csv \
    | tt \
        choose -c 'name, mpg:hp' \
        arrange 'mpg, hp:desc' \
        filter '(mpg > 25) | (mpg < 15)'

# csv2json reorders columns
csv2json cars.csv \
    | tt --json \
        choose -c 'name,mpg,cyl,disp,hp' \
        arrange 'mpg, hp:desc' \
        filter '(mpg > 25) | (mpg < 15)'
