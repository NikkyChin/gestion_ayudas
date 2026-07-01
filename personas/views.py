from django.shortcuts import render, get_object_or_404, redirect
from .models import Persona, Conviviente
from .forms import PersonaForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Persona
from secretarias.models import Secretaria

@login_required
def lista_personas(request):

    q = request.GET.get("q")
    orden = request.GET.get("orden")
    barrio = request.GET.get("barrio")
    encuesta = request.GET.get("encuesta")

    personas = Persona.objects.all()

    # BUSCADOR
    if q:
        personas = personas.filter(
            Q(nombre__icontains=q) |
            Q(apellido__icontains=q) |
            Q(dni__icontains=q)
        )

    # FILTRO POR BARRIO
    if barrio:
        personas = personas.filter(
            barrio__icontains=barrio
        )

    # FILTRO POR ENCUESTA SOCIAL PENDIENTE
    if encuesta == "pendiente":
        personas = personas.filter(
            encuesta_social_pendiente=True
        )

    elif encuesta == "realizada":
        personas = personas.filter(
            encuesta_social_pendiente=False
        )

    # ORDENAMIENTO
    if orden == "az":
        personas = personas.order_by("apellido")

    elif orden == "za":
        personas = personas.order_by("-apellido")

    elif orden == "dni_asc":
        personas = personas.order_by("dni")

    elif orden == "dni_desc":
        personas = personas.order_by("-dni")

    else:
        personas = personas.order_by("apellido")

    paginator = Paginator(personas, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "personas/lista_personas.html", {
        "personas": page_obj,
        "page_obj": page_obj,
        "q": q,
        "orden": orden,
        "barrio": barrio,
        "encuesta": encuesta,
    })

from django.core.paginator import Paginator

@login_required
def detalle_persona(request, persona_id):

    persona = get_object_or_404(
        Persona,
        id=persona_id
    )

    entregas = persona.entregas.all().order_by("-fecha")

    paginator = Paginator(
        entregas,
        10  # ayudas por página
    )

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "personas/detalle_persona.html",
        {
            "persona": persona,
            "page_obj": page_obj,
        }
    )

@login_required
def crear_persona(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)

        if form.is_valid():

            persona = form.save(commit=False)
            persona.creado_por = request.user
            persona.save()

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

            persona = form.save(commit=False)
            persona.modificado_por = request.user
            persona.save()

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

@login_required
def imprimir_persona(request, persona_id):

    persona = get_object_or_404(Persona, id=persona_id)

    grupo = request.user.groups.first()

    secretaria = None

    if grupo:
        secretaria = Secretaria.objects.filter(
            nombre=grupo.name,
            activa=True
        ).first()

    return render(request, "personas/imprimir_persona.html", {
        "persona": persona,
        "secretaria": secretaria,
    })

@login_required
def imprimir_lista(request):

    q = request.GET.get("q")
    orden = request.GET.get("orden")
    barrio = request.GET.get("barrio")
    encuesta = request.GET.get("encuesta")

    personas = Persona.objects.all()

    grupo = request.user.groups.first()

    secretaria = None

    if grupo:
        secretaria = Secretaria.objects.filter(
            nombre=grupo.name,
            activa=True
        ).first()

    # BUSCADOR
    if q:
        personas = personas.filter(
            Q(nombre__icontains=q) |
            Q(apellido__icontains=q) |
            Q(dni__icontains=q)
        )

    # FILTRO BARRIO
    if barrio:
        personas = personas.filter(
            barrio=barrio
        )
    # FILTRO ENCUESTA
    if encuesta == "pendiente":
        personas = personas.filter(
            encuesta_social_pendiente=True
        )

    elif encuesta == "realizada":
        personas = personas.filter(
            encuesta_social_pendiente=False
        )

    # ORDENAMIENTO
    if orden == "az":
        personas = personas.order_by("apellido")

    elif orden == "za":
        personas = personas.order_by("-apellido")

    elif orden == "dni_asc":
        personas = personas.order_by("dni")

    elif orden == "dni_desc":
        personas = personas.order_by("-dni")

    else:
        personas = personas.order_by("apellido")

    return render(
        request,
        "personas/imprimir_lista.html",
        {
            "personas": personas,
            "q": q,
            "barrio": barrio,
            "orden": orden,
            "encuesta": encuesta,
            "secretaria": secretaria,
        }
    )