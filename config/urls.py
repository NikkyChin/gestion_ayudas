from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("usuarios.urls")),
    path("personas/", include("personas.urls")),
    path("secretarias/", include("secretarias.urls")),
    path("solicitudes/", include("solicitudes.urls")),

    path("login/", auth_views.LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]