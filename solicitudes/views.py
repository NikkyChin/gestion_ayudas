from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from personas.models import Persona, Conviviente
from secretarias.models import Secretaria, Ayuda
from .models import EntregaAyuda, EntregaAyudaConviviente
from .forms import EntregaAyudaForm


@login_required
def entregar_ayuda(request):
    persona = None
    conviviente_encontrado = None
    dni = request.GET.get("dni") or request.POST.get("dni")

    grupo = request.user.groups.first()
    secretaria = None
    ayudas = Ayuda.objects.none()

    if grupo:
        secretaria = Secretaria.objects.filter(nombre=grupo.name, activa=True).first()
        if secretaria:
            ayudas = Ayuda.objects.filter(secretaria=secretaria, activa=True)

    if dni:
        persona = Persona.objects.filter(dni=dni).first()

        if not persona:
            conviviente_encontrado = Conviviente.objects.filter(dni=dni).first()
            if conviviente_encontrado:
                persona = conviviente_encontrado.persona

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
        "persona": persona,
        "conviviente_encontrado": conviviente_encontrado,
        "dni": dni,
        "form": form,
        "secretaria": secretaria,
    })