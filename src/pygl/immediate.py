from pygl._gl import lib as _gl

from pygl.constants import GL_TRIANGLES, GL_QUADS, GL_POINTS

from ctypes import c_int, c_int8, c_int16, c_int32
from ctypes import c_uint, c_uint8, c_uint16, c_uint32
from ctypes import c_float, c_double

from pygl.util import _norm_args

#TODO: move me elsewhere!
def strlist(xs, minsep=', ', majsep='or'):
    last = xs.pop()
    init = xs
    return (minsep + majsep).join([minsep.join(map(str, init)), str(last)])

#TODO: move me elsewhere!
_gl_typenames = {
    c_int8: 'b',
    c_int16: 's',
    c_int32: 'i',
    c_int: 'i',

    c_uint8: 'ub',
    c_uint16: 'us',
    c_uint32: 'ui',
    c_uint: 'ui',

    c_double: 'd',
    c_float: 'f',
    }

#TODO: move me elsewhere!
_python_numeric_types = {
                            float: c_double,
                            int: c_int32
                        }

#TODO: move me elsewhere!
_c_numeric_types = {
                    c_int: int,
                    c_int8: int,
                    c_int16: int,
                    c_int32: int,
                    c_uint: int,
                    c_uint8: int,
                    c_uint16: int,
                    c_uint32: int,
                    c_float: float,
                    c_double: float
                   }

#TODO: move me elsewhere?
def homogenous(xs):
    for x in xs:
        try:
            if last != x: return False
        except NameError: continue
    return True

class ImmediateFunction(object):
    #FIXME: possible breakage, assigning module level globals to class
    _python_numeric_types = _python_numeric_types
    _c_numeric_types = _c_numeric_types
    def __init__(self, name, types, counts):
        self.name = name
        self.types = types
        self.counts = counts #valid argument counts
    def _sanitize_args(self, args):
        args = _norm_args(args)

        if not len(args) in self.counts:
            raise TypeError("%(name)s takes %(counts)s arguments" % {"name": self.name, "counts": strlist(self.counts)})

        if not homogenous(map(type, args)):
            args = map(float, args) #FIXME: super-duper naive coersion

        return args

    def _generate_carray(self, args, type):
        #FIXME: rather than using the pointer functions
        #FIXME: use list expansion instead?
        return (type * len(args))(*args)

    def _determine_type(self, args):
        return type(args[0])

    def _determine_gl_type(self, args):
        type = self._determine_type(args)

        if type in self._python_numeric_types:
            type = self._python_numeric_types[type]

        return type

    def _function_name(self, args, type):
        return self.name % {'count': len(args),
                            'type': _gl_typenames[type]}

    def __call__(self, *args):
        args = self._sanitize_args(args)
        type = self._determine_gl_type(args)

        #TODO: eventually cache lookups?
        getattr(_gl, self._function_name(args, type))(self._generate_carray(args, type))

class ImmediateMode(object):
    def _add_fixed_function(self):
        self.vertex = ImmediateFunction("glVertex%(count)d%(type)cv", [float, int],
                                   [2, 3, 4])

        self.texcoord = ImmediateFunction("glTexCoord%(count)d%(type)cv", [float, int],
                                   [1, 2, 3, 4])

        self.color = ImmediateFunction("glColor%(count)d%(type)cv", [float, int],
                                   [3, 4])

        self.normal = ImmediateFunction("glNormal%(count)d%(type)cv", [float],
                                   [3])

    def __exit__(self, exc_type, exc_val, exc_tb):
        _gl.glEnd()

class TrianglesMode(ImmediateMode):
    def __init__(self): self._add_fixed_function()
    def __enter__(self):
        _gl.glBegin(GL_TRIANGLES)
        return self

class QuadsMode(ImmediateMode):
    def __init__(self): self._add_fixed_function()
    def __enter__(self):
        _gl.glBegin(GL_QUADS)
        return self

class QuadsMode(ImmediateMode):
    def __init__(self): self._add_fixed_function()
    def __enter__(self):
        _gl.glBegin(GL_POINTS)
        return self
