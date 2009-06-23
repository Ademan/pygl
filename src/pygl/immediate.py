from pygl._gl import lib as _gl

from pygl.constants import GL_TRIANGLES, GL_QUADS

from ctypes import c_int, c_float, c_double

from pygl.util import _norm_args

def _vertex_data(format, dtype, min, max, args):
    print args
    args = _norm_args(args)
    print args
    assert len(args) >= min
    assert len(args) <= max
    getattr(_gl, format % len(args))(*map(dtype, args))

_typenames = {
    c_double: 'd',
    c_float: 'f',
    c_int: 'i'
    }

_immediate_functions = {
    "vertex": ("glVertex%d%c", [c_double, c_float, c_int],
                               [2, 3, 4]),
    "color": ("glColor%d%c", [c_double, c_float, c_int],
                               [3, 4]),
    "texcoord": ("glTexcoord%d%c", [c_double, c_float, c_int],
                               [1, 2, 3, 4]),
    "normal": ("glNormal%d%c", [c_double, c_float],
                               [3]),
                       }

#TODO: switch to dictionary?

class ImmediateMode(object):
    def vertex(self, *args):
        return _vertex_data("glVertex%dd", c_double, 2, 4, args)
    def color(self, *args):
        print args
        return _vertex_data("glColor%dd", c_double, 3, 3, args)
    def texcoord(self, *args):
        #FIXME: right function name?
        #FIXME: yes I know technically texcoords can be other than 2 component
        return _vertex_data("glTexCoord%dd", c_double, 2, 2, args)
    def __exit__(self, exc_type, exc_val, exc_tb):
        _gl.glEnd()

class TrianglesMode(ImmediateMode):
    def __enter__(self):
        _gl.glBegin(GL_TRIANGLES)
        return self

class QuadsMode(ImmediateMode):
    def __enter__(self):
        _gl.glBegin(GL_QUADS)
        return self
