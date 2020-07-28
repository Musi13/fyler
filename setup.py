#!/usr/bin/env python3.8
from setuptools import setup, find_packages

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

setup(
    name='fyler',
    version='0.1.0',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author='Alex Gonzales<musigonzales@gmail.com>',
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
