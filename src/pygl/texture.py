from pygl._gl import lib as _gl

import ctypes
from ctypes import c_uint, POINTER
from ctypes import c_int8, c_int16, c_int32
from ctypes import c_uint8, c_uint16, c_uint32
from ctypes import c_float

from pygl.gltypes import GLenum, GLuint

from pygl.constants import TEXTURE_MIN_FILTER, TEXTURE_MAG_FILTER
from pygl.constants import TEXTURE_WRAP_S, TEXTURE_WRAP_T
from pygl.constants import TEXTURE_1D, TEXTURE_2D, TEXTURE_3D
from pygl.constants import TEXTURE_2D, TEXTURE0, MAX_TEXTURE_UNITS
from pygl.constants import UNSIGNED_BYTE, BYTE
from pygl.constants import UNSIGNED_SHORT, SHORT
from pygl.constants import UNSIGNED_INT, INT
from pygl.constants import FLOAT

from pygl.constants import RGBA as RGBA

from pygl.util import _get_integer

#TODO: make TextureImage class or something to generically handle 2d texture images?
#TODO: including faces of cube maps, etc?

def _gen_texture():
    texture = GLuint() #TODO: GLuint ?
    _gl.glGenTextures(1, POINTER(texture))
    return texture

class TextureParameter(object):
    def __init__(self, parameter):
        self._parameter = parameter

    def _get_texture(self, instance):
        return instance

    def __get__(self, instance, owner):
        texture = self._get_texture(instance)
        result = GLuint(0)
        with PreserveTextureBinding(texture):
            _gl.glGetTexParameteriv(texture._binding, self._parameter, POINTER(result))
        return result.value

    def __set__(self, instance, value):
        texture = self._get_texture(instance)
        with PreserveTextureBinding(texture._binding) as binding:
            binding.state = texture.texture #FIXME: binding.state ? clean enough?
            _gl.glTexParameteri(self._parameter, GLuint(value))

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

class Texture(object):
    def __init__(self):
        self.filter = Filter(self)
        self.wrap = WrapMode(self)
    def _unit_enum(self):
        return c_uint(TEXTURE0 + self._unit)

    def enable(self):  _gl.glEnable(self._unit_enum())
    def disable(self): _gl.glDisable(self._unit_enum())

    def _set_unit(self, unit):
        self._unit = _unit
        _gl.glActiveTexture(self._unit_enum())

    def _bind(self):
        _gl.glBindTexture(self._binding, self._texture)

#TODO: make sure data mapping is correct
_ctypes_data = {
                UNSIGNED_BYTE.value:    POINTER(ctypes.c_uint8),
                BYTE.value:             POINTER(c_int8),
                UNSIGNED_SHORT.value:   POINTER(ctypes.c_uint16),
                SHORT.value:            POINTER(ctypes.c_int16),
                UNSIGNED_INT.value:     POINTER(ctypes.c_uint32),
                INT.value:              POINTER(ctypes.c_int32),
                FLOAT.value:            POINTER(c_float)
               }
                
class TextureImage(object):
    def __init__(self, width, height, data, level=0, storage=RGBA, format=RGBA, border=0):
        self.width = width
        self.height = height
        self.data = data
        self.level = level
        self.storage = storage
        self.format = format
        self.border = border
    def submit(self, binding):
        _gl.glTexImage2D(binding, c_int(self.level),
                         c_uint(self.storage),
                         c_uint(self.width), c_uint(self.height),
                         c_int(self.border),
                         c_uint(self.format), _data_type[type(self.data)._type_], #TODO: really ok to access _type_ to get element types?
                         POINTER(self.data)) #FIXME: make pointer out of data
    
#TODO: rename class, make Texture2D directly correspond with TEXTURE_2D binding
class Texture2D(Texture):
    def __init__(self):
        self._texture = _gen_texture()
        self._unit = None
        self._binding = TEXTURE_2D
        self._image = None

    @property
    def image(self): return self._image

    @image.setter
    def image(self, image):
        with PreserveTextureBinding(self):
            self._bind()
            self._image = image
            self._image.submit(self._binding)

    def bind(self, _unit): 
        if self._unit:
            self.unbind() #TODO: any reason why you *couldn't* bind the same texture to multiple _units?
                          #TODO: reasons why you *shouldn't* are probably abundant though
        self._set_unit(_unit)
        self._bind()

    #FIXME: remove?
    def unbind(self):
        _gl.glActiveTexture(self._unit_enum())
        _gl.glBindTexture(self._binding, GLuint(0))
        self._unit = None       

class TexturePlaceholder(Texture):
    def __init__(self, unit, binding):
        self._unit = unit
        self._texture = 0
        self._binding = binding
    def bind(self):
        self._set_unit(self.unit)
        self._bind()
        del self._binding #should get rid of _binding attr so that future placeholders won't do useless work

class Textures(object):
    def __init__(self):
        self._max_texture_units = _get_integer(MAX_TEXTURE_UNITS)
        self._textures = [TexturePlaceholder(i)
                          for i in range(0, self._max_texture_units)
                         ]
    def enable(self):
        #FIXME: enable more types?
        #FIXME: require explicit enable? ie: enable_cubemap() etc?
        #TODO: does this affect programmable pipeline?
        _gl.glEnable(TEXTURE_2D)

    def __getitem__(self, index):
        return self._textures[index]

    def __setitem__(self, index, value):
        if value is None:
            try:
                binding = self._textures[index]._binding
                self._textures[index] = TexturePlaceholder(index, binding)
            except AttributeError:
                self._textures[index] = TexturePlaceholder(index, None)
        else:
            self._textures[index] = value

        self._textures[index].bind(index)
