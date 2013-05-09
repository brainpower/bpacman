#!/usr/bin/python3

from distutils.core import setup

setup(name='bpacman',
      version='0.1.0',
			description="A pacman GUI written in python using pyalpm.",
			author="brainpower",
			author_email="brainpower@gulli.com",
			url="",
			packages=['bpacman'],
			scripts=['src/bpacman']
)
