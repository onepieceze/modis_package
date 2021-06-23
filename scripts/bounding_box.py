try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL or OGR library not found, please install GDAL or OGR library.')

def boundingBox(src):

  src_gtrn = src.GetGeoTransform(can_return_null=True)

  src_bbox_cells = ((0., 0.), (0, src.RasterYSize), (src.RasterXSize, 0), (src.RasterXSize, src.RasterYSize))

  geo_pts_x = []
  geo_pts_y = []
  for x, y in src_bbox_cells:
    x2 = src_gtrn[0] + src_gtrn[1] * x + src_gtrn[2] * y
    y2 = src_gtrn[3] + src_gtrn[4] * x + src_gtrn[5] * y
    geo_pts_x.append(x2)
    geo_pts_y.append(y2)
  return ((min(geo_pts_x), min(geo_pts_y)), (max(geo_pts_x), max(geo_pts_y)))