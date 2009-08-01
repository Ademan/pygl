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
