from pygl.gltypes import GLdouble
from pygl._gl import lib as _gl

from ctypes import c_uint, POINTER

def _norm_args(*args):
    if len(args) == 1:
        args = args[0]
    return args

def _get_integer(flag): #FIXME: should this even exist?
    result = c_uint(0)
    _gl.glGetIntegerv(c_uint(flag), POINTER(result))
    return result.value

def _split_enum_name(name):
    return name.split('_')

def _cap_word(word):
    return ''.join([word[0].upper(), word[1:]])

def _cap_name(name):
    return ''.join(map(_cap_word, name))

Rotate = _gl.glRotated
Rotate.argtypes = [GLdouble] * 4

Translate = _gl.glTranslated
Translate.argtypes = [GLdouble] * 3

Scale = _gl.glScaled
Scale.argtypes = [GLdouble] * 3
