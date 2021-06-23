from progress_callback import progressCallback
try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL or OGR library not found, please install GDAL or OGR library.')

def reprojectOne(l, output, driver, subset, dst_xsize, dst_ysize, dst_wkt, dst_gt,resampling, error_threshold, quiet=False):
  '''
  l = complete name of input dataset
  '''

  l_src_ds = gdal.Open(l)
  meta = l_src_ds.GetMetadata()
  band = l_src_ds.GetRasterBand(subset)
  if '_FillValue' in list(meta.keys()):
    fill_value = meta['_FillValue']
  elif band.GetNoDataValue():
    fill_value = band.GetNoDataValue()
  else:
    fill_value = None
  datatype = band.DataType
  
  try:
    dst_ds = driver.Create(output, dst_xsize, dst_ysize, 1, datatype)
  except:
    raise Exception(f'No possible to create dataset {output}')
  
  dst_ds.SetProjection(dst_wkt)
  dst_ds.SetGeoTransform(dst_gt)

  if fill_value:
    dst_ds.GetRasterBand(1).SetNoDataValue(float(fill_value))
    dst_ds.GetRasterBand(1).Fill(float(fill_value))

  cbk = progressCallback
  cbk_user_data = None

  try:
    gdal.ReprojectImage(l_src_ds, dst_ds, l_src_ds.GetProjection(), dst_wkt, 
                        resampling, 0, error_threshold, cbk, cbk_user_data)
    if not quiet:
      print(f'Layer {l} reprojected.')
  except:
    raise Exception(f'Not possible to reproject dataset {l}.')

  dst_ds.SetMetadata(meta)
  dst_ds = None
  l_src_ds = None

  return 0