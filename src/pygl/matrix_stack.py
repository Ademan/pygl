from ctypes import POINTER, c_float, c_double

from pygl.constants import GL_MODELVIEW, GL_PROJECTION

from pygl._gl import lib as _gl

from pygl.util import _norm_args

_matrixf = c_float * 16
_matrixfp = POINTER(c_float)

_matrixd = c_double * 16
_matrixdp = POINTER(c_double)

class MatrixStack(object): pass

class FixedFunctionMatrixStack(MatrixStack):
    def _set_mode(self):
        #TODO: query old mode?
        #TODO: optional direct state access?
        _gl.glMatrixMode(self.matrix_mode)

    def push(self):
        self._set_mode()
        _gl.glPushMatrix()

    def pop(self):
        self._set_mode()
        _gl.glPopMatrix()

    #TODO: load and __mul__ duplicate code
    def load(self, *args):
        values = _norm_args(args)
        array = _matrixd(values)
        _gl.glLoadMatrixdv(_matrixdp(array))

    #TODO: how to support ctx.stack *= matrix ?
    def __mul__(self, *args):
        values = _norm_args(args)
        array = _matrixd(matrix)
        _gl.glMultMatrixdv(_matrixdp(array))
        return self

class ModelviewMatrixStack(FixedFunctionMatrixStack):
    def __init__(self):
        self.matrix_mode = GL_MODELVIEW

class ProjectionMatrixStack(FixedFunctionMatrixStack):
    def __init__(self):
        self.matrix_mode = GL_PROJECTION
