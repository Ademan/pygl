from pygl._gl import lib as _gl

#from pygl.constants import
from pygl.gltypes import GLext, GLuint

try:
    CreateShaderObject = _gl.glCreateShaderObject
except:
    CreateShaderObject = _gl.glCreateShaderObjectARB

    CreateShaderObject.args = [GLenum]
    CreateShaderObject.result = GLuint


class Shader(object):
    def __init__(self):
        self._object = 
                
