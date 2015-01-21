# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-12-07 10:48
# modified : 2014-12-07 10:48
"""
Module handles basic aspects of sequence modeling in LingPy Server.
"""

__author__="Johann-Mattis List"
__date__="2014-12-07"

from lingpy import *
from .query import decode_query
from .settings import rcParams

def tokenize(query):
    """
    Function handles tokenization of sequences into phonological units.
    """

    # note that we don't need defaults here, since these are already defined by
    # switching models (we offer the user to choose a given segmentation
    # schema, and the user can then use it to segmentatize the strings

    data = decode_query(query)
    
    out = []
    for seq in data['sequences']:

        out += [' '.join(ipa2tokens(seq, **rcParams))]
    
    return '\n'.join(out)

def sound_classes(query):
    """
    Function handles conversion of sequences into sound class units.
    """

    data = decode_query(data)
    out = []
    for seq in data['sequences']:

        out += [''.join(tokens2class(ipa2tokens(seq, **rcParams),
            model=rcParams['model']))]
    
    return '\n'.join(out)
