#! /bin/bash

#FIXME: sed character classes?
echo 'from ctypes import c_uint'
egrep '#define[[:space:]]+GL' $1 | sed -re 's/^#define\s+(GL_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+)/\1 = c_uint(\2)/' | grep -v '#define'
