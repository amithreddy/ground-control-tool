import os
from distutils.core import setup

packages = []
for fn in os.listdir('.'):
    if os.path.isfile(fn):
        packages.append(fn)
setup(
    name = "miningapp",
    version = '0.1',
    packages = packages)

