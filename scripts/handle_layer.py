from collections import OrderedDict
try:
  from osgeo import gdal
except ImportError:
  try:
    import gdal
  except ImportError:
    raise ImportError('Python GDAL library not found, please install GDAL library.')

def init_layers(fileNames, subset):

  if isinstance(fileNames, list):
    src_ds = gdal.Open(fileNames[0])
  else:
    raise Exception("The input value should be a list of HDF file")
  
  src_layers = src_ds.GetSubDatasets()
  layers    = OrderedDict()
# n = 0
#  for i in subset:
#    if str(i) == '1':    ####
  name = src_layers[subset][0].split(':')[-1]
  layers[name] = list()
#    n += 1
  return layers

def getUsedLayers(fileNames, subset, layers):

  for fileName in fileNames:
    src_ds = gdal.Open(fileName)
    src_layers = src_ds.GetSubDatasets()
#    n = 0
#    for i in subset:
#      if str(i) == '1':  ####
    name = src_layers[subset][0].split(':')[-1]
    layers[name].append(src_layers[subset][0])
#      n += 1
  return layers
  
    