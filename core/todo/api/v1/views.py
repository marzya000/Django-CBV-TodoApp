# from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import IsAuthenticated ,AllowAny # type: ignore
from rest_framework import viewsets # type: ignore
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
import requests #1
from decouple import config
from django.core.cache import cache #2
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.views import APIView #3
from rest_framework.response import Response #4
from rest_framework import status # 5
from .serializers import WeatherSerializer #6

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



API_KEY = config("OPENWEATHER_API_KEY")

class WeatherAPIView(generics.GenericAPIView):
    serializer_class = WeatherSerializer
    permission_classes = [AllowAny]
    def get(self, request):
        serializer = WeatherSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        city = serializer.validated_data["city"]
        cache_key = f"weather_{city}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response({"source": "cache", "data":cached_data})
        
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "fa"}
        response = requests.get(url, params=params, timeout=5)

        if response.status_code != 200:
            return Response({"error": "API error"}, status=500)
        
        data = response.json()
        weather_data = {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
        }

        cache.set(cache_key, weather_data, timeout=1200)  # 20 دقیقه

        return Response({"source": "api", "data": weather_data})

