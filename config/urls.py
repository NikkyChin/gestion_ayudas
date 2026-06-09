from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("usuarios.urls")),
    path("personas/", include("personas.urls")),
    path("secretarias/", include("secretarias.urls")),
    path("solicitudes/", include("solicitudes.urls")),

    path("cambiar-contraseña/",PasswordChangeView.as_view(template_name="usuarios/cambiar_contraseña.html"), name="cambiar_password"),
    path("cambiar-contraseña/exito/",PasswordChangeDoneView.as_view(template_name="usuarios/cambiar_contraseña_exito.html"), name="password_change_done"),
    path("login/", auth_views.LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
