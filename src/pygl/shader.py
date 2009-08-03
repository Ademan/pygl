from pygl._gl import lib as _gl

from pygl.gltypes import GLext, GLuint
from ctypes import c_char_p as c_str

from pygl.constants import

shaders = Extensions({
                      '': {'CreateShaderObject': 'glCreateShaderObject',
                           'ShaderSource': 'glShaderSource'},
                      'GL_ARB_shader_objects': ['glCreateShaderObjectARB', 'glShaderSourceARB']
                     })

CreateShaderObject = shaders.CreateShaderObject
CreateShaderObject.args = [GLenum]
CreateShaderObject.result = GLuint

#CreateProgram
#LinkProgram

ShaderSource = shaders.ShaderSource

class Shader(object):
    def __init__(self):
        self._object = CreateShaderObject(self._shader_type)

    def _stringify(self, source):
        stringified = str(source)
        if source == stringified:
            #FIXME: is this really an ok test for string-likeness?
            return source
        else:
            return ''.join([line for line in source])

    @property
    def sources(self): pass
        #TODO: GetSources()

    @sources.setter
    def sources(self, sources):
        c_str_array = (c_str * len(sources))(*[
                                                c_str(''.join(source)) if hasattr(source, 'read')
                                                    else c_str(source)
                                                        for source in sources
                                              ])
        ShaderSource(self._object,
                     len(sources),
                     c_str_array,
                     NULL) #FIXME: need NULL

class VertexShader(Shader): pass

class FragmentShader(Shader): pass
