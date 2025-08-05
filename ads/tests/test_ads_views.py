import pytest
from django.urls import reverse
from rest_framework import status

from ads.models import Ad

# fixtures


@pytest.fixture
def ads(ad_factory) -> list[Ad]:
    return [ad_factory(), ad_factory(), ad_factory(), ad_factory(), ad_factory()]


# list


@pytest.mark.django_db
def test_ads_list_unauthenticated_success(api_client, ads):
    response = api_client.get(reverse("ads:ad-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(ads)


@pytest.mark.django_db
def test_ads_list_success(api_client, ads, user):
    api_client.force_authenticate(user)
    response = api_client.get(reverse("ads:ad-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(ads)


# create


@pytest.mark.django_db
def test_ads_create_unauthenticated(api_client, ad_data):
    assert not Ad.objects.filter(title=ad_data["title"]).exists()

    response = api_client.post(reverse("ads:ad-list"), ad_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "id" not in response.data
    assert not Ad.objects.filter(title=ad_data["title"]).exists()


@pytest.mark.django_db
def test_ads_create_success(api_client, user, ad_data):
    assert not Ad.objects.filter(title=ad_data["title"]).exists()

    api_client.force_authenticate(user)
    response = api_client.post(reverse("ads:ad-list"), ad_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    ad = Ad.objects.get(id=response.data.get("id"))
    assert ad.author == user


# retrieve


@pytest.mark.django_db
def test_ads_retrieve_unauthenticated(api_client, ad):
    response = api_client.get(reverse("ads:ad-detail", args=[ad.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "id" not in response.data


@pytest.mark.django_db
def test_ads_retrieve_success(api_client, ad):
    api_client.force_authenticate(ad.author)
    response = api_client.get(reverse("ads:ad-detail", args=[ad.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("id") == ad.id


# update


@pytest.mark.django_db
def test_ads_update_unauthenticated(api_client, ad):
    response = api_client.patch(
        reverse("ads:ad-detail", args=[ad.id]), {"title": "UPDATED"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    ad.refresh_from_db()
    assert ad.title != "UPDATED"


@pytest.mark.django_db
def test_ads_update_as_author_success(api_client, ad):
    api_client.force_authenticate(ad.author)
    response = api_client.patch(
        reverse("ads:ad-detail", args=[ad.id]), {"title": "UPDATED"}
    )

    assert response.status_code == status.HTTP_200_OK
    ad.refresh_from_db()
    assert ad.title == "UPDATED"


@pytest.mark.django_db
def test_ads_update_as_random_user_fail(api_client, ad, random_user):
    api_client.force_authenticate(random_user)
    response = api_client.patch(
        reverse("ads:ad-detail", args=[ad.id]), {"title": "UPDATED"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    ad.refresh_from_db()
    assert ad.title != "UPDATED"


@pytest.mark.django_db
def test_ads_update_as_admin_success(api_client, ad, admin):
    api_client.force_authenticate(admin)
    response = api_client.patch(
        reverse("ads:ad-detail", args=[ad.id]), {"title": "UPDATED"}
    )

    assert response.status_code == status.HTTP_200_OK
    ad.refresh_from_db()
    assert ad.title == "UPDATED"


# delete


@pytest.mark.django_db
def test_ads_delete_unauthenticated(api_client, ad):
    response = api_client.delete(reverse("ads:ad-detail", args=[ad.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Ad.objects.filter(id=ad.id).exists()


@pytest.mark.django_db
def test_ads_delete_as_author_success(api_client, ad):
    api_client.force_authenticate(ad.author)
    response = api_client.delete(reverse("ads:ad-detail", args=[ad.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Ad.objects.filter(id=ad.id).exists()


@pytest.mark.django_db
def test_ads_delete_as_random_user_fail(api_client, ad, random_user):
    api_client.force_authenticate(random_user)
    response = api_client.delete(reverse("ads:ad-detail", args=[ad.id]))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Ad.objects.filter(id=ad.id).exists()


@pytest.mark.django_db
def test_ads_delete_as_admin_success(api_client, ad, admin):
    api_client.force_authenticate(admin)
    response = api_client.delete(reverse("ads:ad-detail", args=[ad.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Ad.objects.filter(id=ad.id).exists()
