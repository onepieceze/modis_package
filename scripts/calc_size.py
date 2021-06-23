
def calculateNewSize(file_infos):

  values = list(file_infos.values())

  l1  = values[0][0]

  ulx = l1.ulx
  uly = l1.uly
  lrx = l1.lrx
  lry = l1.lry

  for fi in file_infos[list(file_infos.keys())[0]]:
    ulx = min(ulx, fi.ulx)
    uly = max(uly, fi.uly)
    lrx = max(lrx, fi.lrx)
    lry = min(lry, fi.lry)
  psize_x = l1.geotransform[1]
  psize_y = l1.geotransform[5]

  geotransform = [ulx, psize_x, 0, uly, 0, psize_y]
  xsize = int((lrx - ulx) / geotransform[1] + 0.5)
  ysize = int((lry - uly) / geotransform[5] + 0.5)

  return xsize, ysize, geotransform
  