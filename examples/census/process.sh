#!/usr/bin/env bash

tt -i acs-data.csv \
    choose --filter 'not("MOE" in name)' \
    rename \
        --map "name.replace('.', '_').replace('-', '_')" \
        --assign 'id <- GEO_id2' \
    choose -s id
