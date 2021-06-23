from distutils.core import setup, Extension
import os

script_root = os.path.dirname(os.path.realpath(__file__))
src_root    = f'{script_root}/src/'

def get_env(string):
    env = os.getenv(string)
    if env == None:
        print(f"[Error]: {string} library environment not define.")
        exit()
    return env

gdal = get_env('GDAL')

extensions = [
      Extension('_write_geogrid', [src_root+'write_geogrid_wrap.c', src_root+'write_geogrid.c'],
                include_dirs=[gdal+'/include'], library_dirs=[gdal+'/lib'], libraries=['gdal'])]

setup(name  = 'write_geogrid',
      version = "1.0",
      ext_modules = extensions,
      py_modules = ['write_geogrid'],
      package_dir = {'' : 'src'}
     )