from django.shortcuts import render, get_object_or_404, redirect
from .models import Persona, Conviviente
from .forms import PersonaForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def lista_personas(request):
    q = request.GET.get("q")

    if q:
        personas = Persona.objects.filter(
            Q(nombre__icontains=q) |
            Q(apellido__icontains=q) |
            Q(dni__icontains=q)
        )
    else:
        personas = Persona.objects.all()

    return render(request, "personas/lista_personas.html", {
        "personas": personas,
        "q": q
    })

@login_required
def detalle_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    return render(request, "personas/detalle_persona.html", {
        "persona": persona
    })


@login_required
def crear_persona(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)

        if form.is_valid():
            persona = form.save()
            nombres = request.POST.getlist("conviviente_nombre")
            apellidos = request.POST.getlist("conviviente_apellido")
            dnis = request.POST.getlist("conviviente_dni")
            parentescos = request.POST.getlist("conviviente_parentesco")

            for nombre, apellido, dni, parentesco in zip(nombres, apellidos, dnis, parentescos):
                # Solo guardamos si al menos el nombre tiene contenido
                if nombre.strip(): 
                    Conviviente.objects.create(
                        persona=persona,
                        nombre=nombre,
                        apellido=apellido,
                        dni=dni,
                        parentesco=parentesco
                    )
            # -----------------------

            return redirect("personas:detalle_persona", persona_id=persona.id)
    else:
        form = PersonaForm()

    return render(request, "personas/form_persona.html", {"form": form})


@login_required
def editar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)

    if request.method == "POST":
        form = PersonaForm(request.POST, instance=persona)

        if form.is_valid():
            persona = form.save()

            # borrar convivientes anteriores
            persona.convivientes.all().delete()

            # recrear convivientes
            nombres = request.POST.getlist("conviviente_nombre")
            apellidos = request.POST.getlist("conviviente_apellido")
            dnis = request.POST.getlist("conviviente_dni")
            parentescos = request.POST.getlist("conviviente_parentesco")

            for nombre, apellido, dni, parentesco in zip(nombres, apellidos, dnis, parentescos):
                if nombre or apellido:
                    Conviviente.objects.create(
                        persona=persona,
                        nombre=nombre,
                        apellido=apellido,
                        dni=dni,
                        parentesco=parentesco
                    )

            return redirect("personas:detalle_persona", persona_id=persona.id)

    else:
        form = PersonaForm(instance=persona)

    return render(request, "personas/form_persona.html", {
        "form": form,
        "persona": persona,
        "modo_edicion": True
    })