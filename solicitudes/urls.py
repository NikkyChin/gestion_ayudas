from django.urls import path
from . import views

app_name = "solicitudes"

urlpatterns = [
    path("entregar/", views.entregar_ayuda, name="entregar_ayuda"),
]