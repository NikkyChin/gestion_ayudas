from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from secretarias.models import Ayuda


@login_required
def inicio(request):

    secretaria = None
    oficina = None
    ayudas = []

    if hasattr(request.user, "perfil"):

        secretaria = request.user.perfil.secretaria
        oficina = request.user.perfil.oficina

        if secretaria:
            ayudas = Ayuda.objects.filter(
                secretaria=secretaria,
                activa=True
            )

    return render(request, "usuarios/inicio.html", {
        "secretaria": secretaria,
        "oficina": oficina,
        "ayudas": ayudas,
    })


def sin_permiso(request):
    return render(request, "usuarios/sin_permiso.html")