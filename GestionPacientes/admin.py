from django.contrib import admin
from .models import Paciente,Consulta  # Importa el modelo Paciente

admin.site.register(Paciente)  # Registra el modelo en el admin
admin.site.register(Consulta)  # Registra el modelo en el admin