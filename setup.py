#!/usr/bin/python3

from distutils.core import setup
from distutils import sysconfig
import sys


setup(name='bpacman',
      version='0.1.0',
			description="A pacman GUI written in python using pyalpm.",
			author="brainpower",
			author_email="brainpower@gulli.com",
			url="",
			packages=['bpacman'],
			scripts=['src/bpacman'],
			data_files = [('share/bpacman', ['data/package-available.png',
			                                 'data/package-install.png',
			                                 'data/package-remove.png',
			                                 'data/package-installed-outdated.png',
			                                 'data/package-installed-updated.png',
			                                 'data/package-reinstall.png',
			                                 'data/package-available.png',
			                                # 'data/',
			                                 'data/package-upgrade.png',])]
)

#package-available-locked.png
#package-broken.png
#package-downgrade.png
#package-purge.png
#package-new.png
#package-installed-locked.png
