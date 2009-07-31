#! /bin/bash

function read_constants
{
    egrep "#define[[:space:]]+([A-Z0-9_]+)" $1 |\
    sed -re 's/^#define\s+(GL_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+)/\1="\2"/' |\
    grep -v '#define'
}

echo 'from gltypes import GLenum'
read_constants $1 | sed -re 's/="((0x)?[0-9A-fa-f)"/=GLenum(\1)'
