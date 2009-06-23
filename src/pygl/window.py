from pygl import context

class Window(object): pass

#FIXME: initialize pygame in a better way
class PygameWindow(Window):
    def __init__(self, width, height, bpp=24, depth=16, stencil=0):
        import pygame
        from pygame.locals import *

        pygame.init()
        self.screen = pygame.display.set_mode((width, height), HWSURFACE|OPENGL|DOUBLEBUF)

    @property
    def context(self):
        from pygame_context import PygameContext
        return PygameContext()

class GLXWindow(Window):
    def __init__(self):
        raise NotImplementedError("GLXWindow not yet implemented...")
