import yaml
import sys
import os
sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/../utils')
from utils import cli
import cli

def parse_subset(subset):

  if isinstance(subset, list):
    return subset
  elif isinstance(subset, str):
    subset = subset.replace('(', '').replace(')', '').strip().split()
    return subset
  else:
    raise Exception('Type for subset parameter not supported')


def parse_window(window):

  if isinstance(window, list):
    return window
  elif isinstance(window, str):
    window = window.replace('[', '').replace(']', '').replace(',', '').strip().split()
    window = [float(x) for x in window]
    return window
  else:
    raise Exception('Type for subset parameter not supported')

def select_area(exist_files, area, packet_root):

  with open(f'{packet_root}/{area.upper()}_Tile.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

  config = yaml.load(content, Loader=yaml.FullLoader)

  tiles_number = config['number']

  fileNames = []
  for tile_number in tiles_number:
    is_exist = False
    for exist_file in exist_files:
      if tile_number in exist_file and '.xml' not in exist_file:
        is_exist = True
        fileNames.append(exist_file)
    if not is_exist: cli.warning(f'{tile_number} of {area} is not exist')

  return fileNames

def get_fileNames(data_root, area, packet_root):

  exist_files = os.listdir(data_root)

  n = 0  
  for exist_file in exist_files:
    exist_files[n] = os.path.join(data_root, exist_file)
    n += 1

  with open(f'{packet_root}/fix/{area.upper()}_Tile.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

  config = yaml.load(content, Loader=yaml.FullLoader)

  tiles_number = config['number']

  fileNames = []
  for tile_number in tiles_number:
    is_exist = False
    for exist_file in exist_files:
      if tile_number in exist_file and '.xml' not in exist_file:
        is_exist = True
        fileNames.append(exist_file)
    if not is_exist: cli.warning(f'{tile_number} of {area} is not exist')

  return fileNames