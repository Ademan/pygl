#! /bin/bash

function read_constants
{
    egrep "#define[[:space:]]+(GL_[A-Z0-9_]+)" $1 |\
    sed -re 's/^#define\s+(GL_[A-Z0-9x_]+)\s+(0x[0-9A-Fa-f]+|[0-9]+L?).*$/\1="\2"/' |\
    grep -v '#define'
}

#echo 'from gltypes import GLenum'
#echo
#read_constants $1 | sed -re 's/="((0x)?[0-9A-Fa-f]+)"/=GLenum(\1)/' | sed -e 's/^GL_//' | sed -re 's/^([0-9])/_\1/'
read_constants $1 | sed -re 's/="((0x)?[0-9A-Fa-f]+)"/=\1/' | sed -e 's/^GL_//' | sed -re 's/^([0-9])/_\1/'
