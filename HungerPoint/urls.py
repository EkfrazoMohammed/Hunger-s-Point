"""Logistics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from HungerPointApp.views import *

from django.views.generic.base import RedirectView
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('HungerPointApp.urls')),
    path(r'^$', serve,kwargs={'path': 'index.html'}),  # Serve index.html for the root URL
    path(r'^(?!/?statics/)(?!/?media/)(?P<path>.*\..*)$',
    RedirectView.as_view(url='/statics/%(path)s', permanent=False)),  # Serve other static files
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('hungerpoint.urls')),
#     url(r'^$', serve,kwargs={'path': 'index.html'}),    
#     url(r'^(?!/?statics/)(?!/?media/)(?P<path>.*\..*)$',
#     RedirectView.as_view(url='/statics/%(path)s', permanent=False)),

# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+[url(r'^.*', serve,kwargs={'path': 'index.html'})]
