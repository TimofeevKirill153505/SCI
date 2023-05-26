from django.test import Client
from django.contrib.auth.models import User
from django.conf import settings

from ..models import ClientModel

import pytest as p_t


@p_t.fixture(autouse=True)
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'ATOMIC_REQUESTS': True,
    }

@p_t.fixture
def user():
    return User.objects.get(username="__bolvanka__")

