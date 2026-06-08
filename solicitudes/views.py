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
    grupo = request.user.groups.first()

    secretaria = None
    estadisticas = []

    mes = request.GET.get("mes", "todos")
    anio = request.GET.get("anio", str(datetime.now().year))

    if grupo:
        secretaria = Secretaria.objects.filter(
            nombre=grupo.name,
            activa=True
        ).first()

    entregas = EntregaAyuda.objects.none()

    if secretaria:
        entregas = EntregaAyuda.objects.filter(
            ayuda__secretaria=secretaria
        )

        # 📅 filtro por mes y año
        if mes != "todos":
            entregas = entregas.filter(fecha__month=mes)

        if anio:
            entregas = entregas.filter(fecha__year=anio)

        estadisticas = (
            entregas
            .values("ayuda__nombre")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

    total_general = sum(item["total"] for item in estadisticas)

    return render(request, "solicitudes/estadisticas.html", {
        "estadisticas": estadisticas,
        "mes": mes,
        "anio": anio,
        "secretaria": secretaria,
        "total_general": total_general,
    })

@login_required
def imprimir_estadisticas(request):

    grupo = request.user.groups.first()

    secretaria = None
    estadisticas = []

    mes = request.GET.get("mes", "todos")
    anio = request.GET.get("anio", str(datetime.now().year))

    if grupo:
        secretaria = Secretaria.objects.filter(
            nombre=grupo.name,
            activa=True
        ).first()

    entregas = EntregaAyuda.objects.none()

    if secretaria:

        entregas = EntregaAyuda.objects.filter(
            ayuda__secretaria=secretaria
        )

        # FILTRO MES
        if mes != "todos":
            entregas = entregas.filter(
                fecha__month=mes
            )

        # FILTRO AÑO
        if anio:
            entregas = entregas.filter(
                fecha__year=anio
            )

        estadisticas = (
            entregas
            .values("ayuda__nombre")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

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

    return render(request, "solicitudes/imprimir_estadisticas.html", {
        "estadisticas": estadisticas,
        "secretaria": secretaria,
        "mes": nombre_mes,
        "anio": anio,
        "total_general": total_general,
    })