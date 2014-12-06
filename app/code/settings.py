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
import json
from lingpy.settings import rcParams
from glob import glob

from .util import write_text_file, normalize_path, read_text_file

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

def modify_segmentation(val):
    """
    Given a segmentation schema, this function modifies the current settings
    for LingPy's segmentation.
    """

    # read the segmentation
    seg = json.loads(
            read_text_file('settings/segmentation/'+val['schema']+'.json')
            )

    for k,v in rcParams.items():
        if k in seg:
            rcParams[k] = seg[k]
    
    rcParams['segmentation'] = val['schema']
    print(val, SETTINGS, seg)

def show_segmentations():
    """
    Return all segmentations currently available as a string with newline
    separation.
    """

    segmentations = glob(normalize_path('settings/segmentation/*.json'))

    return '\n'.join([s.split(os.sep)[-1].replace('.json','') for s in segmentations])


def show_data(dtype):
    """
    Return all datafiles available in the data-directory.
    """
    files = glob(normalize_path('../data/*/*'))
    
    return '\n'.join([os.path.split(f)[1] for f in files if f.endswith(dtype)])

def load_segmentation(schema):
    """
    Given a segmentation schema, this function loads this schema.
    """
    
    data = read_text_file('settings/segmentation/'+schema+'.json')
    return data
    #path = os.path.join('settings', 'segmentation', schema+'.json')
    #if os.path.exists(path):
    #    with open(path) as f:
    #        data = f.read()
    #    rcParams['segmentation'] = schema
    #    return data
    #else:
    #    return False

def modify_sound_classes(schema):
    """
    Modify a given sound class schema.
    """
    pass

def show_sound_classes(schema):
    """
    Show the current schema of available sound class systems.
    """

    pass

def load_sound_classes(schema):
    """
    Load a given sound class schema.
    """
    pass


# additional mods to rcParams (for convenience, later it should be added
# otherwise)
rcParams['segmentation'] = 'sca'
