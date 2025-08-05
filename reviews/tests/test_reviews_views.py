import pytest
from django.urls import reverse
from rest_framework import status

from reviews.models import Review

# fixtures


@pytest.fixture
def reviews(review_factory) -> list[Review]:
    return [
        review_factory(),
        review_factory(),
        review_factory(),
        review_factory(),
        review_factory(),
    ]


# list


@pytest.mark.django_db
def test_reviews_list_unauthenticated(api_client, reviews):
    response = api_client.get(reverse("ads:ads-review-list", args=[reviews[0].ad.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_reviews_list_success(api_client, reviews):
    api_client.force_authenticate(reviews[0].author)
    response = api_client.get(reverse("ads:ads-review-list", args=[reviews[0].ad.id]))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(reviews)


@pytest.mark.django_db
def test_reviews_list_ad_not_found(api_client, reviews):
    api_client.force_authenticate(reviews[0].author)
    response = api_client.get(reverse("ads:ads-review-list", args=[0]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert len(response.data) == 1
    assert "detail" in response.data


# create


@pytest.mark.django_db
def test_reviews_create_unauthenticated(api_client, ad, review_data):
    assert not Review.objects.filter(text=review_data["text"]).exists()

    response = api_client.post(
        reverse("ads:ads-review-list", args=[ad.id]), review_data
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "id" not in response.data
    assert not Review.objects.filter(text=review_data["text"]).exists()


@pytest.mark.django_db
def test_reviews_create_success(api_client, ad, user, review_data):
    assert not Review.objects.filter(text=review_data["text"]).exists()

    api_client.force_authenticate(user)
    response = api_client.post(
        reverse("ads:ads-review-list", args=[ad.id]), review_data
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    review = Review.objects.get(id=response.data.get("id"))
    assert review.author == user
    assert review.ad == ad


# retrieve


@pytest.mark.django_db
def test_reviews_retrieve_unauthenticated(api_client, ad, review):
    response = api_client.get(reverse("ads:ads-review-detail", args=[ad.id, review.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "id" not in response.data


@pytest.mark.django_db
def test_reviews_retrieve_success(api_client, ad, review):
    api_client.force_authenticate(review.author)
    response = api_client.get(reverse("ads:ads-review-detail", args=[ad.id, review.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("id") == review.id


# update


@pytest.mark.django_db
def test_reviews_update_unauthenticated(api_client, ad, review):
    response = api_client.patch(
        reverse("ads:ads-review-detail", args=[ad.id, review.id]), {"text": "UPDATED"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    review.refresh_from_db()
    assert review.text != "UPDATED"


@pytest.mark.django_db
def test_reviews_update_as_author_success(api_client, ad, review):
    api_client.force_authenticate(review.author)
    response = api_client.patch(
        reverse("ads:ads-review-detail", args=[ad.id, review.id]), {"text": "UPDATED"}
    )

    assert response.status_code == status.HTTP_200_OK
    review.refresh_from_db()
    assert review.text == "UPDATED"


@pytest.mark.django_db
def test_reviews_update_as_random_user_fail(api_client, ad, review, random_user):
    api_client.force_authenticate(random_user)
    response = api_client.patch(
        reverse("ads:ads-review-detail", args=[ad.id, review.id]), {"text": "UPDATED"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    review.refresh_from_db()
    assert review.text != "UPDATED"


@pytest.mark.django_db
def test_reviews_update_as_admin_success(api_client, ad, review, admin):
    api_client.force_authenticate(admin)
    response = api_client.patch(
        reverse("ads:ads-review-detail", args=[ad.id, review.id]), {"text": "UPDATED"}
    )

    assert response.status_code == status.HTTP_200_OK
    review.refresh_from_db()
    assert review.text == "UPDATED"


# delete


@pytest.mark.django_db
def test_reviews_delete_unauthenticated(api_client, ad, review):
    response = api_client.delete(
        reverse("ads:ads-review-detail", args=[ad.id, review.id])
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Review.objects.filter(id=review.id).exists()


@pytest.mark.django_db
def test_reviews_delete_as_author_success(api_client, ad, review):
    api_client.force_authenticate(review.author)
    response = api_client.delete(
        reverse("ads:ads-review-detail", args=[ad.id, review.id])
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Review.objects.filter(id=review.id).exists()


@pytest.mark.django_db
def test_reviews_delete_as_random_user_fail(api_client, ad, review, random_user):
    api_client.force_authenticate(random_user)
    response = api_client.delete(
        reverse("ads:ads-review-detail", args=[ad.id, review.id])
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Review.objects.filter(id=review.id).exists()


@pytest.mark.django_db
def test_reviews_delete_as_admin_success(api_client, ad, review, admin):
    api_client.force_authenticate(admin)
    response = api_client.delete(
        reverse("ads:ads-review-detail", args=[ad.id, review.id])
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Review.objects.filter(id=review.id).exists()
