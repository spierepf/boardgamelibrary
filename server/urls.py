"""
URL configuration for server project.

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
from django.urls import path
from django.urls import include, path

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#project-configuration
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
    path("testOnly/", include("test_only.urls")),
    path('admin/', admin.site.urls),

    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#project-configuration
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/clientConfiguration/', views.client_configuration, name='client_configuration'),
    path('api/library/', include("library.urls")),
]
