#! /usr/local/bin/python3
#! -*- coding: utf-8 -*-

import os
import sys
import argparse
import requests
from lxml import etree
from selenium import webdriver
import time
script_root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{script_root}/scripts')
from scripts import read_config, select_area
sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/utils')
from utils import parse_time
# Chromedriver download website: http://chromedriver.storage.googleapis.com/index.html

def download(datasets, dataset, data_time, collection, data_root, area, is_force):

  if not os.path.exists(f'{data_root}'):
    cli.error(f'directory {data_root} Not Found.')
    exit(0)

  if not os.path.exists(f'{data_root}/{dataset}'):
    os.mkdir(f'{data_root}/{dataset}')

  cache_root = f'{data_root}/{dataset}/cache'
  if not os.path.exists(cache_root):
    os.mkdir(cache_root)

  # -----------------------------------------DOWNLOAD FILE(S)-------------------------------------- #
  url = f"https://e4ftl01.cr.usgs.gov/{datasets}/{dataset}.{collection:03d}"

  roots = []
  with requests.get(url.strip()) as response:
    html = etree.HTML(response.text)
    tags = html.xpath('/html/body/pre/a/@href')
    for tag in tags:
        if data_time in tag: roots.append(tag)

  fileNames = {}
  for root in roots:
    file_list = []
    root_url = f'{url}/{root}'
    with requests.get(root_url.strip()) as response:
      html = etree.HTML(response.text)
      tags = html.xpath('/html/body/pre/a/@href')
      for tag in tags:
        if tag.endswith('.hdf'): file_list.append(tag)
    fileNames[root] = select_area(file_list, area, f'{script_root}/fix')

  options = webdriver.ChromeOptions()
  prefs = { 'profile.default_content_settings.popups':0 ,'download.default_directory':cache_root}
                   #设置为0表示禁止弹出窗口，                     #设置文件下载路径
  options.add_experimental_option('prefs',prefs)
  driver = webdriver.Chrome(chrome_options=options)

  count = 1
  for root in roots:
    root_url = f'{url}/{root}'
    driver.get(root_url)
    saveDir = f'{data_root}/{dataset}/{root}'
    if not os.path.exists(saveDir):
      os.mkdir(saveDir)
    for fileName in fileNames[root]:
      saveName = fileName[::-1].split('.', 2)[2][::-1]+'.hdf'
      if not is_force:
        exist_files = os.listdir(saveDir)
        if saveName in exist_files: continue
        exist_files = os.listdir(cache_root)
        if fileName in exist_files: continue
      driver.find_element_by_link_text(fileName).click()
      if count == 1: 
        time.sleep(50)
      else:
        time.sleep(5)
      #driver.back()
      driver.get(root_url)
      time.sleep(5)
      count += 1

  time.sleep(90)
    
  driver.quit()

  for root in roots:
    saveDir = f'{data_root}/{dataset}/{root}'
    for fileName in fileNames[root]:
      saveName = fileName[::-1].split('.', 2)[2][::-1]+'.hdf'
      if not is_force:
        exist_files = os.listdir(saveDir)
        if saveName in exist_files: continue
      os.system(f'mv {cache_root}/{fileName} {saveDir}/{saveName}')

if __name__ == '__main__':

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-t', '--time', required=True, help='Specify LP DDAC downlod data time.')
  parser.add_argument('-d', '--dataset', required=True, help='Specify download LP DAAC dataset.')
  parser.add_argument('-a', '--area', help='Specify the area of LP DACC data (default: china [china, north hemisphere, south hemisphere, global])', default='china')
  parser.add_argument('-f', '--force', help='Force to run', action='store_true')
  args = parser.parse_args()

  data_time    = parse_time(args.time).format('YYYY.MM')
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

  download(datasets, dataset, data_time, collection, data_root, area, is_force)