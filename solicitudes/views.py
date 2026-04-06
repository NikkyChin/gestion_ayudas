from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from personas.models import Persona, Conviviente
from secretarias.models import Secretaria, Ayuda
from .models import EntregaAyudaConviviente
from .forms import EntregaAyudaForm
from django.db.models import Q

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