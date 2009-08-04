from ctypes import CDLL
from ctypes.util import find_library
from ctypes import c_char_p


from sys import platform

from pygl.constants import EXTENSIONS
from pygl.gltypes import GLenum

lib = None

if 'linux' in platform:
    lib = CDLL(find_library('GL'))
elif platform == 'win32':
    raise RuntimeError('No')

GetString = lib.glGetString
GetString.argtypes = [GLenum]
GetString.restype = c_char_p

def _is_extension_supported(name):
    extension_string = GetString(EXTENSIONS).value

    extensions = extension_string.split()

    if name in extensions: return True

    return False
    

class ExtensionError(RuntimeError): pass

class Extension(object):
    def __init__(self, name, symbols):
        if not _is_extension_supported(name) and name:
            raise ExtensionError('Extension \'%s\' not supported.' % name)
        self.name = name

        for name, symbol in symbols:
            f = getattr(lib, symbol[0])
            f.argtypes = symbol[1]
            f.restype = symbol[2]
            setattr(self, name, f)

class Functionality(object):
    def __init__(self, extensions):
        for name, symbols in extensions.iteritems():
            try:
                Extension.__init__(self, name, symbols)
                break
            except ExtensionError: continue
