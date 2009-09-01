#! /usr/bin/env python

from pygame.locals import *
import pygame

from pygl.glu import Perspective
from pygl.util import Translate, Rotate, Scale
from pygl.pygame_context import load_image

from pygl.texture import Texture2D

from pygl.constants import DEPTH_TEST
from pygl.constants import LINEAR
from pygl.constants import NEAREST

from pygl.shader import fixed_function
from pygl.glerror import _check_errors #FIXME: remove when debug no longer needed
import pygl

from test_util import Timer, Cycle
from test_util import create_program, draw_textured_quad, draw_cube
from test_util import checkerboard_teximage

window = pygl.window.PygameWindow(640, 480)

gl = window.context

per_pixel = create_program(open('pixel.vert'), open('pixel.frag'))
per_vertex = create_program(open('vertex.vert'), open('vertex.frag'))

def use_per_pixel():
    per_pixel.use()
    per_pixel.uniforms['checkerboard'] = gl.textures[0]

programs = Cycle([lambda: fixed_function.use(), use_per_pixel, lambda: per_vertex.use()])
programs.next()()

draw_funcs = Cycle([draw_textured_quad, draw_cube])
draw_function = draw_funcs.next()

gl.enable(DEPTH_TEST)

with gl.projection: Perspective(45.0, 640.0 / 480.0, 1.0, 100.0)

with gl.modelview:
    Translate(0.0, 0.0, -10)
    Scale(2.0, 2.0, 2.0)

texture = Texture2D()
texture.image = checkerboard_teximage(16, 16, primary=(255, 255, 255))
texture.filter.min = NEAREST
texture.filter.mag = NEAREST

gl.textures[0] = texture
texture.enable()

per_pixel.attribs._dump()
per_pixel.uniforms._dump()

toggle_texture = Cycle([texture.enable, texture.disable])

frames = 0
time = Timer()
seconds = Timer()
pause = False
while True:
    gl.color.clear()
    gl.depth.clear()
    elapsed = time.elapsed()

    frames += 1
    if seconds.has_elapsed(1.0):
        print "FPS:", frames
        frames = 0

    for event in pygame.event.get():
        if event.type == QUIT: exit(0)
        if event.type == KEYDOWN:
            if event.unicode == 's':
                programs.next()()
            if event.unicode == 'p':
                pause = not pause
            if event.unicode == 'd':
                draw_function = draw_funcs.next()
            if event.unicode == 't':
                toggle_texture.next()()
            if event.unicode == 'q': exit(0)

    if not pause:
        with gl.modelview:
            Rotate(elapsed * 90, 0, 1, 0)

    draw_function(gl)

    gl.flip()
