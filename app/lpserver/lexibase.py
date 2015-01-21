# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-01-14 12:16
# modified : 2015-01-19 13:37
"""
An extended wordlist construct that can be loaded from sqlite3, triple files,
etc.
"""

__author__="Johann-Mattis List"
__date__="2015-01-19"

import lingpyd as lingpy
import sqlite3
import os
import datetime
try:
    import wget
except ImportError:
    print("Module wget could not be loaded, some features may not work properly.")

def load_sqlite(table, dbase, url=False, out=False):
    """
    Retrieve triples from an sqlite3 database.
    """
    if url:
        # check if file already exists
        if os.path.isfile(dbase):
            os.rename(
                    dbase,
                    dbase+'-backup-'+str(datetime.datetime.now()).split('.')[0]
                    )
        wget.download(url, out=dbase)
        
    db = sqlite3.connect(dbase)
    cursor = db.cursor()

    cursor.execute('select * from '+table+';')

    data = cursor.fetchall()
    
    return lingpy.basic.ops.triple2tsv(data, output='dict')

def make_lexibase(list_of_taxa, list_of_concepts, entries, filename='template'):
    """
    Function creates a new LexiBase tsv-file from a list of concepts and a list
    of taxa specified by the user.
    """
    lot = lingpy.csv2list(list_of_taxa)
    loc = lingpy.csv2list(list_of_concepts)
    
    # determine the nature of the header by reading first line of lot and loc
    header = []
    header += [x.upper() for x in loc[0]]
    header += [x.upper() for x in lot[0]]
    header += [x.upper() for x in entries]

    # append the appendix for the individual fields
    fields = []
    for h in entries:
        if not h.endswith('ID'):
            fields += ['-']
        else:
            fields += ['0']

    # dermine index of main gloss
    cidx = [x.upper() for x in loc[0]].index('CONCEPT')
    tidx = [x.upper() for x in lot[0]].index('DOCULECT')

    # make text object
    text = ''
    text += 'ID'+'\t'+'\t'.join(header)+'\n'
    idx = 1

    for i in range(len(loc)-1):
        for j in range(len(lot)-1):
            print(idx,i,j)
            tmp = str(idx)+'\t'
            tmp += '\t'.join(loc[i+1])+'\t'
            tmp += '\t'.join(lot[j+1])+'\t'
            tmp += '\t'.join(fields)+'\n'
            idx += 1
            text += tmp
        text += '#\n'
    with open(filename+'.tsv', 'w') as f:
        f.write(text)
    
class LexiBase(lingpy.basic.wordlist.Wordlist):

    def __init__(self, infile, **keywords):
        
        if type(infile) == dict:
            lingpy.basic.wordlist.Wordlist.__init__(self, infile, **keywords)  
        elif infile.endswith('.triples'):
            D = lingpy.basic.ops.triple2tsv(infile, output='dict', **keywords)

            lingpy.basic.wordlist.Wordlist.__init__(self, D)
        elif 'dbase' in keywords:
            D = load_sqlite(infile, **keywords)
            self.dbase = keywords['dbase']
            lingpy.basic.wordlist.Wordlist.__init__(self, D)
        else:
            lingpy.basic.wordlist.Wordlist.__init__(self,infile, **keywords)
    
    def tokenize(self, override=True, preprocessing=False):

        if not preprocessing:
            preprocessing = lambda x: x

        self.add_entries('tokens', 'ipa', lambda x:
                lingpy.ipa2tokens(preprocessing(x)),override=override)

        self.add_entries('prostring','tokens', lambda x: lingpyd.prosodic_string(x,
            _output='CcV'), override)

        self.add_entries('tokens', 'tokens', lambda x: secondary_structures(x),
                override = override)
    def update(self, table, dbase=None, ignore=False, verbose=False):
        """
        Upload all data which was modified in the current session to the
        database, don't change those entries which have not been touched.
        """
        
        # handle kws
        dbase = dbase or self.dbase
        ignore = ignore or []
        
        # iterate over all entries in the wl, check if they have been modified
        # and update the db if this is the case, make also a note in the backup
        # file that an automatic parse has been done
        self._clean_cache()
        triples = sorted(
                lingpy.basic.ops.tsv2triple(self, False))

        # connect to dbase
        db = sqlite3.connect(dbase)
        cursor = db.cursor()
        
        # get all triples from db
        cursor.execute('select * from '+table+' order by ID,COL,VAL;')
        data = cursor.fetchall()
        # make dict from data
        datad = dict([((a,b),c) for a,b,c in data])
        print(len(datad),len(triples))
        
        modified = 0
        tobemodified = []
        tobebackedup = []
        time = int(datetime.datetime.now().timestamp())

        for line in triples:
             
            if not (line[0],line[1]) in datad or datad[line[0],line[1]] != line[2]:
                bak = False
                if (line[0],line[1]) in datad:
                    tobemodified += [line]
                    bak = True
                    print('yes')

                if (line[0],line[1]) not in datad and line[2] != '':
                    datad[line[0],line[1]] = ''
                    tobemodified += [line]
                    bak = True
                    
                if bak:
                    tobebackedup += [[table]+list(line[:2])+[datad[line[0],line[1]],time,'lingpy']]
                
        cursor.execute('delete from '+table+' where ID|":"|COL in ('+
                ','.join(['"{0}:{1}"'.format(a,b) for a,b,c in
                    tobemodified])+');')

        for a,b,c in tobemodified:
            if verbose:
                print("[i] Inserting value {0} for ID={1} and COL={2}...".format(c,a,b))
            cursor.execute('insert into '+table+' values(?,?,?);',
                    (a,b,c)
                    )
            modified += 1
        for line in tobebackedup:
            cursor.execute('insert into backup values(?,?,?,?,?,?);',
                    tuple(line))
        cursor.execute('vacuum')
        db.commit()
        print("Automatically modified {0} cells in the data.".format(modified))
        


    
    def create(self, table, dbase=None, ignore=False):
        """
        Upload triple-data to sqlite3-db. Thereby, delete the previous table
        if it is still in the database.
        """
        if not dbase:
            dbase = self.dbase

        if not ignore: ignore=[]
        # get the triples
        triples = lingpy.basic.ops.tsv2triple(self,False)
        
        # connect to tatabase
        db = sqlite3.connect(dbase)
        cursor = db.cursor()

        try:
            cursor.execute('drop table '+table+';')
        except sqlite3.OperationalError:
            pass
        cursor.execute('create table '+table+' (ID int, COL text, VAL text);')
        cursor.execute('vacuum')

        for a,b,c in triples:
            if b.lower() not in ignore:
                if type(c) == list:
                    c = ' '.join([str(x) for x in c])
                else:
                    c = str(c)
                cursor.execute('insert into '+table+' values (?, ?, ?);', (a, b, c))
        db.commit()
