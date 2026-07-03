from collections import defaultdict
from urllib import request

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from personas.models import Persona, Conviviente
from secretarias.models import Secretaria, Ayuda
from .models import EntregaAyudaConviviente, EntregaAyuda
from .forms import EntregaAyudaForm
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.db.models import Count
from datetime import datetime

@login_required
def entregar_ayuda(request):
    query = request.GET.get("q")
    persona = None
    conviviente_encontrado = None

    personas = []
    convivientes = []

    grupo = request.user.groups.first()
    secretaria = None
    ayudas = Ayuda.objects.none()

    if grupo:
        secretaria = Secretaria.objects.filter(nombre=grupo.name, activa=True).first()
        if secretaria:
            ayudas = Ayuda.objects.filter(secretaria=secretaria, activa=True)

    # 🔍 BUSQUEDA
    if query:
        personas = Persona.objects.filter(
            Q(dni__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query)
        )

        convivientes = Conviviente.objects.filter(
            Q(dni__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query)
        )

    # 🎯 SELECCIONAR PERSONA
    persona_id = request.GET.get("persona_id")
    conviviente_id = request.GET.get("conviviente_id")
    accion = request.GET.get("accion")

    if persona_id:
        persona = Persona.objects.filter(id=persona_id).first()

    elif conviviente_id:
        conviviente = Conviviente.objects.filter(id=conviviente_id).first()

        if conviviente:
            if accion == "grupo":
                persona = conviviente.persona
                conviviente_encontrado = conviviente

            elif accion == "independizar":
                # 🔥 convertir conviviente en persona
                persona = Persona.objects.create(
                    nombre=conviviente.nombre,
                    apellido=conviviente.apellido,
                    dni=conviviente.dni,
                )

                # opcional: eliminar conviviente original
                conviviente.delete()

    # 📦 FORM
    if request.method == "POST" and persona:
        form = EntregaAyudaForm(request.POST)
        form.fields["ayuda"].queryset = ayudas

        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.persona = persona
            entrega.usuario = request.user
            entrega.save()

            for conviviente in persona.convivientes.all():
                EntregaAyudaConviviente.objects.create(
                    entrega=entrega,
                    nombre=conviviente.nombre,
                    apellido=conviviente.apellido,
                    dni=conviviente.dni,
                    parentesco=conviviente.parentesco,
                )

            return redirect("personas:detalle_persona", persona_id=persona.id)
    else:
        form = EntregaAyudaForm()
        form.fields["ayuda"].queryset = ayudas

    return render(request, "solicitudes/entregar_ayuda.html", {
        "query": query,
        "personas": personas,
        "convivientes": convivientes,
        "persona": persona,
        "conviviente_encontrado": conviviente_encontrado,
        "form": form,
        "secretaria": secretaria,
    })

@login_required
def estadisticas_entregas(request):
    
    if not (request.user.perfil.es_admin_general or request.user.perfil.es_admin_area):
        return redirect("usuarios:sin_permiso")

    
    grupo = request.user.groups.first()
    secretaria_id = request.GET.get("secretaria")

    secretarias = Secretaria.objects.filter(
        activa=True
    ).order_by("nombre")

    secretaria = None

    if not request.user.perfil.es_admin_general and grupo:
        secretaria = Secretaria.objects.filter(
            nombre=grupo.name,
            activa=True
        ).first()

    estadisticas = []
    estadisticas_barrios = []
    estadisticas_barrio_ayuda = []

    mes = request.GET.get("mes", "todos")
    anio = request.GET.get("anio", str(datetime.now().year))

    # ==========================
    # CONSULTA DE ENTREGAS
    # ==========================

    if request.user.perfil.es_admin_general:

        entregas = EntregaAyuda.objects.all()

        if secretaria_id:
            entregas = entregas.filter(
                ayuda__secretaria_id=secretaria_id
            )

    elif secretaria:

        entregas = EntregaAyuda.objects.filter(
            ayuda__secretaria=secretaria
        )

    else:

        entregas = EntregaAyuda.objects.none()

    # ==========================
    # FILTROS
    # ==========================

    if mes != "todos":
        entregas = entregas.filter(
            fecha__month=mes
        )

    if anio:
        entregas = entregas.filter(
            fecha__year=anio
        )

    # ==========================
    # ESTADÍSTICAS
    # ==========================

    estadisticas = (
        entregas
        .values("ayuda__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    estadisticas_barrios = (
        entregas
        .exclude(persona__barrio="")
        .values("persona__barrio")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    estadisticas_barrio_ayuda = (
        entregas
        .exclude(persona__barrio="")
        .values(
            "persona__barrio",
            "ayuda__nombre"
        )
        .annotate(total=Count("id"))
        .order_by(
            "persona__barrio",
            "-total"
        )
    )

    ayudas_por_barrio = defaultdict(list)

    for item in estadisticas_barrio_ayuda:
        ayudas_por_barrio[item["persona__barrio"]].append({
            "ayuda": item["ayuda__nombre"],
            "total": item["total"],
        })

    total_general = sum(
        item["total"]
        for item in estadisticas
    )

    return render(request, "solicitudes/estadisticas.html", {
        "estadisticas": estadisticas,
        "estadisticas_barrios": estadisticas_barrios,
        "estadisticas_barrio_ayuda": estadisticas_barrio_ayuda,
        "mes": mes,
        "anio": anio,
        "secretaria": secretaria,
        "total_general": total_general,
        "ayudas_por_barrio": dict(ayudas_por_barrio),
        "secretarias": secretarias,
        "secretaria_id": secretaria_id,
    })

@login_required
def imprimir_estadisticas(request):

    if not (request.user.perfil.es_admin_general or request.user.perfil.es_admin_area):
        return redirect("usuarios:sin_permiso")

    grupo = request.user.groups.first()

    secretaria_id = request.GET.get("secretaria")

    secretaria = None

    if not request.user.perfil.es_admin_general and grupo:
        secretaria = Secretaria.objects.filter(
            nombre=grupo.name,
            activa=True
        ).first()

    estadisticas = []
    estadisticas_barrios = []
    estadisticas_barrio_ayuda = []

    mes = request.GET.get("mes", "todos")
    anio = request.GET.get("anio", str(datetime.now().year))

    # ==========================
    # CONSULTA DE ENTREGAS
    # ==========================

    if request.user.perfil.es_admin_general:

        entregas = EntregaAyuda.objects.all()

        if secretaria_id:
            entregas = entregas.filter(
                ayuda__secretaria_id=secretaria_id
            )

    elif secretaria:

        entregas = EntregaAyuda.objects.filter(
            ayuda__secretaria=secretaria
        )

    else:

        entregas = EntregaAyuda.objects.none()

    # ==========================
    # FILTROS
    # ==========================

    if mes != "todos":
        entregas = entregas.filter(
            fecha__month=mes
        )

    if anio:
        entregas = entregas.filter(
            fecha__year=anio
        )

    # ==========================
    # ESTADÍSTICAS
    # ==========================

    estadisticas = (
        entregas
        .values("ayuda__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    estadisticas_barrios = (
        entregas
        .exclude(persona__barrio="")
        .values("persona__barrio")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    estadisticas_barrio_ayuda = (
        entregas
        .exclude(persona__barrio="")
        .values(
            "persona__barrio",
            "ayuda__nombre"
        )
        .annotate(total=Count("id"))
        .order_by(
            "persona__barrio",
            "-total"
        )
    )

    ayudas_por_barrio = defaultdict(list)

    for item in estadisticas_barrio_ayuda:
        ayudas_por_barrio[item["persona__barrio"]].append({
            "ayuda": item["ayuda__nombre"],
            "total": item["total"],
        })

    total_general = sum(item["total"] for item in estadisticas)

    meses = {
        "1": "Enero",
        "2": "Febrero",
        "3": "Marzo",
        "4": "Abril",
        "5": "Mayo",
        "6": "Junio",
        "7": "Julio",
        "8": "Agosto",
        "9": "Septiembre",
        "10": "Octubre",
        "11": "Noviembre",
        "12": "Diciembre",
    }

    nombre_mes = meses.get(str(mes), "Todos")

    nombre_secretaria = "Todas las Secretarías"

    if request.user.perfil.es_admin_general:

        if secretaria_id:
            secretaria_filtrada = Secretaria.objects.filter(
                id=secretaria_id,
                activa=True
            ).first()

            if secretaria_filtrada:
                nombre_secretaria = secretaria_filtrada.nombre

    else:

        nombre_secretaria = secretaria.nombre if secretaria else ""

    return render(request, "solicitudes/imprimir_estadisticas.html", {
        "estadisticas": estadisticas,
        "secretaria": secretaria,
        "mes": nombre_mes,
        "anio": anio,
        "total_general": total_general,
        "estadisticas_barrios": estadisticas_barrios,
        "estadisticas_barrio_ayuda": estadisticas_barrio_ayuda,
        "ayudas_por_barrio": dict(ayudas_por_barrio),
        "secretaria_id": secretaria_id,
        "nombre_secretaria": nombre_secretaria,
    })