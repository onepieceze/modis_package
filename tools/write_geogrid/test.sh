cd /Users/xiezm/Project/wind_farm/modis_package/tools/write_geogrid/src
rm write_geogrid.py write_geogrid_wrap.c
swig -python write_geogrid.i
cd /Users/xiezm/Project/wind_farm/modis_package/tools/write_geogrid
python3 setup.py install
