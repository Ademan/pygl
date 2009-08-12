#! /usr/bin/env python
from time import clock

import pygame
from pygame.locals import *

import pygl
from pygl.shader import VertexShader, FragmentShader, Program

from pygl.constants import DEPTH_TEST

from pygl.glu import Perspective
from pygl.util import Translate, Rotate

window = pygl.window.PygameWindow(640, 480)

gl = window.context

def draw_triangle(gl):
    with gl.triangles() as t:
        t.color(1.0, 0.0, 0.0)
        t.vertex(-1.0, 0.0, 0.0)

        t.color(0.0, 1.0, 0.0)
        t.vertex(0.0, 1.0, 0.0)

        t.color(0.0, 0.0, 1.0)
        t.vertex(1.0, 0.0, 0.0)

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
        q.normal(-1.0, 0.0, 0.0)
        q.vertex(-1.0, -1.0, -1.0)
        q.vertex(-1.0, 1.0, -1.0)
        q.vertex(-1.0, 1.0, 1.0)
        q.vertex(-1.0, -1.0, 1.0)

        #right
        q.normal(1.0, 0.0, 0.0)
        q.vertex(1.0, -1.0, 1.0)
        q.vertex(1.0, 1.0, 1.0)
        q.vertex(1.0, 1.0, -1.0)
        q.vertex(1.0, -1.0, -1.0)

vs = VertexShader()

fs = FragmentShader()

program = Program()

vs.sources = ["""
varying vec3 position;
varying vec3 normal;
varying vec3 diffuse;
varying vec3 light;

void main(void)
{
    vec3 light_position = (gl_ProjectionMatrix * vec4(-2, 2, -10, 1.0)).xyz; //FIXME: pre-translated coords

    normal = normalize(gl_NormalMatrix * gl_Normal);

    diffuse = gl_Color.rgb;

    gl_Position = ftransform();
    position = gl_Position.xyz;
    light = normalize(light_position - position);
}
"""]

fs.sources = ["""
varying vec3 position;
varying vec3 normal;
varying vec3 diffuse;
varying vec3 light;

void main(void)
{
    f
    gl_FragColor = vec4(
                        dot(normalize(light), normalize(normal)) * diffuse,
                       1.0);
}
"""]

if not vs.compile():
    print "Vertex Shader log:", vs.log

if not fs.compile():
    print "Fragment Shader log:", fs.log

program.shaders.extend([vs, fs])
if not program.link():
    print "Program log:", program.log

print "Uniforms:"
program.uniforms._dump()

print "Attributes:"
program.attribs._dump()

if not program.use():
    print "Program log:", program.log

gl.enable(DEPTH_TEST)

with gl.projection: Perspective(45.0, 640.0 / 480.0, 1.0, 100.0)

with gl.modelview: Translate(0.0, 0.0, -10)

frames = 0
last = clock()
last_second = last
while True:
    gl.color.clear()
    gl.depth.clear()
    for event in pygame.event.get():
        if event.type == QUIT: exit(0)

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
