# modis_package
Some python scripts to process modis data.   
This package mainly use to convert modis land use to WRF geogrid format.

## License
modis_package is licensed under the terms of GNU GPL 2.

## Prerequisites

main: gdal, python-geogrid

## Procedure

### Step 1
download modis data

```bash
./chrome_download.py -t 20190101 -d MCD12Q1 -a china (need chromedriver)
./download -t 20190101 -d MCD12Q1 -a china
```

### Step 2
joint modis tile data
```bash
./joint_tile.py -t 20010101 -d MCD12Q1 -a china -s 1
```

### Step 3
```bash
resample modis data grid to WSG84 projection
./resample_grid.py -i jointed.tif -s 1
```

### Step 4 
clip ara to a square area
```bash
./clip_region.py -i resampled.tif -s 1 -w "20, 70, 100, 10"
```

### Step 5
convert to geogrid format (WRF supported)
```bash
./convert_geogrid.py -i clipped.tif -s 1
```

### more
See the code (argparse part) to specific parameters

## Reference
[pyModis](https://github.com/lucadelu/pyModis)

