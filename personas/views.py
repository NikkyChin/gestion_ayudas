from django.shortcuts import render, get_object_or_404, redirect
from .models import Persona, Conviviente
from .forms import PersonaForm


def lista_personas(request):
    personas = Persona.objects.all()
    return render(request, "personas/lista_personas.html", {
        "personas": personas
    })


def detalle_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    return render(request, "personas/detalle_persona.html", {
        "persona": persona
    })


def crear_persona(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)

        if form.is_valid():
            persona = form.save()

            # procesar convivientes
            convivientes = request.POST.getlist("convivientes")

            # alternativa: recorrer POST manualmente
            for key, value in request.POST.items():
                if key.startswith("convivientes"):
                    pass  # no lo usamos así

            # forma correcta
            index = 0
            while True:
                nombre = request.POST.get(f"convivientes[{index}][nombre]")
                apellido = request.POST.get(f"convivientes[{index}][apellido]")

                if not nombre:
                    break

                Conviviente.objects.create(
                    persona=persona,
                    nombre=nombre,
                    apellido=apellido,
                    dni=request.POST.get(f"convivientes[{index}][dni]"),
                    parentesco=request.POST.get(f"convivientes[{index}][parentesco]")
                )

                index += 1

            return redirect("personas:detalle_persona", persona_id=persona.id)

    else:
        form = PersonaForm()

    return render(request, "personas/form_persona.html", {
        "form": form
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Persona, Conviviente
from .forms import PersonaForm


def lista_personas(request):
    personas = Persona.objects.all()
    return render(request, "personas/lista_personas.html", {
        "personas": personas
    })


def detalle_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    return render(request, "personas/detalle_persona.html", {
        "persona": persona
    })


def crear_persona(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)

        if form.is_valid():
            persona = form.save()

            # convivientes
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
        form = PersonaForm()

    return render(request, "personas/form_persona.html", {
        "form": form,
        "modo_edicion": False
    })


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