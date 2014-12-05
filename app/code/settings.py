# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-12-05 10:37
# modified : 2014-12-05 10:37
"""
Basic settings for a given LingPy-Server session.
"""

__author__="Johann-Mattis List"
__date__="2014-12-05"

import os

SETTINGS = {}
SETTINGS['root'] = '.'
SETTINGS['server'] = 0
SETTINGS['user'] = ''
SETTINGS['pwd'] = ''
SETTINGS['markdown'] = 'md'

# get the home path of the home directory, tip taken from http://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
SETTINGS['home'] = os.path.expanduser('~')

# starting from here, we need some settings application that can be changed and
# overwritten by the user

