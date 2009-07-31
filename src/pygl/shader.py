from _gl import lib as _gl

try:
    CreateShaderObject = _gl.glCreateShaderObject
except:
    CreateShaderObject = _gl.glCreateShaderObjectARB

class Shader(object):
    def __init__(self):
        self._object = 
                
