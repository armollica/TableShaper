#!/usr/bin/env bash

if [ ! -e data/counties-with-foreign-born.json ]; then
    bash get-data.sh
fi

mapshaper \
    -i data/counties-with-foreign-born.json \
    -colorizer name=getColor \
        colors='#fff7f3,#fde0dd,#fcc5c0,#fa9fb5,#f768a1,#dd3497,#ae017e,#7a0177,#49006a' \
        breaks='0.02,0.04,0.06,0.08,0.10,0.12,0.14,0.16' \
    -proj albersusa \
    -style fill='getColor(pct_foreign_born)' \
    -o map.svg
