from django.urls import path
from . import views

app_name = "personas"

urlpatterns = [
    path("", views.lista_personas, name="lista_personas"),
    path("crear/", views.crear_persona, name="crear_persona"),
    path("<int:persona_id>/", views.detalle_persona, name="detalle_persona"),
]