import ctypes
from ctypes import c_uint, POINTER
from ctypes import c_int8, c_int16, c_int32
from ctypes import c_uint8, c_uint16, c_uint32
from ctypes import c_float
from ctypes import c_void_p
from ctypes import cast
from ctypes import byref

from pygl._gl import lib as _gl
from pygl.gltypes import GLenum, GLuint

from pygl.constants import TEXTURE_MIN_FILTER, TEXTURE_MAG_FILTER
from pygl.constants import TEXTURE_WRAP_S, TEXTURE_WRAP_T
from pygl.constants import TEXTURE_1D, TEXTURE_2D, TEXTURE_3D
from pygl.constants import TEXTURE_2D, TEXTURE0, MAX_TEXTURE_UNITS
from pygl.constants import MAX_COMBINED_TEXTURE_IMAGE_UNITS
from pygl.constants import MAX_TEXTURE_COORDS
from pygl.constants import UNSIGNED_BYTE, BYTE
from pygl.constants import UNSIGNED_SHORT, SHORT
from pygl.constants import UNSIGNED_INT, INT
from pygl.constants import FLOAT

from pygl.constants import RGBA

from pygl.util import _get_integer
from pygl.util import _debug_enum

from pygl.glerror import _check_errors

from pygl.gltypes import GLsizei
from pygl.gltypes import GLushort, GLshort
from pygl.gltypes import GLuint, GLint
from pygl.gltypes import GLubyte, GLbyte
from pygl.gltypes import GLchar
from pygl.gltypes import GLfloat

from pygl.state import PreserveTextureBinding

from pygl._gl import Enable, Disable

from pygl.state import BindTexture

#TODO: make TextureImage class or something to generically handle 2d texture images?
#TODO: including faces of cube maps, etc?

GenTextures = _gl.glGenTextures
GenTextures.argtypes = [GLsizei, POINTER(GLuint)]

def _gen_texture():
    texture = GLuint(0)
    GenTextures(1, texture)
    return texture

TexParameter = _gl.glTexParameteri
TexParameter.argtypes = [GLenum, GLenum, GLint]

GetTexParameter = _gl.glGetTexParameteriv
GetTexParameter.argtypes = [GLenum, GLenum, POINTER(GLint)]

class TextureParameter(object):
    def __init__(self, parameter):
        self._parameter = parameter

    def _get_texture(self, instance):
        return instance

    def __get__(self, instance, owner):
        texture = self._get_texture(instance)
        result = GLint(0)
        with PreserveTextureBinding(texture):
            _gl.glGetTexParameteriv(texture._binding, self._parameter, result)
        return result.value

    def __set__(self, instance, value):
        texture = self._get_texture(instance)
        with PreserveTextureBinding(texture) as binding:
            binding.state = texture._texture #FIXME: binding.state ? clean enough?
            TexParameter(texture._binding, self._parameter, value.value) #FIXME: what if it's not a GLenum?
            _check_errors()

class NestedTextureParameter(TextureParameter):
    def _get_texture(self, instance):
        return instance._texture

class Filter(object):
    min = NestedTextureParameter(TEXTURE_MIN_FILTER)
    mag = NestedTextureParameter(TEXTURE_MAG_FILTER)
    def __init__(self, texture):
        self._texture = texture

class WrapMode(object):
    s = NestedTextureParameter(TEXTURE_WRAP_S)
    t = NestedTextureParameter(TEXTURE_WRAP_T)
    def __init__(self, texture):
        self._texture = texture

ActiveTexture = _gl.glActiveTexture
ActiveTexture.argtypes = [GLenum]

class Texture(object):
    @property
    def unit(self):
        return GLenum(TEXTURE0.value + self._unit)

    #FIXME: probably bad
    @unit.setter
    def unit(self, unit):
        self._unit = unit
        self._set_unit()

    def enable(self):
        self._set_unit()
        _check_errors()
        Enable(self._binding)
        _check_errors()       #FIXME: check after everything?

    def disable(self):
        self._set_unit()
        _check_errors()
        Disable(self._binding)
        _check_errors()

    def _set_unit(self):
        ActiveTexture(self.unit)
        _check_errors()

    def _bind(self):
        BindTexture(self._binding, self._texture)

#TODO: make sure data mapping is correct
_data_types = {
                GLubyte:   UNSIGNED_BYTE,
                GLbyte:    BYTE,
                GLchar:    BYTE,
                GLushort:  UNSIGNED_SHORT,
                GLshort:   SHORT,
                GLuint:    UNSIGNED_INT,
                GLint:     INT,
                GLfloat:   FLOAT
               }
                
TexImage2D = _gl.glTexImage2D
TexImage2D.argtypes = [GLenum, GLint, GLint, GLsizei, GLsizei, GLint, GLenum, GLenum, c_void_p]

GetTexImage = _gl.glGetTexImage
GetTexImage.argtypes = [GLenum, GLint, GLenum, GLenum, c_void_p]

class TextureImage(object):
    def _infer_type(self):
        return self._type if hasattr(self, "_type") else _data_types[type(self.data)._type_] #TODO: really ok to access _type_ to get element types?
    def submit(self, binding):
        TexImage2D(binding, self.level,
                   self.storage.value, #FIXME: HACK! why does the spec want an int anyways?
                   self.width, self.height,
                   self.border,
                   self.format, self.type,
                   cast(self.data, c_void_p)
                   #c_void_p(self.data)
                   #byref(self.data)
                   #self.data.raw
                   ) #FIXME: make pointer out of data
    
#TODO: rename class, make Texture2D directly correspond with TEXTURE_2D binding
class Texture2D(Texture):
    _binding = TEXTURE_2D
    def __init__(self):
        self._texture = _gen_texture()
        _check_errors()
        self._unit = None
        self._image = None
        self.filter = Filter(self)
        self.wrap = WrapMode(self)

    @property
    def image(self): return self._image

    @image.setter
    def image(self, image):
        with PreserveTextureBinding(self):
            self._bind()
            _check_errors()
            self._image = image
            self._image.submit(self._binding)
            _check_errors()

    def bind(self, unit): 
        self.unit = unit
        self._bind()

class TexturePlaceholder(Texture):
    _texture = 0
    def __init__(self, unit, binding=None):
        self._unit = unit
        if binding:
            self._binding = binding
    def bind(self):
        self._set_unit()
        self._bind()
        del self._binding #should get rid of _binding attr so that future placeholders won't do useless work

class Textures(object):
    def __init__(self):
        self._max_texture_units = max([_get_integer(MAX_TEXTURE_COORDS), _get_integer(MAX_COMBINED_TEXTURE_IMAGE_UNITS)])
        self._textures = [TexturePlaceholder(i)
                          for i in xrange(0, self._max_texture_units)
                         ]

    def __len__(self): return self._max_texture_units

    def __getitem__(self, index):
        return self._textures[index]

    def __setitem__(self, index, value):
        if value is None:
            del self[index]
            return
        else:
            self._textures[index] = value

        self._textures[index].bind(index)

    def __delitem__(self, index):
        try:
            binding = self._textures[index]._binding
            self._textures[index] = TexturePlaceholder(index, binding)
        except AttributeError:
            self._textures[index] = TexturePlaceholder(index, None)

        self._textures[index].bind(index)
