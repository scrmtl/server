#!/bin/bash -x

echo "execute manage.py runserver 0.0.0.0:8000 "
python manage.py runserver 0.0.0.0:8000 --noreload

exec "$@"

