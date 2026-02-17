from django.urls import reverse
from rest_framework.test import APIClient
import pytest
from accounts.models import User
from todo.models import Task


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def other_user(db):
    user = User.objects.create_user(
        email="user2@user2.com", password="@#1234567", is_verified=True
    )
    return user


@pytest.fixture
def common_user(db):
    user = User.objects.create_user(
        email="admin@admin.com", password="@#1234567", is_verified=True
    )
    return user


@pytest.fixture
def task(db, common_user):
    return Task.objects.create(user=common_user, title="Existing Task")


@pytest.mark.django_db
class TestTaskApi:

    def test_get_task_response_401_status(self, api_client):
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_task_response_200_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_response_401_status(self, api_client):
        url = reverse("todo:api-v1:task-list")
        data = {"title": "test", "complete": True}
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_task_response_201_status(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        data = {"title": "test", "complete": True}
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_task_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("todo:api-v1:task-list")
        data = {"complete": True}
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_update_task_response_401_status(self, api_client, task):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})
        data = {"title": "update-task", "complete": True}

        response = api_client.put(url, data, format="json")
        assert response.status_code == 401

    def test_update_task_response_200_status(self, api_client, common_user, task):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})
        data = {"title": "update-task", "complete": True}
        api_client.force_authenticate(user=common_user)
        response = api_client.put(url, data, format="json")
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.title == "update-task"
        assert task.complete is True

    def test_partial_update_task_response_401_status(self, api_client, task):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})
        data = {
            "title": "partial-update-task",
        }
        response = api_client.patch(url, data, format="json")
        assert response.status_code == 401

    def test_partial_update_task_response_200_status(
        self, api_client, common_user, task
    ):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})
        data = {
            "title": "partial-update-task",
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.patch(url, data, format="json")
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.title == "partial-update-task"
        assert task.complete == task.complete

    def test_delete_task_response_401_status(self, api_client, task):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})
        response = api_client.delete(url)
        assert response.status_code == 401

    def test_delete_task_response_404_status(self, api_client, other_user, task):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})
        api_client.force_authenticate(user=other_user)
        response = api_client.delete(url)
        assert response.status_code in [403, 404]
        assert Task.objects.filter(id=task.id).exists() is True

    def test_delete_task_response_204_status(self, api_client, common_user, task):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})
        api_client.force_authenticate(user=common_user)
        response = api_client.delete(url)
        assert response.status_code == 204
        assert Task.objects.filter(id=task.id).exists() is False
