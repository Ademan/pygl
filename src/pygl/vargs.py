from ctypes import c_float, c_double

def throw_argcount(*args):
    raise RuntimeError("Invalid argument count")

class VargFunction(object):
    def __init__(self, functions):
        self.functions = functions
    def __call__(self, *args):
        if len(args) == 1:
            args = args[0]
        try:
            return self.functions[len(args)](*args)
        except IndexError:
            raise RuntimeError("Invalid argument count")
