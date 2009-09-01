from ctypes import c_char_p as c_str
from ctypes import POINTER

from pygl.gltypes import GLenum
from pygl.gltypes import GLint, GLuint
from pygl.gltypes import GLboolean
from pygl.gltypes import GLchar
from pygl.gltypes import GLsizei
from pygl.gltypes import GLfloat, GLdouble
from pygl.gltypes import NULL
import pygl

from pygl._gl import function

CreateShader = function('CreateShader', [GLenum], GLuint)
ShaderSource = function('ShaderSource', [GLuint, GLsizei, POINTER(c_str), POINTER(GLuint)], None)
CompileShader = function('CompileShader', [GLuint])
DeleteShader = function('DeleteShader', [GLuint])
GetShaderiv = function('GetShaderiv', [GLuint, GLenum, POINTER(GLint)])
GetShaderInfoLog = function('GetShaderInfoLog', [GLuint, GLuint, POINTER(GLuint), c_str])

CreateProgram = function('CreateProgram', [], GLuint)
AttachShader = function('AttachShader', [GLuint, GLuint])
LinkProgram = function('LinkProgram', [GLuint])
ValidateProgram = function('ValidateProgram', [GLuint])
UseProgram = function('UseProgram', [GLuint])
DeleteProgram = function('DeleteProgram', [GLuint])
GetProgramiv = function('GetProgramiv', [GLuint, GLenum, POINTER(GLint)])
GetProgramInfoLog = function('GetProgramInfoLog', [GLuint, GLuint, POINTER(GLuint), c_str])
GetActiveAttrib = function('GetActiveAttrib',
        [GLuint, GLuint, GLuint, POINTER(GLuint), POINTER(GLint), POINTER(GLenum), POINTER(GLchar)])
GetActiveUniform = function('GetActiveUniform',
        [GLuint, GLuint, GLuint, POINTER(GLuint), POINTER(GLint), POINTER(GLenum), POINTER(GLchar)])
GetUniformLocation = function('GetUniformLocation', [GLuint, c_str], GLuint)
GetAttribLocation = function('GetAttribLocation', [GLuint, c_str], GLuint)

Uniform1i = function('Uniform1i', [GLuint, GLint])
Uniform2i = function('Uniform2i', [GLuint, GLint, GLint])
Uniform3i = function('Uniform3i', [GLuint, GLint, GLint, GLint])
Uniform4i = function('Uniform4i', [GLuint, GLint, GLint, GLint, GLint])

Uniform1f = function('Uniform1f', [GLuint, GLfloat])
Uniform2f = function('Uniform2f', [GLuint, GLfloat, GLfloat])
Uniform3f = function('Uniform3f', [GLuint, GLfloat, GLfloat, GLfloat])
Uniform4f = function('Uniform4f', [GLuint, GLfloat, GLfloat, GLfloat, GLfloat])

UniformMatrix2fv = function('UniformMatrix2fv', [GLuint, GLsizei, GLboolean, POINTER(GLfloat)])
UniformMatrix3fv = function('UniformMatrix3fv', [GLuint, GLsizei, GLboolean, POINTER(GLfloat)])
UniformMatrix4fv = function('UniformMatrix4fv', [GLuint, GLsizei, GLboolean, POINTER(GLfloat)])

#TODO: nonsquare matrices

VertexAttrib1f = function('VertexAttrib1f', [GLuint, GLfloat])
VertexAttrib2f = function('VertexAttrib2f', [GLuint, GLfloat, GLfloat])
VertexAttrib3f = function('VertexAttrib3f', [GLuint, GLfloat, GLfloat, GLfloat])
VertexAttrib4f = function('VertexAttrib4f', [GLuint, GLfloat, GLfloat, GLfloat, GLfloat])

VertexAttrib1d = function('VertexAttrib1d', [GLuint, GLdouble])
VertexAttrib2d = function('VertexAttrib2d', [GLuint, GLdouble, GLdouble])
VertexAttrib3d = function('VertexAttrib3d', [GLuint, GLdouble, GLdouble, GLdouble])
VertexAttrib4d = function('VertexAttrib4d', [GLuint, GLdouble, GLdouble, GLdouble, GLdouble])
