from time import clock
from time import time

from pygl.texture import TextureImage
from pygl.shader import VertexShader, FragmentShader, Program
from pygl.constants import RGB, UNSIGNED_BYTE

from struct import pack

from ctypes import create_string_buffer
from ctypes import c_int
from ctypes import c_void_p, cast

def checkerboard_teximage(w, h, primary=(255, 0, 255), secondary=(0, 0, 0)):
    assert not w % 2
    assert not h % 2
    image = TextureImage()

    image.width = w
    image.height = h

    image.level = 0
    image.storage = c_int(3)
    image.format = RGB
    image.type = UNSIGNED_BYTE
    image.border = 0

    size = w * h * 3

    pairs = Cycle([primary + secondary, secondary + primary])
    data = ''.join([pack('BBBBBB', *(pairs.next())) * (w / 2) for line in xrange(h)])

    image.data = create_string_buffer(data, size)

    return image

def draw_plane(quad, normal):
    s = [-1.0, -1.0, 1.0, 1.0]
    t = [-1.0, 1.0, 1.0, -1.0]

    def vertex(s, t):
        i = iter((s, t))
        quad.vertex([i.next() if x == 0.0 else x for x in normal])

    quad.normal(normal)
    for s, t in zip(s, t):
        quad.texcoord(s, t)
        vertex(s, t)

def draw_cube(gl):
    with gl.quads() as quad:
        #top
        quad.color(1.0, 1.0, 1.0)
        draw_plane(quad, (0.0, 1.0, 0.0))

        #bottom
        quad.normal(0.0, -1.0, 0.0)
        draw_plane(quad, (0.0, -1.0, 0.0))

        #front
        quad.color(1.0, 0.0, 0.0)
        draw_plane(quad, (0.0, 0.0, 1.0))

        #back
        quad.color(0.0, 1.0, 0.0)
        draw_plane(quad, (0.0, 0.0, -1.0))

        #left
        quad.color(0.0, 0.0, 1.0)
        draw_plane(quad, (-1.0, 0.0, 0.0))

        #right
        quad.color(1.0, 0.0, 1.0)
        draw_plane(quad, (1.0, 0.0, 0.0))

def draw_textured_quad(gl):
    with gl.quads() as q:
        q.color(1.0, 1.0, 1.0)
        #q.color(0.5, 0.5, 0.5)
        q.normal(0.0, 0.0, 1.0)
        q.texcoord(0.0, 0.0)
        q.vertex(-1.0, -1.0, 0.0)

        q.texcoord(0.0, 1.0)
        q.vertex(-1.0, 1.0, 0.0)

        q.texcoord(1.0, 1.0)
        q.vertex(1.0, 1.0, 0.0)

        q.texcoord(1.0, 0.0)
        q.vertex(1.0, -1.0, 0.0)

class Timer(object):
    def __init__(self):
        self._last = time()

    def __call__(self): return time()

    def elapsed(self):
        current = time()
        elapsed = current - self._last
        self._last = time()
        return elapsed

    def has_elapsed(self, wait_time):
        current = time()
        elapsed = current - self._last
        if elapsed > wait_time:
            self._last = time() - elapsed + wait_time
            #self._last = time()
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

class Cycle(object):
    def __init__(self, objects):
        self._objects = objects
        self.reset()
    def __iter__(self): return self
    def reset(self):
        self._iter = iter(self._objects)
    def next(self):
        try:
            return self._iter.next()
        except StopIteration:
            self._iter = iter(self._objects)
            return self._iter.next()
