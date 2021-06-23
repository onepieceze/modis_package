#! /usr/local/bin/python3
#! -*- coding: utf-8 -*-

import argparse
import yaml
import sys
import os
import re
script_root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{script_root}/scripts')
from scripts import read_config,  parse_subset, get_fileNames, init_layers, getUsedLayers, \
                    names_to_fileinfos, calculateNewSize
sys.path.append(f'{script_root}/utils')
from utils import parse_time, cli
try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL library not found, please install GDAL library.')


def joint(fileNames, subset, area, outformat, output, quiet):

  #subset = parse_subset(subset)
  ilayers = init_layers(fileNames, subset)
  layers = getUsedLayers(fileNames, subset, ilayers)
  file_infos = names_to_fileinfos(layers)

  values = list(file_infos.values())
  l1 = values[0][0]
  xsize, ysize, geotransform = calculateNewSize(file_infos)

  driver = gdal.GetDriverByName(outformat)
  if driver is None:
    raise Exception(f'Format driver {outformat} not found, pick a supported driver.')

  driverMD = driver.GetMetadata()
  if 'DCAP_CREATE' not in driverMD:
    raise Exception(f'Format driver {outformat} no support creation and piecewise writing.\n'
                     'Please select a format that does, such as Gtiff (the default) or HFA '
                     '(Erdas Imagine).')
                     
  t_fh = driver.Create(output, xsize, ysize, len(list(file_infos.keys())), l1.band_type)
  if t_fh is None:
    raise Exception(f'Not possible to create dataset {output}.')

  t_fh.SetGeoTransform(geotransform)
  t_fh.SetProjection(l1.projection) ###
  i = 1
  for names in list(file_infos.values()):
    fill = None
    if names[0].fill_value:
      fill = float(names[0].fill_value)
      t_fh.GetRasterBand(i).SetNoDataValue(fill)
      t_fh.GetRasterBand(i).Fill(fill)
    for n in names:
      n.copy_into(t_fh, 1, i, fill)
    i = i + 1
  t_fh = None
  if not quiet:
    print(f'The mosaic file {output} has been created.')

  return True

if __name__ == '__main__':

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-t', '--time', required=True, help='Specify LP DAAC data time')
  parser.add_argument('-d', '--dataset', required=True, help='Specify LP DAAC dataset.')
  parser.add_argument('-s', '--subset', required=True, help='Specify subset number from specify data type')
  parser.add_argument('-o', '--outformat', help='Specify output data formation (default: GTiff [HDF4Image, GTiff, HFA]).', default='GTiff')
  parser.add_argument('-a', '--area', help='Specify the area of LP DACC data (default: china [china, north hemisphere, south hemisphere, global]).', default='china')
  args = parser.parse_args()

  time      = parse_time(args.time).format('YYYY.MM.DD')
  dataset   = args.dataset
  subset    = int(args.subset) - 1
  outformat = args.outformat
  area      = args.area

  config = read_config(script_root)

  data_root = os.path.abspath(config['setting']['download_path'])

  data_root = f'{data_root}/{dataset}/{time}'
  if not os.path.exists(data_root): cli.error(f'directory {data_root} Not Found.')

  fileNames  = get_fileNames(data_root, area, script_root)
  output     = './jointed'

  if outformat == 'GTiff':
    output = f'{output}.tif'
  elif outformat == 'HDF4Image':
    output = f'{output}.hdf'
  elif outformat == 'HFA':
    output = f'{output}.hfa'

  joint(fileNames, subset, area, outformat, output, False)

