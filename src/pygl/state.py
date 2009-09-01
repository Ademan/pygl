from pygl.gltypes import GLenum, GLint
from pygl.gltypes import GLuint
from pygl._gl import lib as _gl

from pygl.constants import MATRIX_MODE

from pygl.util import _lookup_enum

from pygl.glerror import _check_errors

from ctypes import POINTER

_gl.glGetIntegerv.args = [GLenum, POINTER(GLint)]
_gl.glGetIntegerv.result = None

class PreserveState(object):
    def __enter__(self):
        self._save = self.state
        return self

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
    state = MatrixModeState()

#TODO: is this reliable?
def _query_from_binding(binding):
    return GLuint(binding.value + 0x7288)

GetInteger = _gl.glGetIntegerv
GetInteger.argtypes = [GLenum, POINTER(GLint)]

BindTexture = _gl.glBindTexture
BindTexture.argtypes = [GLenum, GLuint]

class TextureBindingState(object):
    def _get_binding(self, instance):
        return instance._texture._binding
    def __get__(self, instance, owner):
        texture = GLint(0) #FIXME: textures are GLuints... but GetInteger is integers only
        GetInteger(_query_from_binding(self._get_binding(instance)), texture)
        _check_errors()
        return texture.value

    def __set__(self, instance, value):
        BindTexture(self._get_binding(instance), value)
        _check_errors()

class PreserveTextureBinding(PreserveState):
    state = TextureBindingState()
    def __init__(self, texture):
        self._texture = texture
