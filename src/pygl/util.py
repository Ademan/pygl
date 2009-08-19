#FIXME: eventually sort all of these functions
from pygl.gltypes import GLdouble
from pygl.gltypes import GLenum
from pygl.gltypes import GLint
from pygl._gl import lib as _gl

from ctypes import POINTER

from pygl.glerror import _check_errors

def _norm_args(*args):
    if len(args) == 1:
        args = args[0]
    return args

def _split_enum_name(name):
    return name.split('_')

def _cap_word(word):
    return ''.join([word[0].upper(), word[1:]])

def _cap_name(name):
    return ''.join(map(_cap_word, name))


GetInteger = _gl.glGetIntegerv
GetInteger.argtypes = [GLenum, POINTER(GLint)]

def _get_integer(flag):
    value = GLint(0)
    GetInteger(flag, value)
    _check_errors()
    return value.value

Rotate = _gl.glRotated
Rotate.argtypes = [GLdouble] * 4

Translate = _gl.glTranslated
Translate.argtypes = [GLdouble] * 3

Scale = _gl.glScaled
Scale.argtypes = [GLdouble] * 3
