from pygl._gl import lib as _gl

from constants import COLOR_BUFFER_BIT, DEPTH_BUFFER_BIT

class Buffer(object):
    def clear(self):
        _gl.glClear(self.attachment)

#default buffers
class ColorBuffer(Buffer):
    def __init__(self):
        self.attachment = COLOR_BUFFER_BIT

class DepthBuffer(Buffer):
    def __init__(self):
        self.attachment = DEPTH_BUFFER_BIT
