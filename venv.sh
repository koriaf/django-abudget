#!/bin/bash
ROOT=`dirname "${BASH_SOURCE[0]}"`
act="${ROOT}/system/venv/bin/activate"

if [ ! -f "${act}" ]; then
    set -e
    /usr/local/bin/pyvenv ${ROOT}/system/venv
    source ${act}
    wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
    wget https://bootstrap.pypa.io/get-pip.py -O - | python
    set +e
else
    source ${act}
fi

ARGS="$@"
if [ -n "${ARGS}" ]; then
    cd ${ROOT}
    exec $@
fi
