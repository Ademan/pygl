#! /usr/bin/env python
from time import clock

import pygame
from pygame.locals import *

import pygl
from pygl.shader import VertexShader, FragmentShader, Program

from pygl.constants import DEPTH_TEST

from pygl.glu import Perspective
from pygl.util import Translate, Rotate, Scale
from pygl.pygame_context import load_image

from pygl.texture import Texture2D

window = pygl.window.PygameWindow(640, 480)

gl = window.context

texture = Texture2D()

image = load_image('/home/dan/Pictures/test-texture.png')

texture.image = image

def draw_plane(quad, normal):
    #quad.color(
    quad.normal(normal)

def draw_cube(gl):
    with gl.quads() as q:
        #top
        q.color(1.0, 1.0, 1.0)
        q.normal(0.0, 1.0, 0.0)
        q.vertex(-1.0, 1.0, -1.0)
        q.vertex(1.0, 1.0, -1.0)
        q.vertex(1.0, 1.0, 1.0)
        q.vertex(-1.0, 1.0, 1.0)

        #bottom
        q.normal(0.0, -1.0, 0.0)
        q.vertex(-1.0, -1.0, -1.0)
        q.vertex(1.0, -1.0, -1.0)
        q.vertex(1.0, -1.0, 1.0)
        q.vertex(-1.0, -1.0, 1.0)

        #front
        q.color(1.0, 0.0, 0.0)
        q.normal(0.0, 0.0, 1.0)
        q.vertex(-1.0, -1.0, 1.0)
        q.vertex(-1.0, 1.0, 1.0)
        q.vertex(1.0, 1.0, 1.0)
        q.vertex(1.0, -1.0, 1.0)

        #back
        q.color(0.0, 1.0, 0.0)
        q.normal(0.0, 0.0, -1.0)
        q.vertex(1.0, -1.0, -1.0)
        q.vertex(1.0, 1.0, -1.0)
        q.vertex(-1.0, 1.0, -1.0)
        q.vertex(-1.0, -1.0, -1.0)

        #left
        q.color(0.0, 0.0, 1.0)
        q.normal(-1.0, 0.0, 0.0)
        q.vertex(-1.0, -1.0, -1.0)
        q.vertex(-1.0, 1.0, -1.0)
        q.vertex(-1.0, 1.0, 1.0)
        q.vertex(-1.0, -1.0, 1.0)

        #right
        q.color(1.0, 0.0, 1.0)
        q.normal(1.0, 0.0, 0.0)
        q.vertex(1.0, -1.0, 1.0)
        q.vertex(1.0, 1.0, 1.0)
        q.vertex(1.0, 1.0, -1.0)
        q.vertex(1.0, -1.0, -1.0)

class Timer(object):
    def __init__(self):
        self._last = clock()

    def elapsed(self):
        current = clock()
        elapsed = current - self._last
        self._last = clock()
        return elapsed

    def has_elapsed(self, time):
        current = clock()
        elapsed = current - self._last
        if elapsed > time:
            self._last = clock()
            return True
        else:
            return False

def create_program(vertex_shader, fragment_shader):
    vs = VertexShader()
    fs = FragmentShader()
    program = Program()

    vs.sources = [vertex_shader]
    fs.sources = [fragment_shader]

    if not vs.compile():
        print "Vertex Shader log:", vs.log

    if not fs.compile():
        print "Fragment Shader log:", fs.log

    program.shaders.extend([vs, fs])
    if not program.link():
        print "Program log:", program.log

    if not program.validate():
        print "Invalid"

    return program

per_pixel = create_program(open('pixel.vert'), open('pixel.frag'))
per_vertex = create_program(open('vertex.vert'), open('vertex.frag'))
programs = [per_pixel, per_vertex]
program = per_pixel

if not per_pixel.use():
    print "Program log:", per_pixel.log

gl.enable(DEPTH_TEST)

with gl.projection: Perspective(45.0, 640.0 / 480.0, 1.0, 100.0)

with gl.modelview:
    Translate(0.0, 0.0, -10)
    Scale(2.0, 2.0, 2.0)

print "Max Texture Units:", len(gl.textures)

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
        print "FPS: ", frames
        frames = 0

    for event in pygame.event.get():
        if event.type == QUIT: exit(0)
        if event.type == KEYDOWN:
            if event.unicode == 's':
                unused = [p for p in programs if not p is program][0]
                unused.use()
                program = unused
            if event.unicode == 'p':
                pause = not pause

    if not pause:
        with gl.modelview:
            Rotate(elapsed * 90, 0, 1, 0)

    draw_cube(gl)

    gl.flip()
