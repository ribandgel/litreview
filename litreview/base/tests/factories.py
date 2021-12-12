import os

import factory
import pytest
from django.contrib.auth import get_user_model
from django.core import management

from litreview import settings

nb_users = 12


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)


def generate_db():
    UserFactory.create_batch(nb_users)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker, fake_storage_backends):
    breakpoint()
    with django_db_blocker.unblock():
        dummy_db_file = os.path.join(settings.BASE_DIR, "base/tests/dummy_db.json")
        if os.path.exists(dummy_db_file):
            with open(dummy_db_file, "r") as f:
                management.call_command("loaddata", dummy_db_file)
        else:
            generate_db()
            with open(dummy_db_file, "w") as f:
                management.call_command("dumpdata", "account.emailaddress", "base", stdout=f)
