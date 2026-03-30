from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("secretarias/", include("secretarias.urls")),
    path("personas/", include("personas.urls")),
]