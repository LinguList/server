# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-12-05 10:35
# modified : 2014-12-05 10:35
"""
Module provides basic handlers for queries.
"""

__author__="Johann-Mattis List"
__date__="2014-12-05"

import urllib
from .settings import SETTINGS

def split_url(url):
    """
    Function handles parsing of url strings.
    """
    
    # parse the url
    parsed_url = urllib.parse.urlparse(url)
    
    # debug
    print('@SPLIT_URL',parsed_url)
    
    # get query
    query = parsed_url[4]
    
    # get file path
    path = parsed_url[2]

    # get fragment
    fragment = parsed_url[5]

    return path, query, fragment

def decode_query(query):
    """
    function decodes url queries.
    """

    # get the object if a query is present
    if query:
        data = urllib.parse.parse_qs(query)
        for k in data:
            if len(data[k]) == 1:
                data[k] = data[k][0]
    else:
        data = {}

    return data

def encode_query(thing):
    """
    Function converts python objects to url code.
    """

    url = urllib.parse.urlencode(thing, doseq=True)
    return url

def remote(query, auth=False):
    """
    Conduct a remote query using Pythons urllib.
    """
    
    data = decode_query(query)
    url = data['url']
    
    print('@REMOTE',url)
    
    if not auth:
        request = urllib_request.urlopen(url)
        txt = request.read()
    else:
        # following example from https://docs.python.org/3.1/howto/urllib2.html
        pwm = urllib_request.HTTPPasswordMgrWithDefaultRealm()
        tlu = url
        
        # get password from user
        if not SETTINGS['pwd'] or not SETTINGS['user']:
            user = getpass.getpass(prompt='Username: ')
            pwd = getpass.getpass()
            SETTINGS['user'] = user
            SETTINGS['pwd'] = pwd
        else:
            user = SETTINGS['user']
            pwd = SETTINGS['pwd']

        pwm.add_password(None, tlu, user, pwd)

        handler = urllib_request.HTTPBasicAuthHandler(pwm)
        opener = urllib_request.build_opener(handler)

        request = opener.open(url)
        txt = request.read()

    return txt

