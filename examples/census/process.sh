#!/usr/bin/env bash

tt -i acs-data.csv \
    rename -a 'id <- GEO.id2, pop <- HC01_EST_VC01, pop_above_60 <- HC02_EST_VC01' \
    choose -s 'id, pop, pop_above_60' \
    > retire-age-population.csv

tt -i retire-age-population.csv \
    mutate 'id <- id.apply(lambda x: "%05d" % x)' \
    mutate 'state <- id.apply(lambda x: x[0:2])' \
    mutate -g state 'pop_share <- pop / pop.sum()'
