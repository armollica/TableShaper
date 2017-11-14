#!/usr/bin/env bash

tt -i acs-data.csv \
    rename \
        --map "name.replace('.', '_').replace('-', '_')" \
        --assign 'id <- GEO_id2' \
    choose \
        --filter 'not("MOE" in name)' \
        --select '~GEO_id, ~GEO_display_label' \
    gather ~id
