#!/usr/bin/env bash

tt -i population.csv \
    reshape --way gather -k year -v population -c 1995:2013 \
    filter 'population > 200000000' \
    reshape --way spread -k year -v population \
    choose -c 'country, 2012, 2013' \
    | csvlook

tt -i population.csv \
    reshape --way gather -k year -v population -c '~country' \
    filter 'population > 200000000' \
    reshape --way spread -k year -v population \
    choose -c 'country, 2012, 2013' \
    | csvlook
