from pygl.gltypes import GLdouble

from ctypes import CDLL
from ctypes.util import find_library

from sys import platform

if 'linux' in platform:
    lib = CDLL(find_library('GLU'))
elif platform == 'win32':
    raise RuntimeError('No')

Perspective = lib.gluPerspective
Perspective.argtypes = [GLdouble] * 4
