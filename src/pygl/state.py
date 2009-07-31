from pygl.gltypes import GLenum, GLint
from pygl._gl import lib as _gl

from pygl.constants import MATRIX_MODE

from ctypes import POINTER

_gl.glGetIntegerv.args = [GLenum, POINTER(GLint)]
_gl.glGetIntegerv.result = None

class PreserveState(object):
    def __enter__(self):
        self._save = self.state

    def __exit__(self, exc_type, exc_value, exc_tb):
        #TODO: make more robust
        self.state = self._save

class MatrixModeState(object):
    def __get__(self):
        result = GLenum(0)
        _gl.glGetIntegerv(MATRIX_MODE, POINTER(result))
        return result
    def __set__(self, value):
        _gl.glMatrixMode(value)

class PreserveMatrixMode(PreserveState):
    _state = MatrixModeState()

#TODO: is this reliable?
def _query_from_binding(binding):
    return GLuint(binding + 0x7288)

class TextureBindingState(object):
    def __init__(self, binding):
        self.binding = binding
    def __get__(self):
        texture = GLenum(0)
        _gl.glGetIntegerv(_query_from_binding(self.binding), POINTER(texture))
    def __set__(self, value):
        _gl.glBindTexture(self.binding, value)

class PreserveTextureBinding(PreserveState):
    def __init__(self, binding):
        self._state = TextureBindingState(binding)
