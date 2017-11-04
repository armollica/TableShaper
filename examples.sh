#!/usr/bin/env bash

tt read 'cars.csv' \
    choose 'name, mpg, hp' \
    arrange 'mpg, hp:desc' \
    filter 'mpg > 25 | mpg < 15' \
    write \
    | csvlook

# Above equivalent to this
cat cars.csv \
    | tt read - \
        choose 'name, mpg, hp' \
        arrange 'mpg, hp:desc' \
        filter 'mpg > 25 | mpg < 15' \
        write \
    | csvlook
