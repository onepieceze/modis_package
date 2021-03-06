import argparse
from python_geogrid import geogrid
try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL or OGR library not found, please install GDAL or OGR library.')

def convert(inputs, subset):

  ds = gdal.Open(inputs)
  if not ds: print(f"Error: fail to open {inputs}.")
  
  geotranform = ds.GetGeoTransform()
  projection  = ds.GetProjection()
  xsize       = ds.RasterXSize
  ysize       = ds.RasterYSize
  
  in_band = ds.GetRasterBand(subset)
  data    = in_band.ReadAsArray()[::-1, :]

  out = geogrid("write")
  
  out.set_index(key="type"         , value="categorical")
  out.set_index(key="category_min" , value=1)
  out.set_index(key="category_max" , value=20)
  out.set_index(key="projection"   , value="regular_ll")
  out.set_index(key="dx"           , value=geotranform[1])
  out.set_index(key="dy"           , value=abs(geotranform[5]))
  out.set_index(key="known_x"      , value=1)
  out.set_index(key="known_y"      , value=1)
  out.set_index(key="known_lat"    , value=geotranform[3]+geotranform[5]*ysize)
  out.set_index(key="known_lon"    , value=geotranform[0])
  out.set_index(key="wordsize"     , value=1)
  out.set_index(key="tile_x"       , value=xsize)
  out.set_index(key="tile_y"       , value=ysize)
  out.set_index(key="tile_z"       , value=1)
  out.set_index(key="units"        , value="\"category\"")
  out.set_index(key="description"  , value="\"MODIS modified-IGBP landuse - 500 meter\"")
  out.set_index(key="mminlu"       , value="\"MODIFIED_IGBP_MODIS_NOAH\"")
  out.set_index(key="iswater"      , value=17)
  out.set_index(key="isice"        , value=15)
  out.set_index(key="isurban"      , value=13)
  
  index_root = "./"

  out.write_geogrid(data, index_root=index_root)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-i', '--input', required=True, help='Specify the input file name or directory.')
  parser.add_argument('-s', '--subset', required=True, help='Specify subset (band) number from specify data.')

  args = parser.parse_args()

  inputs = args.input
  subset   = int(args.subset)

  convert(inputs, subset)
  