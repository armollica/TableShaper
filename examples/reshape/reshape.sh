#!/usr/bin/env bash

tableshaper -i population.csv \
    reshape --gather -k year -v population -c 1995:2013 \
    sift 'population > 200000000' \
    reshape --spread -k year -v population \
    choose 'country, 2012, 2013'

tableshaper -i population.csv \
    reshape --gather -k year -v population -c '~country' \
    sift 'population > 200000000' \
    reshape --spread -k year -v population \
    choose 'country, 2012, 2013'
