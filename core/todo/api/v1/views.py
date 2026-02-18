from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticatedOrReadOnly ,IsAuthenticated# type: ignore
from .permissions import IsOwnerOrReadOnly
from todo.models import Task
from .serializers import TaskSerializer
from rest_framework import permissions # type: ignore
from rest_framework import viewsets # type: ignore
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .paginations import DefaultPagination


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly,IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['complete']
    search_fields = ['title']
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    





