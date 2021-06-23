import os
import yaml
import gdal
import osr
import tilemap3

def read_tile_loc(latitude, longitude):

  coord  = tilemap3.To_GlobalMapCoordinate('sn', 'h', float(latitude), float(longitude))

  return coord.x, coord.y

def array_2_raster(newRasterfn, array, latitude, longitude, geotransform):

  cols = array.shape[1]
  rows = array.shape[0]
  
  driver = gdal.GetDriverByName('GTiff')

  outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
  outRaster.SetGeoTransform(geotransform)

  outband = outRaster.GetRasterBand(1)
  outband.WriteArray(array)

  outRasterSRS = osr.SpatialReference()
  outRasterSRS.ImportFromEPSG(4326)
  outRaster.SetProjection(outRasterSRS.ExportToWkt())

  outband.FlushCache()





  

  