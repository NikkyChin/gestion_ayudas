from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Secretaria, Ayuda
from .forms import AyudaForm

@login_required
def lista_secretarias(request):
    secretarias = Secretaria.objects.filter(activa=True)
    return render(request, "secretarias/lista_secretarias.html", {
        "secretarias": secretarias
    })

@login_required
def lista_ayudas(request):
    ayudas = Ayuda.objects.filter(activa=True).select_related("secretaria")
    return render(request, "secretarias/lista_ayudas.html", {
        "ayudas": ayudas
    })

@login_required
def ayudas_por_secretaria(request, secretaria_id):
    secretaria = get_object_or_404(Secretaria, id=secretaria_id, activa=True)
    ayudas = secretaria.ayudas.filter(activa=True)

    return render(request, "secretarias/ayudas_por_secretaria.html", {
        "secretaria": secretaria,
        "ayudas": ayudas
    })

@login_required
def mis_ayudas(request):
    grupo = request.user.groups.first()
    secretaria = None
    ayudas = Ayuda.objects.none()

    if grupo:
        secretaria = Secretaria.objects.filter(nombre=grupo.name, activa=True).first()
        if secretaria:
            ayudas = Ayuda.objects.filter(secretaria=secretaria).order_by("nombre")

    return render(request, "secretarias/mis_ayudas.html", {
        "secretaria": secretaria,
        "ayudas": ayudas,
    })


@login_required
def crear_ayuda(request):
    grupo = request.user.groups.first()
    secretaria = None

    if grupo:
        secretaria = Secretaria.objects.filter(nombre=grupo.name, activa=True).first()

    if not secretaria:
        return redirect("secretarias:mis_ayudas")

    if request.method == "POST":
        form = AyudaForm(request.POST)
        if form.is_valid():
            ayuda = form.save(commit=False)
            ayuda.secretaria = secretaria
            ayuda.save()
            return redirect("secretarias:mis_ayudas")
    else:
        form = AyudaForm()

    return render(request, "secretarias/form_ayuda.html", {
        "form": form,
        "titulo": "Crear ayuda",
        "secretaria": secretaria,
    })


@login_required
def editar_ayuda(request, ayuda_id):
    grupo = request.user.groups.first()
    secretaria = None

    if grupo:
        secretaria = Secretaria.objects.filter(nombre=grupo.name, activa=True).first()

    ayuda = get_object_or_404(Ayuda, id=ayuda_id)

    if not secretaria or ayuda.secretaria != secretaria:
        return redirect("secretarias:mis_ayudas")

    if request.method == "POST":
        form = AyudaForm(request.POST, instance=ayuda)
        if form.is_valid():
            ayuda = form.save(commit=False)
            ayuda.secretaria = secretaria
            ayuda.save()
            return redirect("secretarias:mis_ayudas")
    else:
        form = AyudaForm(instance=ayuda)

    return render(request, "secretarias/form_ayuda.html", {
        "form": form,
        "titulo": "Editar ayuda",
        "secretaria": secretaria,
    })


@login_required
def toggle_activa_ayuda(request, ayuda_id):
    grupo = request.user.groups.first()
    secretaria = None

    if grupo:
        secretaria = Secretaria.objects.filter(nombre=grupo.name, activa=True).first()

    ayuda = get_object_or_404(Ayuda, id=ayuda_id)

    if not secretaria or ayuda.secretaria != secretaria:
        return redirect("secretarias:mis_ayudas")

    if request.method == "POST":
        ayuda.activa = not ayuda.activa
        ayuda.save()

    return redirect("secretarias:mis_ayudas")