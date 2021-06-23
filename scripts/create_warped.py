from bounding_box import boundingBox
from calc_resolution import calculateRes
try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL or OGR library not found, please install GDAL or OGR library.')

def createWarped(raster, dst_wkt, resampling, error_threshold, resolution=False):

  src = gdal.Open(raster)
  tmp_ds = gdal.AutoCreateWarpedVRT(src, src.GetProjection(), dst_wkt, resampling, error_threshold)

  if not resolution:
    dst_xsize = tmp_ds.RasterXSize
    dst_ysize = tmp_ds.RasterYSize
    dst_gt    = tmp_ds.GetGeoTransform()
  else:
    bbox = boundingBox(tmp_ds)
    dst_xsize = calculateRes(bbox[0][0], bbox[1][0], resolution)
    dst_ysize = calculateRes(bbox[0][1], bbox[1][1], resolution)
    if dst_xsize == 0:
      raise Exception('Invalid number of pixel 0 for X size. The problem could be in an invalid value of resolution.')
    elif dst_ysize == 0:
      raise Exception('Invalid number of pixel 0 for Y size. The problem could be in an invalid value of resolution.')
    dst_gt = [bbox[0][0], resolution, 0.0, bbox[1][1], 0.0, -resolution]
  
  tmp_ds = None
  src    = None

  return dst_xsize, dst_ysize, dst_gt
