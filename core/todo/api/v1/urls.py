from . import views
from rest_framework.routers import DefaultRouter  # type: ignore

app_name = "api-v1"

router = DefaultRouter()
router.register("task", views.TaskModelViewSet, basename="task")


urlpatterns = []
urlpatterns += router.urls
