from pygl._gl import lib as _gl

from ctypes import c_uint, POINTER
from ctypes import c_int8, c_int16, c_int32
from ctypes import c_uint8, c_uint16, c_uint32
from ctypes import c_float

from ctypes import c_uint32 as GLenum #FIXME: use globally? use at all?
import ctypes

from pygl.constants import GL_TEXTURE_2D, GL_TEXTURE0, GL_MAX_TEXTURE_UNITS
from pygl.constants import GL_UNSIGNED_BYTE, GL_BYTE
from pygl.constants import GL_UNSIGNED_SHORT, GL_SHORT
from pygl.constants import GL_UNSIGNED_INT, GL_INT
from pygl.constants import GL_FLOAT

from pygl.constants import GL_RGBA as RGBA

from pygl.util import _get_integer

#TODO: make TextureImage class or something to generically handle 2d texture images?
#TODO: including faces of cube maps, etc?

def _gen_texture():
    texture = c_uint()
    _gl.glGenTextures(1, POINTER(texture))
    return texture

class Texture(object):
    def _unit_enum(self):
        return c_uint(GL_TEXTURE0 + self._unit)
    def enable(self):  _gl.glEnable(self._unit_enum())
    def disable(self): _gl.glDisable(self._unit_enum())
    def _bind(self, _unit):
        self._unit = _unit
        _gl.glActiveTexture(self._unit_enum())
        _gl.glBindTexture(self._binding, self._texture)

#FIXME: make sure data mapping is correct
#FIXME: discover all possibilities
_ctypes_data = {
                GL_UNSIGNED_BYTE.value: POINTER(ctypes.c_uint8),
                GL_BYTE.value: POINTER(c_int8),
                GL_UNSIGNED_SHORT.value: POINTER(ctypes.c_uint16),
                GL_SHORT.value: POINTER(ctypes.c_int16),
                GL_UNSIGNED_INT.value: POINTER(ctypes.c_uint32),
                GL_INT.value: POINTER(ctypes.c_int32),
                GL_FLOAT.value: POINTER(c_float)
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
                         c_uint(self.format), GL_BYTES, #FIXME: don't hardcore bytes 
                         bytestream(self.data)) #FIXME: make pointer out of data
    
#TODO: rename class, make Texture2D directly correspond with GL_TEXTURE_2D binding
class Texture2D(Texture):
    def __init__(self):
        self._texture = _gen_texture()
        self._unit = None
        self._binding = GL_TEXTURE_2D
        self._image = None
    @property
    def image(self): return self._image

    @image.setter
    def image(self, image):
        #FIXME: save prior binding, use open texture unit?
        #FIXME: use DSA?
        self.bind(0)
        self._image = image
        self._image.submit(self.binding)
        #FIXME: self.unbind()

    def bind(self, _unit): 
        if self._unit:
            self.unbind() #TODO: any reason why you *couldn't* bind the same texture to multiple _units?
        self._bind(_unit)

    #FIXME: remove?
    def unbind(self):
        _gl.glActiveTexture(self._unit_enum())
        _gl.glBindTexture(GL_TEXTURE_2D, c_uint(0))
        self._unit = None       

class TexturePlaceholder(Texture):
    def __init__(self, unit):
        self._unit = unit
        self._texture = 0
    def bind(self, unit): self._bind(unit)

class Textures(object):
    def __init__(self):
        self._max_texture_units = _get_integer(GL_MAX_TEXTURE_UNITS)
        self._textures = [TexturePlaceholder(i)
                          for i in range(0, self._max_texture_units)
                         ]
    def enable(self):
        #FIXME: enable more types?
        #FIXME: require explicit enable? ie: enable_cubemap() etc?
        _gl.glEnable(GL_TEXTURE_2D)

    def __getitem__(self, index):
        return self._textures[index]

    def __setitem__(self, index, value):
        if value is None:
            self._textures[index] = TexturePlaceholder(i)
            self._textures[index].bind(index)
        else:
            self._textures[index] = value

        value.bind(index)
