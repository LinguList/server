# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-12-05 10:33
# modified : 2014-12-06 13:34
"""
Alignment backend for LingPy Server.
"""

__author__="Johann-Mattis List"
__date__="2014-12-06"

from lingpy import *
from lingpy.convert.html import *
from lingpy.convert.strings import *

from .settings import rcParams
from .util import normalize_path
from .query import decode_query, encode_query

def pairwise(query):
    """
    Function carries out pairwise alignments from a given query.
    """

    defaults = dict(
            mode = "global",
            model = "sca",
            gop = -2,
            scale = 0.5,
            factor = 1,
            restricted_chars = "_T"
            )

    data = decode_query(query)
    
    # check for seqs or file 
    if 'seqs' in data:

        # convert seqs to correct format
        seqs = []
        for seq in data['seqs']:
            seqA,seqB = seq.split('//')
            seqs += [(seqA.strip(),seqB.strip())]

    else:

        # get the psa object
        psa = PSA(normalize_path('../data/psa/'+data['file']))
        seqs = psa.seqs

    # modify floats and the like
    for k,v in data.items():
        if type(v) == str:
            try:
                data[k] = float(v)
            except ValueError:
                try:
                    data[k] = int(v)
                except ValueError:
                    data[k] = v

    
    # check for vowel merge
    if 'merge_vowels' in data:
        data['merge_vowels'] = eval(data['merge_vowels'])
    
    # check for distance or similarity output
    hamming = False
    if 'distance' in data:
        if data['distance'] not in ['hamming', 'nhamming']:
            data['distance'] = eval(data['distance'])
        else:
            hamming = True

    # parse defaults 
    for k in defaults:
        if k not in data:
            data[k] = defaults[k]

    if data['method'] == 'sca':
        psa = Pairwise(seqs, merge_vowels=data['merge_vowels'])
        psa.align(**data)
        alms = psa.alignments
    else:
        alms = []
        for a,b in seqs:
            seqA = ipa2tokens(a, merge_vowels=data['merge_vowels'])
            seqB = ipa2tokens(b, merge_vowels=data['merge_vowels'])

            almA, almB, score = pw_align(seqA, seqB, **data)

            if data['mode'] == 'local':
                almA = almA[1]
                almB = almB[1]
            alms += [(almA,almB,score)]
            
    txt = ''
    for almA,almB,dist in alms:
        if hamming:
            cdist = len([1 for a,b in zip(almA,almB) if a != b])
            if data['distance'] == 'nhamming':
                cdist = cdist / len(almA)
                
        else:
            cdist = dist
        txt += ' '.join(almA) + '//' + ' '.join(almB) + '//' + '{0:.2f}'.format(cdist) + '\n'
    
    # pass the object reference to rcParams to make it usable by other
    # functions, currently, we have the problem that we don't have a unified
    # object to use here, so we just use the alignments that were carried out
    # already
    rcParams['psa'] = alms

    return txt

def multiple(query):
    """
    Function carries out multiple alignments from a query.
    """
    defaults = dict(
            method = "progressive",
            model = "sca",
            mode = "global",
            gop = -5,
            scale = 0.6,
            factor = 1,
            tree_calc = "neighbor",
            gap_weight = 0,
            restricted_chars = "_T"
            )
    
    data = decode_query(query)

    # modify floats and the like
    for k,v in data.items():
        if type(v) == str:
            try:
                data[k] = float(v)
            except ValueError:
                try:
                    data[k] = int(v)
                except ValueError:
                    data[k] = v
    
    # check for vowel merge
    if 'merge_vowels' in data:
        data['merge_vowels'] = eval(data['merge_vowels'])

    # parse defaults 
    for k in defaults:
        if k not in data:
            data[k] = defaults[k]
    
    # check for input format
    if 'seqs' in data:
        msa = Multiple(data['seqs'], merge_vowels=data['merge_vowels'])
    elif 'file' in data:
        msa = MSA(normalize_path('../data/msa/'+data['file']))
    
    # check which mode
    if data['method'] == 'progressive':
        msa.prog_align(**data)
    else:
        msa.lib_align(**data)

    # check for post-processing
    if 'iterate_orphans' in data:
        msa.iterate_orphans(0.5)
    if 'iterate_similar_gap_sites' in data:
        msa.iterate_similar_gap_sites()
    if 'iterate_clusters' in data:
        msa.iterate_clusters(0.5)
    if 'iterate_all_sequences' in data:
        msa.iterate_all_sequences()

    # get sum of pairs
    data['pid'] = msa.get_pid()

    # serialize the data (actually not needed right now)
    data['alignments'] = msa.alm_matrix
    data['type'] = 'msa'

    url = encode_query(data)

    txt = '\n'.join([' '.join(alm) for alm in data['alignments']])
    txt += '\n@PID: {0}'.format(int(100 * data['pid']))
    
    # pass the object reference to rcParams to make it retrievable in other
    # applications
    rcParams['msa'] = msa

    return txt 
