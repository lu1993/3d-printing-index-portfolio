#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = '3dprinting-index-construct',
    author = 'Lu Cao',
    author_email = 'cao_lu66@live.com',
    url='https://github.com/lu1993/3d-printing-index-portfolio',
    keywords = "3d printing index portfolio".split(),
    description='construct 3d printing index portfolio',
    packages = find_packages(),
    install_requires=[
        "requests >= 2.4.3",
        "tablib >= 0.9.11",
        "backports.csv >= 1.0.4",
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Environment :: Console",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)
