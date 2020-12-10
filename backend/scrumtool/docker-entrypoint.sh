#!/bin/bash -x

echo "execute python manage.py migrate "
python manage.py migrate
echo "execute manage.py runserver 0.0.0.0:8000 "
python manage.py runserver 0.0.0.0:8000
echo "execute python manage.py runapscheduler "
python manage.py runapscheduler
exec "$@"

