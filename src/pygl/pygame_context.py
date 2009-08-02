from pygl._gl import lib as _gl

from pygl.context import Context
import pygame

class PygameContext(Context):
    def __init__(self):
        Context.__init__(self)
    def flip(self):
        pygame.display.flip()

from pygl.texture import TextureImage

#FIXME: don't name sdl_image ?
def sdl_image(path):
    #TODO: image loading code
    surface = pygame.image.load(path)

    width, height = surface.get_size()

    Bpp = surface.get_bytesize()
    bpp = surface.get_bitsize()

    buffer = surface.get_buffer()

    image = TextureImage(width, height, buffer) #FIXME: buffer needs to be transformed!
    return texture_image
