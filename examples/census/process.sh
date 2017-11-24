#!/usr/bin/env bash

tt -i acs-data.csv \
    rename 'id <- GEO.id2, pop <- HC01_EST_VC01, pop_above_60 <- HC02_EST_VC01' \
    choose 'id, pop, pop_above_60' \
    > retire-age-population.csv

tt -i retire-age-population.csv \
    mutate --way by-row --name id '"%05d" % id' \
    mutate --way by-row --name state 'id[0:2]' \
    mutate -g state --name pop_share 'pop / pop.sum()' \
    filter 'state.isin(["55", "56"])'
