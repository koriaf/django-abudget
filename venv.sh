#!/bin/bash
ROOT=`dirname "${BASH_SOURCE[0]}"`
act="${ROOT}/.venv/bin/activate"

if [ ! -f "${act}" ]; then
    set -e
    pyvenv ${ROOT}/.venv
    source ${act}
    pip install pip wheel --upgrade
    pip install -r system/requirements.test.txt
    set +e
else
    source ${act}
fi

ARGS="$@"
if [ -n "${ARGS}" ]; then
    cd ${ROOT}
    exec $@
fi
