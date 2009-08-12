from pygl._gl import Functionality

from pygl.gltypes import GLenum

from pygl.constants import NO_ERROR, INVALID_ENUM, INVALID_VALUE, INVALID_OPERATION
from pygl.constants import STACK_OVERFLOW, STACK_UNDERFLOW, OUT_OF_MEMORY
from pygl.constants import TABLE_TOO_LARGE

error_handling = Functionality({'':
                                    {
                                     'GetError': ('glGetError', [], GLenum),
                                     }
                              })

GetError = error_handling.GetError

class GLError(RuntimeError): pass

class InvalidEnum(GLError): pass

class InvalidValue(GLError): pass

class InvalidOperation(GLError): pass

class StackOverflow(GLError): pass

class StackUnderflow(GLError): pass

class OutOfMemory(GLError): pass

class TableTooLarge(GLError): pass

_errors = {
            INVALID_ENUM.value: InvalidEnum,
            INVALID_VALUE.value: InvalidValue,
            INVALID_OPERATION.value: InvalidOperation,
            STACK_OVERFLOW.value: StackOverflow,
            STACK_UNDERFLOW.value: StackUnderflow,
            OUT_OF_MEMORY.value: OutOfMemory,
            TABLE_TOO_LARGE.value: TableTooLarge
          }

def _check_errors():
    error = GetError()
    try:
        raise _errors[error]() #FIXME: make the tracebacks longer, don't need to report the error reporting...
    except KeyError:
        pass # either means NO_ERROR or an error we don't have an exception for

def _wrap_errors(f):
    def _checked_f(*args, **kwargs):
        f(*args, **kwargs)
        _check_errors()
    return _wrapped
