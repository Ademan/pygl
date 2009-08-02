from ctypes import c_uint32 as GLenum
from ctypes import c_uint32 as GLtexture

from ctypes import c_int8 as GLbyte
from ctypes import c_uint8 as GLubyte

from ctypes import c_int16 as GLshort
from ctypes import c_uint16 as GLushort

from ctypes import c_int32 as GLint
from ctypes import c_uint32 as GLuint

from ctypes import c_float as GLfloat
from ctypes import c_double as GLdouble

_gl_type_symbols = {
    GLint8: 'b',
    GLint16: 's',
    GLint32: 'i',
    GLint: 'i',

    GLuint8: 'ub',
    GLuint16: 'us',
    GLuint: 'ui',
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
_accuracy = [[GLuint8, GLint8], [GLuint16, GLint16], [GLuint32, GLint32], [GLfloat], [GLdouble]]
def coerce(args): pass
