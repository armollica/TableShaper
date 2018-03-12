#!/usr/bin/env bash

echo 'write data'
tableshaper -i acs-data.csv -o retire-age-population.csv \
    rename 'id = GEO.id2, pop = HC01_EST_VC01, pop_above_60 = HC02_EST_VC01' \
    mutate -r 'state = ("%05d" % id)[0:2]' \
    choose 'state, id, pop, pop_above_60'

echo 'grouped mutate'
tableshaper -i retire-age-population.csv \
    mutate -g state 'pop_share = pop / pop.sum()' \
    filter 'state.isin(["55", "56"])'

echo 'grouped aggregate'
tableshaper -i retire-age-population.csv \
    aggregate -g state 'pop_sum = pop.sum()'
