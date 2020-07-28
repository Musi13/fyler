#!/usr/bin/env python3.8
from setuptools import setup, find_packages
from pathlib import Path

# Package meta-data.
DESCRIPTION = 'An application to help organize TV Shows/Anime/Movies'
REQUIRED = [
    # UI
    'PyQT5',

    # AniDB
    'fuzzywuzzy[speedup]',
    'ratelimit',
    'beautifulsoup4',
    'lxml',

    # General
    'requests',
    'appdirs',
    'diskcache',
]

with open(Path(__file__).parent / 'README.md') as f:
    long_description = f.read()

setup(
    name='fyler',
    version='0.1.1',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alex Gonzales',
    python_requires='>=3.8.0',
    packages=find_packages(exclude=['tests']),
    package_data={'fyler.assets': ['*.ui']},
    entry_points={
        'gui_scripts': ['fyler=fyler.__main__:main'],
        'fyler.providers': [
            'anidb = fyler.providers.anidb:AniDBProvider',
            'anilist = fyler.providers.anilist:AniListProvider',
            'thetvdb = fyler.providers.thetvdb:TheTVDBProvider',
        ]
    },
    install_requires=REQUIRED
)
