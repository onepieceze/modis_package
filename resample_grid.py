#! /usr/local/bin/python3
#! -*- coding: utf-8 -*-
'''

RESAMPLE METHOD: 
  'AVERAGE', 'BILINEAR', 'CUBIC', 'CUBIC_SPLINE', 'LANCZOS', 'MODE', 'NEAREST_NEIGHBOR'
  
''' 

import argparse
import os
import sys
import numpy as np
script_root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{script_root}/scripts')
from scripts import getResample, createWarped, reprojectOne
sys.path.append(f'{script_root}/utils')
from utils import cli
try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL or OGR library not found, please install GDAL or OGR library.')
try:
    from osgeo import osr
except ImportError:
    try:
        import osr
    except ImportError:
        raise ImportError('Python GDAL library not found, please install python-gdal.')

def resample(fileName, subset, resolution, outformat, epsg, res, output, quiet=False):

  src_ds = gdal.Open(fileName)
  if src_ds == None: cli.error(f"fail to read {fileName}.")
  xsize = src_ds.RasterXSize
  ysize = src_ds.RasterYSize

  dst_srs = osr.SpatialReference()
  dst_srs.ImportFromEPSG(int(epsg))
  dst_wkt = dst_srs.ExportToWkt()

  error_threshold = 0.125
  resampling = getResample(res)

  driver = gdal.GetDriverByName(outformat)
  if driver is None:
    raise Exception(f'Format driver {outformat} not found, pick a supported driver.')

  dst_xsize, dst_ysize, dst_gt = createWarped(fileName, dst_wkt, resampling, error_threshold, resolution)

  reprojectOne(fileName, output, driver, subset, dst_xsize, dst_ysize, dst_wkt, dst_gt, resampling, error_threshold, quiet=quiet)
  if not quiet:
    print(f'All layer for dataset {fileName} reprojected.')

if __name__ == '__main__':

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-i', '--input', required=True, help='Specify Gtiff filename')
  parser.add_argument('-s', '--subset', required=True, help='Specify subset (band) number from specify data type')
  parser.add_argument('-r', '--resolution', help='Specify the resolution of output data (default: 0.00416666667 (500m) )', default=0.00416667)  #0.00416666667)
  parser.add_argument('-o', '--outformat', help='Specify output formation (default: GTiff [HDF4Image, GTiff, HFA]).', default='GTiff')
  parser.add_argument('-e', '--epsg', help='Specify the EPSG code for the prejection of output file (default: 4326 (WGS84) ).', default=4326)
  parser.add_argument('-m', '--resample', help='Specify the resampling method to use (default: NEAREST_NEIGHBOR).', default='NEAREST_NEIGHBOR')
  args = parser.parse_args()

  fileName   = args.input
  subset     = int(args.subset)
  resolution = float(args.resolution)
  outformat  = args.outformat
  epsg       = args.epsg
  res        = args.resample

  if outformat == 'GTiff':
    output = './resampled.tif'
  elif outformat == 'HDF4Image':
    output = './resampled.hdf'
  elif outformat == 'HFA':
    output = './resampled.hfa'

  resample(fileName, subset, resolution, outformat, epsg, res, output)

  