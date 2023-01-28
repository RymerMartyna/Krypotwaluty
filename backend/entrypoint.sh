#!/bin/sh

#python manage.py migrate
#python manage.py collectstatic --no-input


python manage.py migrate
python manage.py migrate auth
python manage.py migrate sessions
python manage.py migrate admin
python manage.py migrate contenttypes
python manage.py migrate messages
python manage.py migrate staticfiles

DJANGO_SUPERUSER_PASSWORD=$DJANGO_USER_PASSWORD python manage.py createsuperuser --username $DJANGO_USER_NAME --email $DJANGO_USER_EMAIL --noinput

python manage.py runserver 0.0.0.0:8000