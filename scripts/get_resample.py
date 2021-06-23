try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL or OGR library not found, please install GDAL or OGR library.')

def getResample(resample):

  if resample == 'AVERAGE':
    return gdal.GRA_Average
  elif resample == 'BILINEAR' or resample == 'BICUBIC':
    return gdal.GRA_Bilinear
  elif resample == 'LANCZOS':
    return gdal.GRA_Lanczos
  elif resample == 'MODE':
    return gdal.GRA_Mode
  elif resample == 'NEAREST_NEIGHBOR':
    return gdal.GRA_NearestNeighbour
  elif resample == 'CUBIC_CONVOLUTION' or resample == 'CUBIC':
    return gdal.gdal.GRA_Cubic
  elif resample == 'CUBIC_SPLINE':
    return gdal.GRA_CubicSpline
  else:
    raise KeyError('Method of resample value not exist.')

  