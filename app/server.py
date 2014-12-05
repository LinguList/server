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

from lingpyd import *
from lingpyd.convert.html import *
from lingpyd.convert.strings import *

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
from code.settings import SETTINGS
from code.align import pairwise, multiple
from code.query import *


# code example taken and modified to account for py3 from
# https://wiki.python.org/moin/BaseHttpServer


HOST_NAME = '' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.

#SETTINGS = {}
#SETTINGS['root'] = '.'
#SETTINGS['server'] = 0
#SETTINGS['user'] = ''
#SETTINGS['pwd'] = ''
#
## get the home path of the home directory, tip taken from http://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
#SETTINGS['home'] = os.path.expanduser('~')

#def split_url(url):
#    """
#    Function handles parsing of url strings.
#    """
#    
#    # parse the url
#    parsed_url = urllib.parse.urlparse(url)
#    
#    # debug
#    print('@SPLIT_URL',parsed_url)
#    
#    # get query
#    query = parsed_url[4]
#    
#    # get file path
#    path = parsed_url[2]
#
#    # get fragment
#    fragment = parsed_url[5]
#
#    return path, query, fragment
#
#def decode_query(query):
#    """
#    function decodes url queries.
#    """
#
#    # get the object if a query is present
#    if query:
#        data = urllib.parse.parse_qs(query)
#        for k in data:
#            if len(data[k]) == 1:
#                data[k] = data[k][0]
#    else:
#        data = {}
#
#    return data
#
#def encode_query(thing):
#    """
#    Function converts python objects to url code.
#    """
#
#    url = urllib.parse.urlencode(thing, doseq=True)
#    return url
#
#def remote(query, auth=False):
#    """
#    Conduct a remote query using Pythons urllib.
#    """
#    
#    data = decode_query(query)
#    url = data['url']
#    
#    print('@REMOTE',url)
#    
#    if not auth:
#        request = urllib_request.urlopen(url)
#        txt = request.read()
#    else:
#        # following example from https://docs.python.org/3.1/howto/urllib2.html
#        pwm = urllib_request.HTTPPasswordMgrWithDefaultRealm()
#        tlu = url
#        
#        # get password from user
#        if not SETTINGS['pwd'] or not SETTINGS['user']:
#            user = getpass.getpass(prompt='Username: ')
#            pwd = getpass.getpass()
#            SETTINGS['user'] = user
#            SETTINGS['pwd'] = pwd
#        else:
#            user = SETTINGS['user']
#            pwd = SETTINGS['pwd']
#
#        pwm.add_password(None, tlu, user, pwd)
#
#        handler = urllib_request.HTTPBasicAuthHandler(pwm)
#        opener = urllib_request.build_opener(handler)
#
#        request = opener.open(url)
#        txt = request.read()
#
#    return txt


#def prepare_markdown(path):
#    """
#    Function loads the headers and footers and servers markdown as html.
#    """
#    
#    if not os.path.exists(path):
#        return '404 FNF'
#    else:
#        # first load the path
#        with open(path) as f:
#            content = ''
#            settings = {}
#            # find the basic information regarding the site
#            for line in f:
#                if line.startswith('@'):
#                    key = line[1:line.index(':')]
#                    val = line[line.index(':')+1:].strip()
#                    if key not in ['js', 'css']:
#                        settings[key] = val
#                    else:
#                        settings[key] = val.split(',')
#                else:
#                    content += line
#            # convert to markdown
#            content = markdown.markdown(content)
#            
#            # load the templates
#            head = open('layouts/'+settings['head']+'.head').read()
#            header = open('layouts/'+settings['header']+'.header').read()
#            body = open('layouts/'+settings['body']+'.body').read()
#            footer = open('layouts/'+settings['footer']+'.footer').read()
#            
#            # add js and css
#            js = '\n'.join(['<script src="js/'+j+'.js"></script>' for j in settings['js']])
#            css = '\n'.join(['<link type="text/css" rel="stylesheet" href="css/'+j+'.css" />' for j
#                in settings['css']])
#
#            head = head.format(scripts=js, styles=css, title=settings['title'])
#
#            html = body.format(content=content, head=head, footer=footer,
#                    header=header)
#
#            return html

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

        # prepare headers
        s.send_response(200)

        if path.endswith('.css'):
            s.send_header("Content-type", "text/css")
        else:
            s.send_header("Content-type", "text/html")
        s.end_headers()
        
        # serve msa output if the path ends on .msa
        if path.endswith('.msa'):
            msa = multiple(query)
            s.wfile.write(bytes(msa,'utf-8'))

        elif path.endswith('.psa'):
            psa = pairwise(query)
            s.wfile.write(bytes(psa, 'utf-8'))

        elif path.endswith('.md'):
            new_path = '.'+path.replace('/', os.sep)
            html = handle_markdown(new_path)
            s.wfile.write(bytes(html, 'utf-8'))

        elif path.endswith('.stop'):
            
            s.wfile.write(b"<p><b>Server was shut down.<b></p>")
            p = SETTINGS['server']
            os.kill(p.pid, signal.SIGKILL)

        elif path.endswith('.remote'):
            txt = remote(query)
            s.wfile.write(txt)

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

