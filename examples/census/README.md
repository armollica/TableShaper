# Mapping Census data

Download, clean up and map data from the U.S. Census Bureau using TablesShaper and [mapshaper](https://mapshaper.org/).

Here's the map that we'll create.

![Map showing the share of county population that's foreign born.](https://github.com/armollica/TableShaper/blob/master/examples/census/map.svg)

This shows the percentage of a county's population that is foreign born. Darker colors indicate a higher share of the population is foreign born.

Here are the steps to make this. You can also check out `create-map.sh` for the entire process in a bash script.

Download the census data as a JSON file. This file has the total population,
the foreign born population and an FIPS code that we will use to join the data 
to the county geodata.

```bash
curl -o raw-data.json 'https://api.census.gov/data/2016/acs/acs5?get=NAME,B05002_001E,B05002_013E&for=county:*'
```

Download the county geodata. This data compressed in a tarball that you 
unpack.

```bash
curl -o counties.tar.gz 'https://prd-tnm.s3.amazonaws.com/StagedProducts/Small-scale/data/Boundaries/countyp010g.shp_nt00934.tar.gz'
tar -xzm -f counties.tar.gz
```

With the all the data downloaded, we can use TableShaper to clean things up and join the two dataset.

First, import the JSON file. 

This particular JSON file is formatted in the array-of-arrays, "values" format which looks looks like this.

```
[
    ["NAME","B05002_001E","B05002_013E","state","county"],
    ["Carroll County, Arkansas","27690","2289","05","015"],
    ["Chicot County, Arkansas","11189","286","05","017"],
    ["Clark County, Arkansas","22684","657","05","019"],
    ...
]
```

We specify that it's formatted this way by passing `values` to the `-j` parameter.

We name the table `foreign_born` with the `-n` parameter. It's helpful to name a table when you're importing and joining multiple tables like we will be in this example.

Finally, we give the columns meaningful names by passing a comma-separated list of names to the `-c` parameter.

```bash
input -f json -j values -n foreign_born \
    -c 'name, population, foreign_born, state, county' raw-data.json
```

The JSON file's first row contains column names that we don't use. Remove that
first row using the filter command's slice parameter `-s`.

```bash
filter -s 2:
```

Create a 5-digit FIPS column by concatenating the 2-digit state FIPS and and
3-digit county FIPS codes. We'll use this to join the data to the county
geodata.

```bash
mutate -r 'fips = format_text("{state}{county}")'
```

Calculate the percent county population that's foreign born.

```bash
mutate 'pct_foreign_born = parse_float(foreign_born) / parse_float(population)'
```

Drop unnecessary columns. Keep just the FIPS code and the percent of population
that's foreign born.

```bash
pick 'fips, pct_foreign_born'
```

Now import the county geodata. We names the table `counties`.

```bash
input -f shp -n counties countyp010g.shp
```

Rename the FIPS column to match the name in the other table.

```bash
rename 'fips = ADMIN_FIPS'
```

Simplify the county polygons. We are doing a zoomed out map of the whole U.S.
so we don't need the level of detail present in the original shapefile.

```bash
mutate 'geometry = geometry.simplify(0.01)'
```

Drop unnecessary columns, keeping just the FIPS code and the geometry.

```bash
pick 'fips, geometry'
```

Remove lakes from the geodata. Lakes have FIPS codes that end in three zeroes.

```bash
filter -r 'fips[2:] != "000"'
```

Remove Puerto Rico. We do this because the map projection we're using doesn't
fit it nicely into the canvas like it does for Alaska and Hawaii. The first two
digits of its FIPS code is 72.

```bash
filter -r 'fips[:2] != "72"' \
```

Join the census data to the geodata using the FIPS code column. Since the current "target" table is `counties` we need to tell TableShaper that we'll be joining this to the `foreign_born` table we cleaned earlier.

```bash
join --left -k fips foreign_born
```

Export the data as GeoJSON.

```bash
output -f geojson counties-with-foreign-born.json
```

Here's what that looks like all together.

```bash
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
    filter -r 'fips[:2] != "72"' \
    join --left -k fips foreign_born \
    output -f geojson counties-with-foreign-born.json
```

Now let's map it. We'll use mapshaper for this.

First, create a colorizer function that takes a list of colors and a list of
break points. Use this function to color the polygons. Finally, reproject the 
data to U.S. Albers and export it as SVG.

Here's the full command.

```bash
mapshaper \
    -i data/counties-with-foreign-born.json \
    -colorizer name=getColor \
        colors='#fff7f3,#fde0dd,#fcc5c0,#fa9fb5,#f768a1,#dd3497,#ae017e,#7a0177,#49006a' \
        breaks='0.02,0.04,0.06,0.08,0.10,0.12,0.14,0.16' \
    -style fill='getColor(pct_foreign_born)' \
    -proj albersusa \
    -o map.svg
```
