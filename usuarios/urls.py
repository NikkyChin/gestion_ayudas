from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("sin-permiso/", views.sin_permiso, name="sin_permiso"),
]