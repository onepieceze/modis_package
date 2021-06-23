from collections import OrderedDict
from raster_copy import raster_copy
try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL library not found, please install GDAL library.')

class file_info:

  def init_from_name(self, filename):

    print('filename:', filename)
    fh = gdal.Open(filename)
    if fh is None:
      return 0

    self.filename = filename
    self.bands = fh.RasterCount
    self.xsize = fh.RasterXSize
    self.ysize = fh.RasterYSize
    self.band_type = fh.GetRasterBand(1).DataType
    self.block_size = fh.GetRasterBand(1).GetBlockSize()
    self.projection = fh.GetProjection()
    self.geotransform = fh.GetGeoTransform()
    self.ulx = self.geotransform[0]
    self.uly = self.geotransform[3]
    self.lrx = self.ulx + self.geotransform[1] * self.xsize
    self.lry = self.uly + self.geotransform[5] * self.ysize

    meta = fh.GetMetadata()
    if '_FillValue' in list(meta.keys()):
      self.fill_value = meta['_FillValue']
    elif fh.GetRasterBand(1).GetNoDataValue():
      self.fill_value = fh.GetRasterBand(1).GetNoDataValue()
    else:
      self.fill_value = None

    ct = fh.GetRasterBand(1).GetRasterColorTable()
    if ct is not None:
      self.ct = ct.Clone()
    else:
      self.ct = None

    return 1

  def copy_into(self, t_fh, s_band=1, t_band=1, nodata_arg=None):

    t_geotransform = t_fh.GetGeoTransform()
    t_ulx = t_geotransform[0]
    t_uly = t_geotransform[3]
    t_lrx = t_geotransform[0] + t_fh.RasterXSize * t_geotransform[1]
    t_lry = t_geotransform[3] + t_fh.RasterYSize * t_geotransform[5]

    tgw_ulx = max(t_ulx, self.ulx)
    tgw_lrx = min(t_lrx, self.lrx)
    if t_geotransform[5] < 0:
      tgw_uly = min(t_uly, self.uly)
      tgw_lry = max(t_lry, self.lry)
    else:
      tgw_uly = max(t_uly, self.uly)
      tgw_lry = min(t_lry, self.lry)

    if tgw_ulx >= tgw_lrx:
      return 1
    if t_geotransform[5] < 0 and tgw_uly <= tgw_lry:
      return 1
    if t_geotransform[5] > 0 and tgw_uly >= tgw_lry:
      return 1

    tw_xoff = int((tgw_ulx - t_geotransform[0]) / t_geotransform[1] + 0.1)
    tw_yoff = int((tgw_uly - t_geotransform[3]) / t_geotransform[5] + 0.1)
    tw_xsize = int((tgw_lrx - t_geotransform[0]) / t_geotransform[1] + 0.5) - tw_xoff
    tw_ysize = int((tgw_lry - t_geotransform[3]) / t_geotransform[5] + 0.5) - tw_yoff

    if tw_xsize < 1 or tw_ysize < 1:
      return 1

    sw_xoff = int((tgw_ulx - self.geotransform[0]) / self.geotransform[1])
    sw_yoff = int((tgw_uly - self.geotransform[3]) / self.geotransform[5])
    sw_xsize = int((tgw_lrx - self.geotransform[0]) / self.geotransform[1] - 0.5) - sw_xoff
    sw_ysize = int((tgw_lry - self.geotransform[3]) / self.geotransform[5] - 0.5) - sw_yoff

    if sw_xsize < 1 or sw_ysize < 1:
      return 1

    s_fh = gdal.Open(self.filename)

    return raster_copy(s_fh, sw_xoff, sw_yoff, sw_xsize, sw_ysize, s_band,
                       t_fh, tw_xoff, tw_yoff, tw_xsize, tw_ysize, t_band,
                       nodata_arg)

def names_to_fileinfos(layers):

  file_infos = OrderedDict()
  for k, v in layers.items():
    file_infos[k] = []
    for name in v:
      fi = file_info()
      if fi.init_from_name(name) == 1:
        file_infos[k].append(fi)
        
  return file_infos

