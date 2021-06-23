#! /usr/local/bin/python3
#! -*- coding: utf-8 -*-
import argparse
import os
import sys
from array import array
script_root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{script_root}/scripts')
from scripts import read_config, parse_window
sys.path.append(f'{script_root}/utils')
from utils import cli
try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL or OGR library not found, please install GDAL or OGR library.')

def clip(fileName, subset, outformat, window, output):

  ds = gdal.Open(fileName)
  if ds == None: cli.error(f"fail to read {fileName}.")
  gt = ds.GetGeoTransform()

  offset_x = abs(int((gt[0] - window[0])/gt[1]))
  offset_y = abs(int((gt[3] - window[1])/gt[5]))

  block_xsize = abs(int((gt[0] - window[2])/gt[1])) - offset_x
  block_ysize = abs(int((gt[3] - window[3])/gt[5])) - offset_y

  ulx = gt[0] + offset_x * gt[1]
  uly = gt[3] + offset_y * gt[5]

  xsize = ds.RasterXSize
  ysize = ds.RasterYSize

  in_band = ds.GetRasterBand(subset)

  out_band = in_band.ReadAsArray(offset_x, offset_y, block_xsize, block_ysize)

  driver = gdal.GetDriverByName(outformat)
  src_ds = driver.Create(output, block_xsize, block_ysize, 1, in_band.DataType)

  gt = (ulx, gt[1], gt[2], uly, gt[4], gt[5])

  src_ds.SetGeoTransform(gt)
  src_ds.SetProjection(ds.GetProjection())

  src_ds.GetRasterBand(1).WriteArray(out_band)

  src_ds.FlushCache()

  del src_ds

  print(" Notice: GeoTransform -> ", gt)
  print(f"   Size: X -> {block_xsize} ; Y -> {block_ysize}")

if __name__ == '__main__':

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-i', '--input', required=True, help='Specify Gtiff filename')
  parser.add_argument('-s', '--subset', required=True, help='Specify subset (band) number from specify data.')
  parser.add_argument('-o', '--outformat', help='Specify output formation (default: GTiff [HDF4Image, GTiff, HFA]).', default='GTiff')
  parser.add_argument('-w', '--window', help='Specify subwindow in projected coordinates to extract:' 
                                             '"ulx, uly, lrx, lry" (default: "70, 55, 140, 10").', default="70, 55, 140, 10")
  args = parser.parse_args()

  fileName  = args.input
  subset    = int(args.subset)
  outformat = args.outformat
  window    = parse_window(args.window)

  if outformat == 'GTiff':
    output = './clipped.tif'
  elif outformat == 'HDF4Image':
    output = './clipped.hdf'
  elif outformat == 'HFA':
    output = './clipped.hfa'

  clip(fileName, subset, outformat, window, output)
  