from django.urls import path
from . import views

app_name = "solicitudes"

urlpatterns = [
    path("entregar/", views.entregar_ayuda, name="entregar_ayuda"),
    path("estadisticas/", views.estadisticas_entregas, name="estadisticas_entregas"),
    path("estadisticas/imprimir/", views.imprimir_estadisticas, name="imprimir_estadisticas"),
]