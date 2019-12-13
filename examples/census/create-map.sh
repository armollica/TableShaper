#!/usr/bin/env

mkdir -p data

cd data

# Info on the Census API:
# https://www.census.gov/data/developers/data-sets/acs-5year.html
if [ ! -e raw-data.json ]; then
    curl -o raw-data.json 'https://api.census.gov/data/2016/acs/acs5?get=NAME,B05002_001E,B05002_013E&for=county:*'
fi

if [ ! -e counties.tar.gz ]; then
    curl -o counties.tar.gz 'https://prd-tnm.s3.amazonaws.com/StagedProducts/Small-scale/data/Boundaries/countyp010g.shp_nt00934.tar.gz'
fi

if [ ! -e countyp010g.shp ]; then
    tar -xzm -f counties.tar.gz
fi

# Clean up the data and join to the county geography
tableshaper \
    input -f json -j values -n foreign_born \
        -c 'name, population, foreign_born, state, county' raw-data.json \
    filter -s 2: \
    mutate -r 'fips = format_text("{state}{county}")' \
    mutate 'pct_foreign_born = parse_float(foreign_born) / parse_float(population)' \
    pick 'fips, pct_foreign_born' \
    input -f shp -n counties countyp010g.shp \
    rename 'fips = ADMIN_FIPS' \
    mutate 'geometry = geometry.simplify(0.01)' \
    pick 'fips, geometry' \
    filter -r 'fips[2:] != "000"' \
    join --left -k fips foreign_born \
    output -f geojson counties-with-foreign-born.json

cd ..

# Draw the map
mapshaper \
    -i data/counties-with-foreign-born.json \
    -colorizer name=getColor \
        colors='#fff7f3,#fde0dd,#fcc5c0,#fa9fb5,#f768a1,#dd3497,#ae017e,#7a0177,#49006a' \
        breaks='0.02,0.04,0.06,0.08,0.10,0.12,0.14,0.16' \
    -proj albersusa \
    -style fill='getColor(pct_foreign_born)' \
    -o map.svg
