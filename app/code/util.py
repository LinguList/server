# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-12-05 22:36
# modified : 2014-12-05 22:36
"""
Utility functions for LingPy Server.
"""

__author__="Johann-Mattis List"
__date__="2014-12-05"

from glob import glob
import io
import unicodedata
import os
from pathlib import Path

def lines_to_text(lines):
    return ''.join(line if line.endswith('\n') else line + '\n' for line in lines)

# function forked from @xrotwang's addons to LingPy
def _str_path(path, mkdir=False):
    """Get a file-system path as text_type, suitable for passing into io.open.

    :param path: A fs path either as Path instance or as text_type.
    :param mkdir: If True, create the directories within the path.
    :return: The path as text_type.
    """
    res = text_type(path) if isinstance(path, Path) else path
    if mkdir:
        dirname = os.path.dirname(res)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
    return res

def normalize_path(path):
    """Normalize a path for different platforms."""
    return os.path.join(*path.split('/'))

def write_text_file(path, content, normalize=None):
    """Write a text file encoded in utf-8.

    :param path: File-system path of the file.
    :content: The text content to be written.
    :param normalize: If not `None` a valid unicode normalization mode must be passed.
    """
    # modify path to be usable in windows
    path = normalize_path(path)
    
    if not isinstance(content, text_type):
        content = lines_to_text(content)
    with io.open(_str_path(path, mkdir=True), 'w', encoding='utf8') as fp:
        fp.write(unicodedata.normalize(normalize, content) if normalize else content)

def read_text_file(path, normalize=None, lines=False):
    """Read a text file encoded in utf-8.

    :param path: File-system path of the file.
    :param normalize: If not `None` a valid unicode normalization mode must be passed.
    :param lines: Flag signalling whether to return a list of lines.
    :return: File content as unicode object or list of lines as unicode objects.

    .. note:: The whole file is read into memory.
    """
    
    # modify path to be usable in windoof
    path = normalize_path(path)

    def _normalize(chunk):
        return unicodedata.normalize(normalize, chunk) if normalize else chunk

    with io.open(_str_path(path), 'r', encoding='utf8') as fp:
        if lines:
            return [_normalize(line) for line in fp]
        else:
            return _normalize(fp.read())
