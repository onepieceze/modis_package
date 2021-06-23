from netrc import netrc
from subprocess import Popen
from getpass import getpass
import os
import time
  
def authenticate():

  urs     =  'urs.earthdata.nasa.gov'
  prompts = ['Enter NASA Earthdata Login Username \n(or create an account at urs.earthdata.nasa.gov): ',
             'Enter NASA Earthdata Login Password: ']

  # --------------------------------AUTHENTICATION CONFIGURATION----------------------------------- #
  # Determine if netrc file exists, and if so, if it includes NASA Earthdata Login Credentials
  try:
    netrcDir = os.path.expanduser(f"{os.path.dirname(os.path.realpath(__file__))}/../.netrc")
    netrc(netrcDir).authenticators(urs)[0]
  
  # Below, create a netrc file and prompt user for NASA Earthdata Login Username and Password
  except FileNotFoundError:
    homeDir = os.path.expanduser("~")
    Popen('touch {0}.netrc | chmod og-rw {0}.netrc | echo machine {1} >> {0}.netrc'.format(homeDir + os.sep, urs), shell=True)
    Popen('echo login {} >> {}.netrc'.format(getpass(prompt=prompts[0]), homeDir + os.sep), shell=True)
    Popen('echo password {} >> {}.netrc'.format(getpass(prompt=prompts[1]), homeDir + os.sep), shell=True)
  
  # Determine OS and edit netrc file if it exists but is not set up for NASA Earthdata Login
  except TypeError:
    homeDir = os.path.expanduser("~")
    Popen('echo machine {1} >> {0}.netrc'.format(homeDir + os.sep, urs), shell=True)
    Popen('echo login {} >> {}.netrc'.format(getpass(prompt=prompts[0]), homeDir + os.sep), shell=True)
    Popen('echo password {} >> {}.netrc'.format(getpass(prompt=prompts[1]), homeDir + os.sep), shell=True)
  
  # Delay for up to 1 minute to allow user to submit username and password before continuing
  tries = 0
  while tries < 30:
    try:
      netrc(netrcDir).authenticators(urs)[2]
    except:
      time.sleep(2.0)
    tries += 1

  return netrcDir, urs