from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    title = models.CharField(max_length=100)  # Título de la sesión
    description = models.TextField()  # Descripción de la sesión
    date = models.DateTimeField()  # Fecha y hora de la sesión

    def __str__(self):
        return self.title


class Paciente(models.Model):
    # Relación con el usuario que crea el paciente
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pacientes')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=100, unique=True)  # DNI único por paciente
    edad = models.PositiveIntegerField()
    obra_social = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    fecha = models.DateTimeField(auto_now_add=True)  # Se guarda la fecha automáticamente
    motivo_de_consulta = models.CharField(max_length=200, blank=True, null=True)
    antecedentes = models.TextField(blank=True, null=True)
    dx_actual = models.CharField(max_length=200, blank=True, null=True)
    laboratorios = models.TextField(blank=True, null=True)
    estudios_realizados = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    analisis_ai = models.TextField(blank=True, null=True)  # Nuevo campo para el análisis AI

    def __str__(self):
        return f"Consulta de {self.paciente} - {self.fecha.strftime('%d/%m/%Y')}"