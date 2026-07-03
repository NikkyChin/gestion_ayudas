from urllib import request

from django.shortcuts import redirect
from secretarias.models import Secretaria


class SecretariaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tiene_secretaria = False

        rutas_permitidas = [
            "/login/",
            "/logout/",
            "/sin-permiso/",
            "/admin/",
            "/static/",
        ]

        if request.user.is_authenticated:

            perfil = getattr(request.user, "perfil", None)

            permitido = perfil and perfil.es_admin_general

            if not permitido:
                grupo = request.user.groups.first()

                if grupo:
                    secretaria = Secretaria.objects.filter(
                        nombre=grupo.name,
                        activa=True
                    ).first()

                    permitido = secretaria is not None

            request.tiene_secretaria = permitido

            if (
                not permitido
                and not any(request.path.startswith(ruta) for ruta in rutas_permitidas)
            ):
                return redirect("usuarios:sin_permiso")
            
        response = self.get_response(request)
        return response