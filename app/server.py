# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-11-28 11:13
# modified : 2014-11-28 11:13
"""
Server integration of LingPy.

Notes
-----
This is the attempt to provide a GUI access to LingPy's basic functionalities
using an HTTP server along with HTML and JavaScript.
"""

__author__="Johann-Mattis List"
__date__="2014-11-28"

from lingpy import *
from lingpy.convert.html import *
from lingpy.convert.strings import *
import lingpy

import time
import http.server as server
import webbrowser
import multiprocessing
import os

import urllib
from urllib import request as urllib_request
import html.parser as parser
import json
import cgi
import signal
import getpass

# import markdown module for easy markdown handling
#import markdown

# internal imports
from code.files import handle_markdown
from code.settings import SETTINGS, rcParams, modify_segmentation,\
        show_segmentations, load_segmentation, show_data
from code.align import pairwise, multiple
from code.query import *


# code example taken and modified to account for py3 from
# https://wiki.python.org/moin/BaseHttpServer


HOST_NAME = '' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.

class MyHandler(server.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        
        # debug
        print('@GET:',s.path)
        
        # split the path
        path, query, fragment = split_url(s.path)

        # prepare headers, needs refinement for more stuff apart from css, html
        s.send_response(200)

        if path.endswith('.css'):
            s.send_header("Content-type", "text/css")
        else:
            s.send_header("Content-type", "text/html")
        s.end_headers()
        
        # serve msa and psa output if the path ends on .msa
        if path.endswith('.msa'):
            msa = multiple(query)
            s.wfile.write(bytes(msa,'utf-8'))

        elif path.endswith('.psa'):
            psa = pairwise(query)
            s.wfile.write(bytes(psa, 'utf-8'))
        
        # serve markdown (basic) output in html if path ends with .md
        elif path.endswith('.md'):
            new_path = '.'+path.replace('/', os.sep)
            html = handle_markdown(new_path)
            s.wfile.write(bytes(html, 'utf-8'))
        
        # break the server on .stop
        elif path.endswith('.stop'):
            
            s.wfile.write(b"<p><b>Server was shut down.<b></p>")
            p = SETTINGS['server']
            os.kill(p.pid, signal.SIGKILL)
        
        # allow for remote access using remote queries
        elif path.endswith('.remote'):
            txt = remote(query)
            s.wfile.write(txt)
        
        # specific output for the edictor, needs refinement
        elif 'triples.php' in path:
            query = 'url=http://tsv.lingpy.org/triples/triples.php?'+query
            txt = remote(query)
            s.wfile.write(txt)
            
        elif 'update.php' in path:
            qob = {}
            qob['url'] = 'http://tsv.lingpy.org/triples/update.php?'+query
            query = encode_query(qob)

            print('UPDATE',query)
            #queryn = 'url=http://tsv.lingpy.org/triples/update.php?'+query
            txt = remote(query, auth=True)
            s.wfile.write(txt)
        
        # if the path ends with ".rc" we serve lingpy.settings.rcParams as json
        elif path.endswith('.rc'):
            
            d = {}
            for k,v in rcParams.items():
                if isinstance(v, lingpy.data.model.Model):
                    V = v.name
                else:
                    V = str(v)
                d[str(k)] = V

            txt = json.dumps(d)
            s.wfile.write(bytes(txt, 'utf-8'))
        
        # settings is the ending to change various settings by modifying
        # lingpy.settings.rcParams
        elif path.endswith('.settings'):
            
            val = decode_query(query)
            
            # we check for the type argument of the queries to distinguish
            # different types

            # store_segmentation means storing a specific setting for vowels,
            # diacritics, and the like, which is used in ipa2tokens of
            # lingpy.sequence.sound_classes
            if val['type'] == 'store_segmentation':

                # XXX we need a real handler here
                val_string = json.dumps(val)

                with open(
                        os.path.join('settings','segmentation',val['name']+'.json'),
                        'w'
                        ) as f:
                    f.write(val_string)

                # dummy output
                s.wfile.write(b'success')

            # modify segmentation modifies the current standard segmentation
            # settings in rcParams
            elif val['type'] == 'modify_segmentation':
                
                modify_segmentation(val)
                s.wfile.write(b'modified\n')
            
            # return all segmentations in settings.segmentation (encoded as
            # json)
            elif val['type'] == 'show_segmentations':

                s.wfile.write(bytes(show_segmentations(),'utf-8'))
            
            # load a given segmentation and return it as json
            elif val['type'] == 'load_segmentation':

                s.wfile.write( bytes( load_segmentation(val['schema']), 
                    'utf-8'))

            # modify a given sound class model
            elif val['type'] == 'load_sound_classes':

                s.wfile.write(bytes(load_sound_classes(val['schema']),
                    'utf-8'))


            # retrieve basic data for available data
            elif val['type'] == 'show_data':

                s.wfile.write(bytes(show_data(val['format']),'utf-8'))
        
        # serve normal output for traditional path endings
        elif True in [path.endswith(x) for x in [
            '.html',
            '.js',
            '.css',
            '.txt',
            '.svg',
            '.tsv',
            '.csv'
            ]]:
            
            try:
                # change the path to find the right way
                new_path = '.'+path.replace('/',os.sep)
                with open(new_path) as f:
                    data = f.read()
                    s.wfile.write(bytes(data,'utf-8'))
            # if we don't find the file, we search in the home directory
            except FileNotFoundError:
                try:
                    new_path = SETTINGS['home'] + path.replace('/', os.sep)
                    with open(new_path) as f:
                        data = f.read()
                        s.wfile.write(bytes(data, 'utf-8'))
                except FileNotFoundError:
                    s.wfile.write(b'404 FNF')
        
        # serve binary if this is suggested by endings
        elif True in [path.endswith(x) for x in [
            '.png',
            '.ttf',
            '.bin',
            '.jpg'
            ]]:

            new_path = '.'+path.replace('/', os.sep)
            with open(new_path, 'rb') as f:
                data = f.read()
                s.wfile.write(data)
                
if __name__ == '__main__':
  
    server_class = server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    # start multiprocessing functionalities
    # we use two processes: one for the server, and one to open the webbrowser
    # at the correct localhost-address
    # this can also be used to make sure that we can stop the server once a
    # button is pressed, since we know the browser and the like
    p1 = multiprocessing.Process(
            target = lambda x: x.serve_forever(),
            args = [httpd]
            )
    p2 = multiprocessing.Process(
            target = lambda x: webbrowser.open(x),
            args = ['http://localhost:9000/index.md']
            )
    SETTINGS['server'] = p1
    
    from sys import argv
    if 'start' in argv:
        p1.start()
        p2.start()

