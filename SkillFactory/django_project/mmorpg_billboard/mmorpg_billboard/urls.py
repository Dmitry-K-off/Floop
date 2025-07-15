"""
URL configuration for mmorpg_billboard project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

from forum import views

# The `urlpatterns` list routes URLs to views.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum.urls')),
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
