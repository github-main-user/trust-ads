import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(django_user_model: User):
    return django_user_model.objects.create_user(
        email="user@user.com", password="pass", role=User.UserRole.USER
    )


@pytest.fixture
def admin(django_user_model: User):
    return django_user_model.objects.create_user(
        email="admin@admin.com", password="pass", role=User.UserRole.ADMIN
    )
