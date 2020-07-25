# Fyler
 An Open-Source bulk renaming desktop app. Select a number of files, then match them to media by searching with a provider (currently AniDB is the only really supported provider). Files can be renamed/symlinked/hardlinked based on a number of template variables: title, episode number, season number, etc.

This project was heavily inspired by Filebot and attempts to have a similar interface with similar template variables. That said, this project does not intend to replicate all features of Filebot, only the renaming of files. Even then, there's some differences: for example, Fyler currently doesn't perform any introspection of the media being renamed, so certain template variables are completely unavailable.

These are all of the variables currently supported:

|Variable|Description|
|--------|-----------|
|db|Database name, e.g. 'AniDB'|
|id|ID specific to that database|
|t|Title|
|y|Release year|
|n|Series title (for episodes)|
|s|Season number|
|e|Episode number|
|sxe|Season number with zero padded episode number, e.g. '2x04'|
|s00e00|Zero padded season and episode number, e.g. 'S02E0'|
|e00|Zero padded episode number, e.g. '04'|

To use this, download the executable for your platform from the releases tab.
Alternatively, you can install `fyler` from PyPI. Note that fyler requires Python3.8.
