from ctypes import CDLL
from ctypes.util import find_library
from ctypes import c_char_p

from sys import platform
from os import environ

from pygl.constants import EXTENSIONS
from pygl.gltypes import GLenum

lib = None

if 'linux' in platform:
    if 'USE_BUGLE' in environ:
        lib = CDLL(find_library('libbugle.so')) #FIXME: debug
    else:
        lib = CDLL(find_library('GL'))
elif platform == 'win32':
    raise RuntimeError('No')

Enable = lib.glEnable
Enable.argtypes = [GLenum]

Disable = lib.glDisable
Disable.argtypes = [GLenum]

GetString = lib.glGetString
GetString.argtypes = [GLenum]
GetString.restype = c_char_p

def _is_extension_supported(name):
    extension_string = GetString(EXTENSIONS)

    extensions = extension_string.split()

    if name in extensions: return True

    return False
    

class ExtensionError(RuntimeError): pass

class Extension(object):
    def __init__(self, name, symbols):
        if not name == '':
            if not _is_extension_supported(name):
                raise ExtensionError('Extension \'%s\' not supported.' % name)
            self.name = name

        for name, symbol in symbols.iteritems():
            f = getattr(lib, symbol[0])
            f.argtypes = symbol[1]
            f.restype = symbol[2]
            setattr(self, name, f)

class Functionality(Extension):
    def __init__(self, extensions):
        for name, symbols in extensions.iteritems():
            try:
                Extension.__init__(self, name, symbols)
                break
            except ExtensionError: continue

def function(name, argtypes, restype=None, names=["gl%(name)s", "gl%(name)sARB", "gl%(name)sEXT"]):
    for symbol in [name_format % {'name': name} for name_format in names]:
        try:
            f = getattr(lib, symbol)
            f.argtypes = argtypes
            f.restype = restype
            return f
        except AttributeError: continue
