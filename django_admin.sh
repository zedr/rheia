#!/bin/bash

source env/bin/activate
manage="$(which python) scripts/manage.py"

PYTHONPATH=. $manage $@
