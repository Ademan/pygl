from pygl._gl import lib as _gl
from pygl._gl import GetString

from pygl.constants import MODELVIEW, COLOR_BUFFER_BIT, DEPTH_BUFFER_BIT
from pygl.constants import VERSION

from pygl.immediate import TrianglesMode, QuadsMode, PointsMode
from pygl.buffer import ColorBuffer, DepthBuffer

from pygl.matrix_stack import ModelviewMatrixStack, ProjectionMatrixStack

from pygl.texture import Textures
from pygl.util import _get_integer

from pygl.gltypes import GLenum

from pygl._gl import Enable, Disable

class Context(object):
    def __init__(self):
        self._modelview = ModelviewMatrixStack()
        self._projection = ProjectionMatrixStack()
        self._color = ColorBuffer()
        self._depth = DepthBuffer()
        self._textures = Textures()

    def enable(self, enum):
        Enable(enum)

    def disable(self, enum):
        Disable(enum)

    def triangles(self):
        return TrianglesMode()

    def quads(self):
        return QuadsMode()
    
    @property
    def textures(self): return self._textures

    @property
    def version(self):
        return GetString(VERSION).value

    @property
    def modelview(self):
        return self._modelview

    @modelview.setter
    def modelview(self, value):
        if value != self._modelview:
            self.modelview.load(value)

    @property
    def projection(self):
        return self._projection

    @projection.setter
    def projection(self, value):
        if value != self._modelview:
            self.modelview.load(value)

    @property
    def color(self): return self._color

    @property
    def depth(self): return self._depth

#FIXME: put me somewhere else!
def clear_buffers(buffers):
    flags = 0x0000
    for buffer in buffers:
        flags |= buffer.attachment
    _gl.glClear(flags)
