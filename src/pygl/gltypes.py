from ctypes import c_uint32 as GLenum

from ctypes import c_int8 as GLbyte
from ctypes import c_uint8 as GLubyte

from ctypes import c_int16 as GLshort
from ctypes import c_uint16 as GLushort

from ctypes import c_int32 as GLint
from ctypes import c_uint32 as GLuint

from ctypes import c_float as GLfloat
from ctypes import c_double as GLdouble

from ctypes import c_char as GLchar

from ctypes import c_uint32 as GLsizei #FIXME: correct size?

_gl_type_symbols = {
    GLbyte: 'b',
    GLshort: 's',
    GLint: 'i',

    GLubyte: 'ub',
    GLushort: 'us',
    GLuint: 'ui',

    GLdouble: 'd',
    GLfloat: 'f',
    }

_python_numeric_types = {
                            float: GLdouble,
                            int: GLint
                        }

from ctypes import c_int, c_int8, c_int16, c_int32
from ctypes import c_uint, c_uint8, c_uint16, c_uint32
from ctypes import c_float, c_double

_c_numeric_types = {
                    c_int: int,
                    c_int8: int,
                    c_int16: int,
                    c_int32: int,
                    c_uint: int,
                    c_uint8: int,
                    c_uint16: int,
                    c_uint32: int,
                    c_float: float,
                    c_double: float
                   }

#TODO: implement, decide whether it works on python types or ctypes and so on
#TODO: working on python types would probably be easiest and best
_accuracy = [[GLubyte, GLbyte], [GLushort, GLshort], [GLuint, GLint], [GLfloat], [GLdouble]]
def coerce(args): pass

from ctypes import c_void_p

NULL = c_void_p(0)
