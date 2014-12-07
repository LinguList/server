# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-12-05 10:42
# modified : 2014-12-05 10:42
"""
Handle different filetypes in LingPy-Server.
"""

__author__="Johann-Mattis List"
__date__="2014-12-05"

import markdown
import os

from .settings import rcParams


def handle_markdown(path):
    """
    Function loads the headers and footers and servers markdown as html.
    """
    
    # get the real path
    real_path = os.path.join(rcParams['markdown'], path)

    if not os.path.exists(real_path):
        return '404 FNF'
    else:
        # first load the path
        with open(real_path) as f:
            content = ''
            settings = {}
            # find the basic information regarding the site
            for line in f:
                if line.startswith('@'):
                    key = line[1:line.index(':')]
                    val = line[line.index(':')+1:].strip()
                    if key not in ['js', 'css']:
                        settings[key] = val
                    else:
                        settings[key] = val.split(',')
                else:
                    content += line

            # convert to markdown
            content = markdown.markdown(content)
            
            # load the templates
            head = open('layouts/'+settings['head']+'.head').read()
            header = open('layouts/'+settings['header']+'.header').read()
            body = open('layouts/'+settings['body']+'.body').read()
            footer = open('layouts/'+settings['footer']+'.footer').read()
            
            # add js and css
            js = '\n'.join(['<script src="js/'+j+'.js"></script>' for j in settings['js']])
            css = '\n'.join(['<link type="text/css" rel="stylesheet" href="css/'+j+'.css" />' for j
                in settings['css']])

            head = head.format(scripts='',styles=css, title=settings['title'])
            footer = footer.format(scripts=js)

            html = body.format(content=content, head=head, footer=footer,
                    header=header)

            return html

