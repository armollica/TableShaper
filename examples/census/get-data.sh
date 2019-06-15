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

mapshaper data/counties-with-foreign-born.json -colorizer name=getColor colors='#f0f9e8,#bae4bc,#7bccc4,#2b8cbe' breaks='0.01,0.02,0.03' -proj albersusa -style fill='getColor(pct_foreign_born)' -o output.svg

cd ..