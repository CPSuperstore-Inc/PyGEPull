import logging
import urllib.request as r
from sys import path, argv
import zipfile
import shutil
import os
import importlib
from time import time

start = time()

DEVELOPMENT_RELEASE = "https://github.com/CPSuperstore-Inc/PyGE/archive/master.zip"
LATEST_VERSION = "http://pyge.pythonanywhere.com/api/version/pyge_pull"

TMP_SOURCE_DIR = "PyGE"
DST_DIR = "PyGE"

DEPENDENCIES = """
numpy==1.16.2
moviepy==1.0.0
pygame==1.9.4
xmltodict==0.12.0
screeninfo==0.3.1
matplotlib==3.0.3
typing==3.7.4.1
"""

logging.basicConfig(format='[%(asctime)s] (%(levelname)s) - %(message)s', level=logging.DEBUG, datefmt='%Y/%d/%m %H:%M:%S')

logging.info('Generating A List Of Installed Packages...')

logging.info('Checking PyGE Dependencies...')
for d in DEPENDENCIES.split("\n"):
    if d != "":
        name = d[:d.index("=")]
        lib = importlib.util.find_spec(name)
        if lib is None:
            logging.info('Installing Module "{}"'.format(name))
            os.system("pip install {} --quiet".format(name))

logging.info('Downloading Latest PyGE Release')
r.urlretrieve(DEVELOPMENT_RELEASE, TMP_SOURCE_DIR + '.zip')

logging.info('Installing Latest PyGE Release...')

site_packages = None

logging.info('Locating Python3 Installation Path...')
for p in path:
    if p.lower().replace("\\", "/").endswith("lib/site-packages"):
        site_packages = p
        break

if site_packages is None:
    raise OSError("Python3 Is Not In Your PATH!")

logging.info('Extracting PyGE Source...')
with zipfile.ZipFile(TMP_SOURCE_DIR + ".zip", 'r') as zip_ref:
    zip_ref.extractall(TMP_SOURCE_DIR)

dst = os.path.join(site_packages, DST_DIR)

if os.path.isdir(dst):
    logging.info('Uninstalling Old PyGE Version...')
    shutil.rmtree(dst)

logging.info('Coping Source Files...')
shutil.copytree(os.path.join(TMP_SOURCE_DIR, "PyGE-master"), os.path.join(site_packages, DST_DIR))

logging.info('Cleaning Up Temporary Files...')
shutil.rmtree(TMP_SOURCE_DIR)
os.remove(TMP_SOURCE_DIR + ".zip")
logging.info('Finished Installing Latest PyGE Release In {}s. You Are Up To Date. Enjoy (:'.format(round(time() - start, 2)))

if "-p" not in argv:
    os.system("pause")
