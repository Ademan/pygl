#! /usr/bin/env python
from time import clock

import pygame
from pygame.locals import *

import pygl
from pygl.shader import VertexShader, FragmentShader, Program

from pygl.constants import DEPTH_TEST

from pygl.glu import Perspective
from pygl.util import Translate, Rotate, Scale

window = pygl.window.PygameWindow(640, 480)

gl = window.context

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

    if program.validate():
        print "Valid"
    else:
        print "Invalid"

    print program._object

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

frames = 0
last = clock()
last_second = last
while True:
    gl.color.clear()
    gl.depth.clear()
    for event in pygame.event.get():
        if event.type == QUIT: exit(0)
        if event.type == KEYDOWN:
            if event.unicode == 's':
                unused = [p for p in programs if not p is program][0]
                unused.use()
                program = unused

    with gl.modelview:
        current = clock()
        Rotate((current - last) * 90, 0, 1, 0)
        last = current
        frames += 1
        second_progress = current - last_second
        if second_progress >= 1.0:
            print "FPS: ", frames
            last_second = current
            frames = 0

    draw_cube(gl)

    gl.flip()
