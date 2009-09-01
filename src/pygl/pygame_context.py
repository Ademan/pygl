from ctypes import create_string_buffer

from pygl._gl import lib as _gl

from pygl.context import Context
import pygame

from pygl.constants import UNSIGNED_BYTE
from pygl.constants import RGBA

class PygameContext(Context):
    def __init__(self):
        Context.__init__(self)
    def flip(self):
        pygame.display.flip()

from pygl.texture import TextureImage

def load_image(path):
    surface = pygame.image.load(path)

    width, height = surface.get_size()

    Bpp = surface.get_bytesize()
    bpp = surface.get_bitsize()

    pygame_buffer = surface.get_buffer()

    buffer = create_string_buffer(pygame_buffer.raw, pygame_buffer.length)

    image = TextureImage()

    image.width = width
    image.height = height

    image.level = 0
    image.storage = RGBA        #FIXME: don't assume either
    image.type = UNSIGNED_BYTE  #FIXME: don't assume 32 bit RGBA
    image.format = RGBA         #FIXME: don't assume 32 bit RGBA
    image.border = 0

    image.data = buffer

    return image
