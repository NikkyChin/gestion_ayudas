from django.urls import path
from . import views

app_name = "secretarias"

urlpatterns = [
    path("", views.lista_secretarias, name="lista_secretarias"),
    path("ayudas/", views.lista_ayudas, name="lista_ayudas"),
    path("<int:secretaria_id>/ayudas/", views.ayudas_por_secretaria, name="ayudas_por_secretaria"),
]