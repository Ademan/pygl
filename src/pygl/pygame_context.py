from pygl._gl import lib as _gl

from pygl.context import Context

import pygame

class PygameContext(Context):
    def __init__(self):
        Context.__init__(self)
    def flip(self):
        pygame.display.flip()
