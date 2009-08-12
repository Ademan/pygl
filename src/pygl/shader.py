#FIXME: stop using POINTER(GLchar) except for buffer construction?
#FIXME: possible if c_str(POINTER((GLchar * size)())) is valid
from ctypes import c_char_p as c_str
from ctypes import POINTER
from ctypes import addressof
from ctypes import create_string_buffer
from ctypes import cast

from pygl.gltypes import GLenum
from pygl.gltypes import GLint, GLuint
from pygl.gltypes import GLchar
from pygl.gltypes import GLsizei
from pygl.gltypes import NULL
import pygl

from pygl.constants import VERTEX_SHADER, FRAGMENT_SHADER

from pygl._gl import Functionality

from pygl.util import _split_enum_name, _cap_name

from pygl.glerror import _check_errors

shader = Functionality({
                      '': {
                              'CreateShader': ('glCreateShader', [GLenum], GLuint),
                              'ShaderSource': ('glShaderSource', [GLuint, GLsizei, POINTER(c_str), POINTER(GLuint)], None),  #FIXME: conversion between arrays and pointers in ctypes?
                              'CompileShader': ('glCompileShader', [GLuint], None),
                              'DeleteShader' : ('glDeleteShader', [GLuint], None),
                              'GetShaderiv'    : ('glGetShaderiv', [GLuint, GLenum, POINTER(GLint)], None),
                              'GetShaderInfoLog': ('glGetShaderInfoLog', [GLuint, GLuint, POINTER(GLuint), c_str], None),

                          },
#                      'GL_ARB_shader_objects': { #FIXME: find out arb symbols
#                              'CreateShader': ('glCreateShaderObjectARB'),
#                              'ShaderSource': ('glShaderSourceARB'),
#                              'CompileShader': ('glCompileShaderARB', [GLuint], None),
#                              'DeleteShader' : ('glDeleteShaderARB', [GLuint], None),
#                              'GetShader'    : ('glGetShaderivARB', [GLuint, GLenum, POINTER(GLint)], None)
#                                               }                     
                      })

CreateShader = shader.CreateShader
ShaderSource = shader.ShaderSource
CompileShader = shader.CompileShader
GetShaderiv = shader.GetShaderiv
GetShaderInfoLog = shader.GetShaderInfoLog

program = Functionality({
                    '': {
                            'CreateProgram': ('glCreateProgram', [], GLuint),
                            'AttachShader':  ('glAttachShader', [GLuint, GLuint], None),
                            'LinkProgram':   ('glLinkProgram', [GLuint], None),
                            'UseProgram':    ('glUseProgram', [GLuint], None),
                            'DeleteProgram': ('glDeleteProgram', [GLuint], None),
                            'GetProgramiv':    ('glGetProgramiv', [GLuint, GLenum, POINTER(GLint)], None),
                            'GetProgramInfoLog': ('glGetProgramInfoLog', [GLuint, GLuint, POINTER(GLuint), c_str], None),
                            'GetActiveAttrib': ('glGetActiveAttrib', [GLuint, GLuint, GLuint, POINTER(GLuint), POINTER(GLint), POINTER(GLenum), POINTER(GLchar)], None),
                            'GetActiveUniform': ('glGetActiveUniform', [GLuint, GLuint, GLuint, POINTER(GLuint), POINTER(GLint), POINTER(GLenum), POINTER(GLchar)], None),
                            #TODO: verify
                            'GetUniformLocation': ('glGetUniformLocation', [GLuint, c_str], GLuint),
                            'GetAttribLocation': ('glGetAttribLocation', [GLuint, c_str], GLuint),
                        },
                        })

CreateProgram = program.CreateProgram
AttachShader = program.AttachShader
LinkProgram = program.LinkProgram
UseProgram = program.UseProgram
DeleteProgram = program.DeleteProgram

GetProgramiv = program.GetProgramiv
GetProgramInfoLog = program.GetProgramInfoLog
GetActiveAttrib = program.GetActiveAttrib
GetAttribLocation = program.GetAttribLocation

GetActiveUniform = program.GetActiveUniform
GetUniformLocation = program.GetUniformLocation

def _get_info_log(getter):
    def _wrapped_get_info_log(self):
        log_length = self.info_log_length
        log = create_string_buffer('', log_length)
        getter(self._object,
               GLuint(log_length),
               cast(NULL, POINTER(GLuint)),
               c_str(addressof(log))
              )
        return log.value
    return _wrapped_get_info_log

def _info_log_property(getter):
    return property(_get_info_log(getter))

class ObjectProperty(object):
    _convert = lambda x: x
    def __get__(self, program, owner):
        value = GLint(0)
        self._get(program._object,
                     self._property,
                     value
                 )
        return self._convert(value.value)
    def __set__(self, program, value): pass

def _add_properties(object, getter, properties):
    for type, properties in properties.iteritems():
        for property in properties:
            name = _split_enum_name(property)
            caps = _cap_name(name)

            from pygl import constants #FIXME: move to top like normal?

            class Property(ObjectProperty):
                _get = getter
                _property = getattr(constants, property)
                _convert = type

            setattr(object, '_'.join(map(str.lower, name)), Property())

_shader_properties = {
                      GLenum: ['SHADER_TYPE'],
                      bool: ['DELETE_STATUS', 'COMPILE_STATUS'],
                      int: ['INFO_LOG_LENGTH', 'SHADER_SOURCE_LENGTH']
                      }

def _object_properties(getter, properties):
    def _wrapped_add_properties(cls):
        _add_properties(cls, getter, properties)
        return cls
    return _wrapped_add_properties

@_object_properties(GetShaderiv, _shader_properties)
class Shader(object):
    log = _info_log_property(GetShaderInfoLog)
    def __init__(self):
        self._object = CreateShader(self._shader_type)
        #_add_properties(self, GetShaderiv, _shader_properties)

    def _stringify(self, source):
        stringified = str(source)
        if source == stringified:
            #FIXME: is this really an ok test for string-likeness?
            return source
        else:
            return ''.join([line for line in source])

    def compile(self):
        CompileShader(self._object)
        _check_errors()
        return self.compile_status

    @property
    def sources(self): pass
        #TODO: GetSources()

    @sources.setter
    def sources(self, sources):
        #FIXME: looking at that for a second time, that is UGLY
        c_str_array = (c_str * len(sources))(*[
                                                c_str(''.join(source)) if hasattr(source, 'read')
                                                    else c_str(source)
                                                        for source in sources
                                              ])
        ShaderSource(self._object,
                     len(sources),
                     c_str_array,
                     cast(NULL, POINTER(GLuint))
                    )
        _check_errors()

class VertexShader(Shader):
    _shader_type = VERTEX_SHADER

class FragmentShader(Shader):
    _shader_type = FRAGMENT_SHADER

class AttachedShaders(object):
    def __init__(self, program):
        self._program = program
        self._shaders = []

    def append(self, shader):
        self._shaders.append(shader)

        AttachShader(self._program._object, shader._object)
        _check_errors()

    def extend(self, shaders):
        self._shaders.extend(shaders)
        for shader in shaders:
            AttachShader(self._program._object, shader._object)

    def remove(self, shader):
        DetachShader(self._program._object,
                     shader._object)
        _check_errors()

class ProgramVariable(object):
    def __init__(self, type, size):
        self.type = type
        self.size = size

class Attribute(ProgramVariable):
    def __call__(self, *args): pass
        #Attribute3f(args) #TODO

#FIXME: what represents the "preferred" vector? 1x3 or 3x1?
#FIXME: or does opengl switch between column and row vectors
#FIXME: as needed?
_numeric_variable_types = {float: [(1,1), (1, 2), (1,3), (1,4),
                           (2,2), (3, 3), (4,4)],
                   int:   [(1,1), (1, 2), (1,3), (1,4)],
                   bool:  [(1,1), (1, 2), (1,3), (1,4)]}

_names = {float: "FLOAT",
          int:   "INT",
          bool:  "BOOL"}

_variable_types = {}
for type, sizes in _numeric_variable_types.iteritems():
    for size in sizes:
        if size[1] == 1:
            constant_name = _names[type]
        else:
            constant_name = "%(name)s_%(type)s%(size)d" % {
                                                      'name': _names[type],
                                                      'type': 'VEC' if size[0] == 1 else 'MAT',
                                                      'size': size[1]
                                                     }
        constant = getattr(pygl.constants, constant_name).value
        _variable_types[constant] = ProgramVariable(type, size)

class ProgramVariables(object):
    #FIXME: other types exist (nonsquare matrices)
    _variable_types = ['FLOAT', 'FLOAT_VEC2', 'FLOAT_VEC3', 'FLOAT_VEC4',
                       'INT', 'INT_VEC2', 'INT_VEC3', 'INT_VEC4',
                       'BOOL', 'BOOL_VEC2', 'BOOL_VEC3', 'BOOL_VEC4',
                       'FLOAT_MAT2', 'FLOAT_MAT3', 'FLOAT_MAT4',
                       'SAMPLER_1D', 'SAMPLER_2D', 'SAMPLER_3D',
                       'SAMPLER_CUBE',
                       'SAMPLER_1D_SHADOW', 'SAMPLER_2D_SHADOW']
    def __init__(self, program):
        self._program = program
        self._get_all()
    def _get_info(self, index):
        namelen = GLsizei(0)
        attrib_size = GLint(0)
        type = GLenum(0)

        name = create_string_buffer('', self._max_name_length())
        
        self._get_variable(self._program._object,
                        GLuint(index),
                        GLsizei(self._max_name_length()),
                        namelen,
                        attrib_size,
                        type,
                        name
                       )

        return name.value, type, attrib_size.value

    def _dump(self):
        for name, info in self._variables.iteritems():
            print "%s:" % name
            print "\ttype: %d" % info[0].value
            print "\tsize: %d" % info[1]
            print "\tlocation: %d" % info[2]

    def _get_all(self):
        self._variables = {}
        for index in xrange(0, self._get_variable_count()):
            name, type, size = self._get_info(index)
            self._variables[name] = (type, size,
                                     self._get_location(self._program._object, c_str(name))) #TODO: c_str necessary?

    def __getitem__(self, name): pass #TODO: getuniform/getattrib

    def _set_variable(self, location, value): pass
        #TODO: how to handle this?!?
        #TODO: check for _n _m and _data?
        #TODO: seems a bit magical, but would make everything easier to use

    def __setitem__(self, name, value):
        location = self._variables[name][2]
        self._set_variable(location, value)

class ProgramAttributes(ProgramVariables):
    _get_variable = GetActiveAttrib
    _get_location = GetAttribLocation
    def _get_variable_count(self):
        return self._program.active_attributes
    def _max_name_length(self):
        return self._program.active_attribute_max_length

class ProgramUniforms(ProgramVariables):
    _get_variable = GetActiveUniform
    _get_location = GetUniformLocation
    def _get_variable_count(self):
        return self._program.active_uniforms
    def _max_name_length(self):
        return self._program.active_uniform_max_length

_program_properties = {
                      bool: ['DELETE_STATUS', 'LINK_STATUS', 'VALIDATE_STATUS'],
                      int: ['INFO_LOG_LENGTH', 'ATTACHED_SHADERS', 'ACTIVE_ATTRIBUTES', 'ACTIVE_ATTRIBUTE_MAX_LENGTH', 'ACTIVE_UNIFORMS', 'ACTIVE_UNIFORM_MAX_LENGTH']
                      }

@_object_properties(GetProgramiv, _program_properties)
class Program(object):
    log = _info_log_property(GetProgramInfoLog)
    def __init__(self):
        self._object = CreateProgram()
        self._shaders = AttachedShaders(self)
        _add_properties(self, GetProgramiv, _program_properties)

    def link(self):
        LinkProgram(self._object)
        _check_errors()

        self._attribs = ProgramAttributes(self)
        self._uniforms = ProgramUniforms(self)
        return self.link_status

    def use(self):
        UseProgram(self._object)
        _check_errors()

    @property
    def attribs(self): return self._attribs

    @property
    def uniforms(self): return self._uniforms

    @property
    def shaders(self):
        return self._shaders
