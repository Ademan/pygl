from pygl._gl import lib as _gl

from pygl.gltypes import GLext, GLuint
from pygl.gltypes import NULL
from ctypes import c_char_p as c_str

from pygl.constants import VERTEX_SHADER, FRAGMENT_SHADER

shader = Functionality({
                      '': {
                              'CreateShader': ('glCreateShader', [GLenum], GLuint),
                              'ShaderSource': ('glShaderSource', [GLuint, GLsizei, POINTER(c_char_p), POINTER(GLuint)], None),  #FIXME: conversion between arrays and pointers in ctypes?
                              'CompileShader': ('glCompileShader', [GLuint], None),
                              'DeleteShader' : ('glDeleteShader', [GLuint], None),
                              'GetShader'    : ('glGetShaderiv', [GLuint, GLenum, POINTER(GLint)], None)

                          },
                      'GL_ARB_shader_objects': { #FIXME: find out arb symbols
                              'CreateShader': ('glCreateShaderObjectARB'),
                              'ShaderSource': ('glShaderSourceARB'),
                              'CompileShader': ('glCompileShaderARB', [GLuint], None),
                              'DeleteShader' : ('glDeleteShaderARB', [GLuint], None),
                              'GetShader'    : ('glGetShaderivARB', [GLuint, GLenum, POINTER(GLint)], None)
                                               }                     
                      })

CreateShaderObject = shader.CreateShaderObject
ShaderSource = shader.ShaderSource

#CreateProgram
#LinkProgram

program = Functionality({
                    '': {
                            'CreateProgram': ('glCreateProgram', [], GLuint),
                            'AttachShader':  ('glAttachShader', [GLuint, GLuint], None),
                            'LinkProgram':   ('glLinkProgram', [GLuint], None),
                            'UseProgram':    ('glUseProgram', [GLuint], None),
                            'DeleteProgram': ('glDeleteProgram', [GLuint], None),
                            'GetProgram':    ('glGetProgramiv', [GLuint, GLenum, POINTER(GLint)], None),
                            'GetProgramInfoLog': ('glGetProgramInfoLog', [GLuint, GLuint, POINTER(GLuint), POINTER(GLchar)], None),
                        },
                        })

CreateProgram = program.CreateProgram
GetProgramInfoLog = program.GetProgramInfoLog

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
                     NULL)

class VertexShader(Shader):
    _shader_type = VERTEX_SHADER

class FragmentShader(Shader):
    _shader_type = FRAGMENT_SHADER

class ProgramProperty(object):
    _convert = lambda x: x
    def __get__(self, program, owner):
        value = GLuint(0)
        GetProgramiv(program._object,
                     self._property,
                     POINTER(value))
        return self._convert(value.value)

class BoolProgramProperty(object):
    _convert = bool

program_properties = ['DELETE_STATUS',
                      'LINK_STATUS',
                      'VALIDATE_STATUS',
                      'INFO_LOG_LENGTH',
                      'ATTACHED_SHADERS',
                      'ACTIVE_ATTRIBUTES',
                      'ACTIVE_ATTRIBUTE_MAX_LENGTH',
                      'ACTIVE_UNIFORMS',
                      'ACTIVE_UNIFORM_MAX_LENGTH'
                     ]

class DeleteStatus(BoolProgramProperty):
    _property = DELETE_STATUS

class LinkStatus(BoolProgramProperty):
    _property = LINK_STATUS

class ValidateStatus(BoolProgramProperty):
    _property = VALIDATE_STATUS

class Program(object):
    def __init__(self):
        self._object = CreateProgram()

        for property in program_properties:
            name = _split_enum_name(property)
            caps = _cap_name(name)

            def add_property():
                class Property(ProgramProperty):
                    _property = getattr(constants, property)
                    _convert = bool
                               if property in boolean_properties
                               else lambda x: x

                setattr(self, '_'.join(name), Property())
            add_property()

    @property
    def log(self): pass
        log_length = self.info_long_length
        log = (GLchar * (log_length.value + 1))()
        GetProgramInfoLog(self._object,
                          log_length, NULL,
                          POINTER(log))
        return log.value
