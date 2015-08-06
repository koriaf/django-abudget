#!/bin/bash
set -e
export PYTHONDONTWRITEBYTECODE='dontwrite'
./manage.sh runserver 127.0.0.1:6835
