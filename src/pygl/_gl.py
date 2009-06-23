from ctypes import CDLL
from ctypes.util import find_library

from sys import platform

lib = None

if 'linux' in platform:
    lib = CDLL(find_library('GL'))
elif platform == 'win32':
    raise RuntimeError('No')
