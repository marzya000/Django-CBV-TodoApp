from locust import HttpUser, task


class QuickstartUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/accounts/api/v2/jwt/create/",
            data={"email": "admin@admin.com", "password": "@#123456"},
        ).json()
        self.client.headers = {"Authorization": f"Bearer {response.get('access',None)}"}

    @task
    def task_list(self):
        self.client.get("/todo/api/v1/task/")
