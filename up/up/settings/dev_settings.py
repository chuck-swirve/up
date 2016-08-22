import os

from django.contrib.messages import constants as message_constants


SECRET_KEY = 'niqvma8gtothigsu%=j)ngig8ghs04$cemi_8-q^qe$4_-e-(y'
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'utopia',
        'USER': 'utopiadev',
        'PASSWORD': 'localdev',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
# Dev-mode email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
