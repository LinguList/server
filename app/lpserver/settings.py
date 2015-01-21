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
from lingpy.settings import rcParams, rc
from lingpy.data.model import Model

from glob import glob

from .util import write_text_file, normalize_path, read_text_file

rcParams['root'] = '.'
rcParams['server'] = 0
rcParams['user'] = ''
rcParams['pwd'] = ''
rcParams['markdown'] = 'md'

# get the home path of the home directory, tip taken from http://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
rcParams['home'] = os.path.expanduser('~')

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
    
    rcParams['segmentations_current'] = val['schema']

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

def modify_sound_classes(schema):
    """
    Modify a given sound class schema.
    """
    
    # check if schema is one of the basic sound class models
    if schema in ['asjp', 'sca', 'dolgo']:
        rcParams['model'] = rcParams['schema']

    # if not, we need to load the model
    else:
        scm = Model(normalize_path('settings/sound_classes/'+schema))
        rcParams['model'] = scm

    rcParams['sound_class_models_current'] = schema

def show_sound_classes():
    """
    Show the current schema of available sound class systems.
    """
    
    files = glob(normalize_path('settings/sound_classes/*'))
    
    return '\n'.join([os.path.split(f)[1] for f in files])

def load_sound_classes(schema):
    """
    Load a given sound class schema.
    """
    
    # read the data from text file
    data = read_text_file('settings/sound_classes/'+schema+'/converter')

    return data

def store_sound_classes(data):
    """
    Store a user-defined sound class model.
    """
    
    write_text_file('settings/sound_classes/'+data['name']+'/converter',
            data['data'])

    return 'success'

def modify_schema(schema):
    """
    Redefine the application schema.
    """
    
    # modify schema
    rc(schema=schema)

    # for temporal compatibility with older lingpy source
    if schema == 'ipa':
        rcParams['model'] = rcParams['sca']
        rcParams['sound_class_models_current'] = 'sca'
        rcParams['segmentations_current'] = 'ipa'
    else:
        rcParams['model'] = rcParams['asjp']
        rcParams['sound_class_models_current'] = 'asjp'
        rcParams['segmentations_current'] = 'asjp'
    print('modified',schema)
    return 'success'

# additional mods to rcParams (for convenience, later it should be added
# otherwise)
print(rcParams.keys())
rcParams['sound_class_models_current'] = rcParams['model'].name
rcParams['segmentations_current'] = 'ipa'
