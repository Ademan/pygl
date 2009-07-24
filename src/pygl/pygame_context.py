from pygl._gl import lib as _gl

from pygl.context import Context
import pygame

class PygameContext(Context):
    def __init__(self):
        Context.__init__(self)
    def flip(self):
        pygame.display.flip()

from pygl.texture import Texture

#FIXME: don't name sdl_image ?
def sdl_image(path):
    #TODO: image loading code
    return texture_image
