#!/bin/bash
set -e
ROOT=`dirname "${BASH_SOURCE[0]}"`
export DJANGO_SETTINGS_MODULE=abudget.settings
export PYTHONDONTWRITEBYTECODE='dontwrite'

export AB_DEBUG="True"

${ROOT}/venv.sh ./src/manage.py $@
