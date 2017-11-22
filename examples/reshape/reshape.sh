#!/usr/bin/env bash

tt -i population.csv \
    gather -k year -v population 1995:2013 \
    filter 'population > 200000000' \
    spread -k year -v population \
    choose -c 'country, 2012, 2013' \
    | csvlook

tt -i population.csv \
    gather -k year -v population '~country' \
    filter 'population > 200000000' \
    spread -k year -v population \
    choose -c 'country, 2012, 2013' \
    | csvlook

tt -i population.csv \
    reshape -g -k year -v population -c '~country' \
    filter 'population > 200000000' \
    reshape -s -k year -v population \
    choose -c 'country, 2012, 2013' \
    | csvlook