from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework import viewsets  # type: ignore
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from todo.models import Task
from .paginations import DefaultPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import TaskSerializer


class TaskModelViewSet(viewsets.ModelViewSet):
    # queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  #
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["complete"]
    search_fields = ["title"]
    pagination_class = DefaultPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(user=self.request.user)
        return Task.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
