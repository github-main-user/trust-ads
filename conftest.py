import pytest
from rest_framework.test import APIClient

from ads.models import Ad
from users.models import User

# general


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


# users


@pytest.fixture
def user_factory(db):
    def _user_factory(**kwargs):
        defaults = {
            "email": "user@user.com",
            "password": "pass",
            "role": User.UserRole.USER,
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)

    return _user_factory


@pytest.fixture
def user(user_factory):
    return user_factory()


@pytest.fixture
def random_user(user_factory):
    return user_factory(email="random@random.com")


@pytest.fixture
def admin(user_factory):
    return user_factory(email="admin@admin.com", role=User.UserRole.ADMIN)


# ads


@pytest.fixture
def ad_data() -> dict:
    return {
        "title": "Test Ad",
        "price": 1000,
        "description": "Test Description",
    }


@pytest.fixture
def ad_factory(db, user: User, ad_data: dict):
    def _ad_factory(**kwargs):
        defaults = ad_data | {"author": user}
        defaults.update(kwargs)
        return Ad.objects.create(**defaults)

    return _ad_factory


@pytest.fixture
def ad(ad_factory) -> Ad:
    return ad_factory()
