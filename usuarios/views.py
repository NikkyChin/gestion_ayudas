from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from secretarias.models import Secretaria, Ayuda


@login_required
def inicio(request):
    grupo = request.user.groups.first()
    secretaria = None
    ayudas = []

    if grupo:
        secretaria = Secretaria.objects.filter(nombre=grupo.name, activa=True).first()
        if secretaria:
            ayudas = Ayuda.objects.filter(secretaria=secretaria, activa=True)

    return render(request, "usuarios/inicio.html", {
        "secretaria": secretaria,
        "ayudas": ayudas,
    })