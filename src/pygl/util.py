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

def _lookup_enum(value):
    from pygl import constants
    try:
        value = value.value
    except AttributeError: pass

    results = []
    try:
        for constant in dir(constants):
            if getattr(constants, constant).value == value:
                results.append(constant)
    except: pass

    return results[0] if len(results) == 1 else results

def _debug_enum(name, value):
    print "%s:" % name, ' = '.join(map(str, [_lookup_enum(value), value.value]))
