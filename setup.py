#!/usr/bin/env python3.8
from setuptools import setup

# Package meta-data.
DESCRIPTION = 'An application to help organize TV Shows/Anime/Movies'
REQUIRED = [
    # UI
    'PyQT5',

    # AniDB
    'fuzzywuzzy[speedup]',
    'ratelimit',
    'diskcache',
    'beautifulsoup4',
    'lxml',

    # General
    'requests',
    'appdirs',
]

setup(
    name='fyler',
    version='0+unknown',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author='Alex Gonzales<musigonzales@gmail.com>',
    python_requires='>=3.8.0',
    packages=['fyler', 'fyler.providers'],
    entry_points={
        'gui_scripts': ['fyler=fyler.__main__:main'],
        'fyler.providers': [
            'anidb = fyler.providers.anidb:AniDBProvider',
            'anilist = fyler.providers.anilist:AniListProvider',
        ]
    },
    install_requires=REQUIRED
)
