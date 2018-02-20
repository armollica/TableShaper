#!/usr/bin/env bash

tableshaper -i cars.csv \
    choose 'name, mpg:hp' \
    arrange 'mpg, hp:desc' \
    filter '(mpg > 25) | (mpg < 15)'

cat cars.csv \
    | tableshaper \
        choose 'name, mpg:hp' \
        arrange 'mpg, hp:desc' \
        filter '(mpg > 25) | (mpg < 15)'

# csv2json reorders columns
csv2json cars.csv \
    | tableshaper --json \
        choose 'name,mpg,cyl,disp,hp' \
        arrange 'mpg, hp:desc' \
        filter '(mpg > 25) | (mpg < 15)'
