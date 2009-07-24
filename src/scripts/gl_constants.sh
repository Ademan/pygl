#! /bin/bash

function constant
{
    echo '$1 = c_uint($2)'
}

function get_requests
{
    echo "$1"
    sed -nre '/^#\s+Begin\s+GL\s+Constants$/,/^#End\s+GL\s+Constants$/s/^#\s*GL_([A-Z0-9_]+)\s*$/\1/p' $1
}

function append_constant
{
    echo "$(cat)|$1"
}

function retrieve_constants
{
    i=0
    cat | while read request; do
       constants=$(echo "$constants" | append_constant $request)
    done

    constants=$(egrep "#define[[:space:]]+($constants)" $1 |\
    sed -re 's/^#define\s+(GL_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+)/\1="\2"/' |\
    grep -v '#define')
    $constants
}

#FIXME: sed character classes?
#echo 'from ctypes import c_uint'
#egrep '#define[[:space:]]+GL' $1 | sed -re 's/^#define\s+(GL_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+)/\1 = c_uint(\2)/' | grep -v '#define'

get_requests $1
