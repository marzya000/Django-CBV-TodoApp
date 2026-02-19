from django.urls import path, include
from . import views

app_name = "todo"
urlpatterns = [   
    path("", views.TaskList.as_view(), name="task_list"),
   # path("task/api/", views.TaskListApi.as_view(), name="task_list_api"),
    path("task/create/", views.TaskCreate.as_view(), name="task_create"),
    path("task/update/<int:pk>/", views.TaskUpdate.as_view(), name="task_update"),
    path(
        "task/complete/<int:pk>/",
        views.TaskComplete.as_view(),
        name="task_complete",
    ),
    path("task/delete/<int:pk>/", views.TaskDelete.as_view(), name="task_delete"),
    path("api/v1/", include(("todo.api.v1.urls", "api-v1"), namespace="api-v1")),
]
