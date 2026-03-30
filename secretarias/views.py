from django.shortcuts import render, get_object_or_404
from .models import Secretaria, Ayuda


def lista_secretarias(request):
    secretarias = Secretaria.objects.filter(activa=True)
    return render(request, "secretarias/lista_secretarias.html", {
        "secretarias": secretarias
    })


def lista_ayudas(request):
    ayudas = Ayuda.objects.filter(activa=True).select_related("secretaria")
    return render(request, "secretarias/lista_ayudas.html", {
        "ayudas": ayudas
    })


def ayudas_por_secretaria(request, secretaria_id):
    secretaria = get_object_or_404(Secretaria, id=secretaria_id, activa=True)
    ayudas = secretaria.ayudas.filter(activa=True)

    return render(request, "secretarias/ayudas_por_secretaria.html", {
        "secretaria": secretaria,
        "ayudas": ayudas
    })
