from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("usuarios.urls")),
    path("admin/", admin.site.urls),
    path("personas/", include("personas.urls")),
    path("secretarias/", include("secretarias.urls")),
]