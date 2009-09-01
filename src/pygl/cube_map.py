from pygl.texture import _gen_texture()
from pygl.texture import Texture
from pygl.texture import Filter, WrapMode

from pygl.util import _debug_enum

from pygl.constants import TEXTURE_CUBE_MAP_POSITIVE_X

from pygl import texture

#TODO: direct state access path?

_sign = ["positive", "negative"]
_axis = ["x", "y", "z"]
_cube_attrs = ["%s_%c" % (sign, axis)
               for (sign, axis) in product(_sign, _axis)]

_attr_enum  = zip(_cube_attrs,
                  [TEXTURE_CUBE_MAP_POSITIVE_X + i
                   for i in xrange(0, 6)])

#TODO: functions go here

class CubeFace(object):
    def __init__(self, face):
        self._face = face
    def __get__(self, instance, owner): pass
    def __set__(self, texture, image):
        with PreserveTextureBinding(texture) as binding: #FIXME: why do i need to give PreserveTextureBinding a texture?
            binding.state = texture
            image.submit(self._face)

def _add_faces(cls):
    for name, face in _cube_enum:
        _debug_enum(name, face)
        setattr(cls, name, CubeFace(face))
    return cls

@_add_faces
class CubeMap(Texture):
    _binding = TEXTURE_
    def __init__(self):
        self._texture = _gen_texture()
        self._unit = None
        self.filter = Filter(self)
        self.wrap = WrapMode(self)
    def bind(self, unit):
        self.unit = unit
        self._bind()
