from pygl._gl import lib as _gl

from ctypes import c_uint, POINTER

from pygl.constants import GL_TEXTURE_2D, GL_TEXTURE0, GL_MAX_TEXTURE_UNITS

from pygl.constants import GL_RGBA as RGBA

from pygl.util import _get_integer

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
        _gl.glBindTexture(GL_TEXTURE_2D, self._texture)
    
#TODO: rename class, make Texture2D directly correspond with GL_TEXTURE_2D binding
class Texture2D(Texture):
    def __init__(self):
        self._texture = _gen_texture()
        self._unit = None
    def image(self, width, height, data, level=0, storage=RGBA, format=RGBA, border=0):
        #FIXME: make sure it's currently bound
        _gl.glTexImage2D(GL_TEXTURE_2D, c_int(level),
                         c_uint(storage),
                         c_uint(width), c_uint(height),
                         c_int(border),
                         c_uint(format), GL_BYTES, #FIXME: don't hardcore bytes 
                         bytestream(data)) #FIXME: make pointer out of data



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
