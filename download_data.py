#! /usr/local/bin/python3
#! -*- coding: utf-8 -*-

from subprocess import Popen
from getpass import getpass
from netrc import netrc
import requests
from lxml import etree
from shutil import rmtree
import time
import os
import sys
import argparse
script_root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{script_root}/scripts')
from scripts import read_config, parse_subset, call_authentication, select_area
sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/utils')
from utils import parse_time, cli

def download(datasets, dataset, time ,collection, data_root, area, is_force):

  # ---------------------------------READ DOWNLOAD CONFIGURATION------------------------------------ #

  if not os.path.exists(f'{data_root}'):
    cli.error(f'directory {data_root} Not Found.')
    exit(0)

  if not os.path.exists(f'{data_root}/{dataset}'):
    os.mkdir(f'{data_root}/{dataset}')

  saveDir = f'{data_root}/{dataset}/{time}'
  if not os.path.exists(saveDir):
    os.mkdir(saveDir)
  else:
    if is_force:
      rmtree(saveDir)
      os.mkdir(saveDir)

  # Generalize download directory
  if saveDir[-1] != '/' and saveDir[-1] != '\\':
    saveDir = saveDir.strip("'").strip('"') + os.sep

  # Address to call for authentication
  netrcDir, urs = call_authentication.authenticate()

  # -----------------------------------------DOWNLOAD FILE(S)-------------------------------------- #

  url = f"https://e4ftl01.cr.usgs.gov/{datasets}/{dataset}.{collection:03d}/{time}"

  # Create and submit request and download file
  file_list = []
  with requests.get(url.strip()) as response:
    html = etree.HTML(response.text)
    tags = html.xpath('/html/body/pre/a/@href')
    for tag in tags:
      if tag.endswith('.hdf'):            
        file_list.append(tag)
  
  fileNames = select_area(file_list, area, f'{script_root}/fix')

  for fileName in fileNames:
    saveName = fileName[::-1].split('.', 2)[2][::-1]+'.hdf'
    if not is_force:
      exist_files = os.listdir(saveDir)
      if saveName in exist_files: continue
    file_url = os.path.join(url, fileName.split('/')[-1].strip())
    saveName = os.path.join(saveDir, saveName)
    with requests.get(file_url.strip(), stream=True, auth=(netrc(netrcDir).authenticators(urs)[0], netrc(netrcDir).authenticators(urs)[2])) as response:
      print(netrc(netrcDir).authenticators(urs)[0])
      print(netrc(netrcDir).authenticators(urs)[2])
      if response.status_code != 200:
        print("{} not downloaded. Verify that your username and password are correct in {}".format(fileName.split('/')[-1].strip(), netrcDir))
        print(f"Error code {response.status_code}")
      else:
        response.raw.decode_content = True
        content = response.raw
        with open(saveName, 'wb') as d:
          while True:
            chunk = content.read(16 * 1024)
            if not chunk:
              break
            d.write(chunk)
        print('Downloaded file: {}'.format(saveName))

if __name__ == "__main__":

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-t', '--time', required=True, help='Specify LP DDAC downlod data time.')
  parser.add_argument('-d', '--dataset', required=True, help='Specify download LP DAAC dataset.')
  parser.add_argument('-a', '--area', help='Specify the area of LP DACC data (default: china [china, north hemisphere, south hemisphere, global])', default='china')
  parser.add_argument('-f', '--force', help='Force to run', action='store_true')
  args = parser.parse_args()

  time    = parse_time(args.time).format('YYYY.MM.DD')
  dataset = args.dataset
  area    = args.area

  if args.force:
    is_force = True
  else:
    is_force = False
  
  config = read_config(script_root)
  data_root = os.path.abspath(config['setting']['download_path'])
  datasets  = config['dataset']['LP_DAAC'][dataset[0:3]]
  collection = config['collection']

  download(datasets, dataset, time, collection, data_root, area, is_force)


