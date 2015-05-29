#!/usr/bin/env sh

python manage.py makemessages -a
python manage.py makemessages -a -d djangojs
