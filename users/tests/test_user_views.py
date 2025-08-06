import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


# token obtain pair


@pytest.mark.django_db
def test_obtain_token_pair_success(api_client, user):
    response = api_client.post(
        reverse("users:token-obtain-pair"),
        {"email": "user@user.com", "password": "pass"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_obtain_token_pair_wrong_credentials(api_client, user):
    response = api_client.post(
        reverse("users:token-obtain-pair"),
        {"email": "user@user.com", "password": "WRONG"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "access" not in response.data
    assert "refresh" not in response.data


# token refresh


@pytest.mark.django_db
def test_token_refresh_token_success(api_client, user):
    response = api_client.post(
        reverse("users:token-obtain-pair"),
        {"email": "user@user.com", "password": "pass"},
    )

    assert response.status_code == status.HTTP_200_OK

    refresh_token = response.data.get("refresh")
    response = api_client.post(
        reverse("users:token-refresh"), {"refresh": refresh_token}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_token_refresh_token_invalid(api_client):
    response = api_client.post(reverse("users:token-refresh"), {"refresh": "WRONG"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "access" not in response.data


# registration


@pytest.mark.django_db
def test_user_register_success(api_client):
    assert User.objects.filter(email="user@user.com").count() == 0
    response = api_client.post(
        reverse("users:user-register"), {"email": "user@user.com", "password": "pass"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert User.objects.filter(id=response.data.get("id")).exists()


@pytest.mark.django_db
def test_user_register_already_exists(api_client, user):
    response = api_client.post(
        reverse("users:user-register"), {"email": user.email, "password": "pass"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "id" not in response.data


# me/ retrieve


@pytest.mark.django_db
def test_me_retrieve_unauthenticated(api_client):
    response = api_client.get(reverse("users:user-me"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_me_retrieve_success(api_client, user):
    api_client.force_authenticate(user)
    response = api_client.patch(reverse("users:user-me"))

    assert response.status_code == status.HTTP_200_OK
    assert user.email == response.data.get("email")


# me/ update


@pytest.mark.django_db
def test_me_update_unauthenticated(api_client):
    response = api_client.patch(reverse("users:user-me"), {"first_name": "UPDATED"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not User.objects.filter(first_name="UPDATE").exists()


@pytest.mark.django_db
def test_me_update_success(api_client, user):
    api_client.force_authenticate(user)
    response = api_client.patch(reverse("users:user-me"), {"first_name": "UPDATED"})

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.first_name == "UPDATED"


# me/ delete


@pytest.mark.django_db
def test_me_delete_unauthenticated(api_client):
    count_before = User.objects.count()
    response = api_client.delete(reverse("users:user-me"))
    count_after = User.objects.count()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert count_before == count_after


@pytest.mark.django_db
def test_me_delete_success(api_client, user):
    api_client.force_authenticate(user)
    response = api_client.delete(reverse("users:user-me"))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(id=user.id).exists()


# change password


def test_change_password_unauthenticated(api_client):
    response = api_client.put(
        reverse("users:user-change-password"),
        {"old_password": "pass", "new_password": "new_pass"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_change_password_success(api_client, user):
    api_client.force_authenticate(user)
    response = api_client.put(
        reverse("users:user-change-password"),
        {"old_password": "pass", "new_password": "NEWPASSWORD"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert user.check_password("NEWPASSWORD")


@pytest.mark.django_db
def test_change_password_wrong_old_password(api_client, user):
    api_client.force_authenticate(user)
    response = api_client.put(
        reverse("users:user-change-password"),
        {"old_password": "WRONG", "new_password": "NEWPASSWORD"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not user.check_password("NEWPASSWORD")
