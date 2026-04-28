import os
import django
import random
from faker import Faker

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from personas.models import Persona, Conviviente

fake = Faker(['es_AR'])

def cargar_datos(n=100):
    print(f"--- Iniciando carga de {n} registros realistas ---")
    
    # Datos locales para mayor realismo en Chubut
    barrios_rawson = [
        'Centro', 'Playa Unión', 'General Valle', 'Gregorio Mayo', 
        'Luis Vernet', 'Área 16', '3 de Abril', 'Río Chubut'
    ]
    parentescos = ['Hijo/a', 'Cónyuge', 'Padre', 'Madre', 'Nieto/a', 'Hermano/a', 'Sobrino/a']

    for i in range(n):
        # Generar titular
        apellido_familia = fake.last_name()
        
        persona = Persona.objects.create(
            dni=str(fake.unique.random_int(min=10000000, max=50000000)),
            nombre=fake.first_name(),
            apellido=apellido_familia,
            direccion=f"{fake.street_name()} {fake.building_number()}",
            barrio=random.choice(barrios_rawson),
            telefono=fake.phone_number(),
            observaciones="Cargado mediante script de prueba.",
            activa=random.choices([True, False], weights=[90, 10])[0] # 90% activos
        )

        # Generar convivientes (entre 0 y 4 por familia)
        num_convivientes = random.choices([0, 1, 2, 3, 4], weights=[15, 25, 30, 20, 10])[0]

        for _ in range(num_convivientes):
            # 70% de probabilidad de compartir el mismo apellido
            ape_conv = apellido_familia if random.random() < 0.7 else fake.last_name()
            
            Conviviente.objects.create(
                persona=persona,
                nombre=fake.first_name(),
                apellido=ape_conv,
                dni=str(fake.unique.random_int(min=10000000, max=60000000)),
                parentesco=random.choice(parentescos),
                observaciones=""
            )
        
        if (i + 1) % 10 == 0:
            print(f">> {i + 1} familias procesadas...")

    print("--- Proceso finalizado correctamente ---")

if __name__ == '__main__':
    cargar_datos(100)