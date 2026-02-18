from django.urls import reverse
from rest_framework.test import APIClient
import pytest
from accounts.models import User
from rest_framework.authtoken.models import Token


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@example.com", password="@#123456", is_verified=True
    )


@pytest.fixture
def token(user):
    return Token.objects.create(user=user)


@pytest.mark.django_db
class TestRegistrationApi:
    def test_get_registration_response_405_status(self, api_client):
        url = reverse("accounts:registration")
        response = api_client.get(url)
        assert response.status_code == 405

    def test_registration_success(self, api_client):
        url = reverse("accounts:registration")
        data = {
            "email": "user@test.com",
            "password": "123456@#",
            "password1": "123456@#",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201
        assert "email" in response.json()

    def test_registration_invalid(self, api_client):
        url = reverse("accounts:registration")
        data = {
            "email": "user",
            "password": "123456@#",
            "password1": "123456@#",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestJWTAuth:
    def test_jwt_create(self, api_client, user):
        url = reverse("accounts:jwt-create")
        data = {"email": "user@example.com", "password": "@#123456"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

        self.access = response.data["access"]
        self.refresh = response.data["refresh"]

    def test_jwt_refresh(self, api_client, user):
        create_url = reverse("accounts:jwt-create")
        response = api_client.post(
            create_url,
            {"email": "user@example.com", "password": "@#123456"},
            format="json",
        )
        refresh_token = response.data["refresh"]

        url = reverse("accounts:jwt-refresh")
        response = api_client.post(url, {"refresh": refresh_token}, format="json")

        assert response.status_code == 200
        assert "access" in response.data

    def test_jwt_verify(self, api_client, user):
        create_url = reverse("accounts:jwt-create")
        response = api_client.post(
            create_url,
            {"email": "user@example.com", "password": "@#123456"},
            format="json",
        )
        access_token = response.data["access"]

        url = reverse("accounts:jwt-verify")
        response = api_client.post(url, {"token": access_token}, format="json")

        assert response.status_code == 200


@pytest.mark.django_db
class TestChangePasswordApi:
    def test_change_password_success(self, api_client, user):
        url = reverse("accounts:change-password")
        api_client.force_authenticate(user=user)
        data = {
            "old_password": "@#123456",
            "new_password": "@#@#@#@#",
            "new_password1": "@#@#@#@#",
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.check_password("@#@#@#@#")

    def test_change_password_wrong_old_password(self, api_client, user):
        url = reverse("accounts:change-password")
        api_client.force_authenticate(user=user)
        data = {
            "old_password": "wrongpassword",
            "new_password": "@#654321",
            "new_password1": "@#654321",
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code in [400, 403]

    def test_change_password_with_mismatch_new_passwords(self, api_client, user):
        url = reverse("accounts:change-password")
        api_client.force_authenticate(user=user)
        data = {
            "old_password": "@#123456",
            "new_password": "@#65432100",
            "new_password1": "@#654321",
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == 400

    def test_change_password_unauthenticated(self, api_client, user):
        url = reverse("accounts:change-password")
        data = {
            "old_password": "@#123456",
            "new_password": "@#@#@#@#",
            "new_password1": "@#@#@#@#",
        }
        response = api_client.put(url, data, format="json")

        assert response.status_code == 401
