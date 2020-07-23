#!/usr/bin/env python3.8

from setuptools import find_packages, setup

# Package meta-data.
NAME = ''
DESCRIPTION = 'A collection of utilities for automatically organizing TV Shows/Anime/Movies'
URL = 'None'
EMAIL = 'None'
AUTHOR = 'Musi'
REQUIRES_PYTHON = '>=3.8.0'
VERSION = '0+unknown'

# What packages are required for this module to be executed?
REQUIRED = [
    # CLI
    'click',

    # UI
    'PyQT5',

    # AniDB
    'textdistance[extras]',
    'ratelimit',
    'diskcache',
    'beautifulsoup4',
    'lxml',

    # General
    'requests',
    'appdirs',
    'pluggy',
]


# Where the magic happens:
setup(
    name='fyler',
    version='0+unknown',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    packages=['fyler', 'fyler.providers'],
    entry_points={
        'console_scripts': ['fyler=fyler.__main__:main'],
        'fyler.providers': [
            'anidb = fyler.providers.anidb:AniDBProvider',
            'anilist = fyler.providers.anilist:AniListProvider',
        ]
    },
    install_requires=REQUIRED
)
