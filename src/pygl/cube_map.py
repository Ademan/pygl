from pygl.texture import _gen_texture()
from pygl.texture import Texture

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

class CubeFace(object):
    def __init__(self, binding):
        self._binding = binding
    def __get__(self, instance, owner): pass
    def __set__(self, texture, image):
        with PreserveTextureBinding(texture):
            texture._bind()
            image.submit(self._binding)


class CubeMap(Texture):
    def __init__(self):
        self.texture = _gen_texture()
        self.unit = None
        for face in _cube_attrs:
            setattr(self, face, CubeFace(_attr_enum[face])) #FIXME: face to face enum
