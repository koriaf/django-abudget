#!/bin/bash
set -e
ROOT=`dirname "${BASH_SOURCE[0]}"`
export DJANGO_SETTINGS_MODULE=abudget.settings.local
export PYTHONDONTWRITEBYTECODE='dontwrite'
${ROOT}/venv.sh ./src/manage.py $@
