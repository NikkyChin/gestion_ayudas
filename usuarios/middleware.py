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
            grupo = request.user.groups.first()
            secretaria = None

            if grupo:
                secretaria = Secretaria.objects.filter(
                    nombre=grupo.name,
                    activa=True
                ).first()

            if secretaria:
                request.tiene_secretaria = True

            if not any(request.path.startswith(ruta) for ruta in rutas_permitidas):
                if not secretaria:
                    return redirect("usuarios:sin_permiso")

        response = self.get_response(request)
        return response