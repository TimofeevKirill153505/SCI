from django.test import Client
from django.contrib.auth.models import User
from django.conf import settings


import pytest as p_t


@p_t.fixture(autouse=True)
def django_db_setup():
    # settings.configure()
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'ATOMIC_REQUESTS': True,
    }

@p_t.fixture
def user():
    return User.objects.get(username="__bolvanka__")

@p_t.fixture
def client():
    return Client()

