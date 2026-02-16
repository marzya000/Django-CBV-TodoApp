"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views 
from rest_framework.documentation import include_docs_urls # type: ignore
from accounts.views import *
from rest_framework import permissions # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore

schema_view = get_schema_view(
   openapi.Info(
      title="Todo API Documentation",
      default_version='v1',
      description="API documentation for Todo App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="marzya@mail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("accounts/", include("accounts.urls")),
    path('accounts/signup/',SignupView.as_view(),name='signup'),
    path('accounts/login/',views.LoginView.as_view(),name='login'),
    path('accounts/logout/',views.LogoutView.as_view(),name='logout'), 
    path('accounts/password_change/',views.PasswordChangeView.as_view(),name='password_change'),
    path('accounts/password_change/done/',views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('accounts/password_reset/',views.PasswordResetView.as_view(),name='password_reset'),
    path('accounts/password_reset/done',views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',views.PasswordResetView.as_view(),name='password_reset_confirm'),
    path('accounts/reset/done',views.PasswordResetConfirmView.as_view(),name='password_reset_complete'),
    path('',include('todo.urls')),
    path('api-docs/',include_docs_urls(title='api sample')),
    path('swagger/api.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# serving static and media for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)