from django.urls import path
from . import views

app_name = "secretarias"

urlpatterns = [
    path("", views.lista_secretarias, name="lista_secretarias"),
    path("ayudas/", views.lista_ayudas, name="lista_ayudas"),
    path("mis-ayudas/", views.mis_ayudas, name="mis_ayudas"),
    path("ayudas/crear/", views.crear_ayuda, name="crear_ayuda"),
    path("ayudas/<int:ayuda_id>/editar/", views.editar_ayuda, name="editar_ayuda"),
    path("ayudas/<int:ayuda_id>/toggle/", views.toggle_activa_ayuda, name="toggle_ayuda"),
    path("<int:secretaria_id>/ayudas/", views.ayudas_por_secretaria, name="ayudas_por_secretaria"),
]