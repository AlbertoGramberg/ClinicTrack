from django import forms
from .models import Session
from django import forms
from .models import Paciente, Consulta
class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'description', 'date']


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'dni', 'edad', 'obra_social']

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'motivo_de_consulta', 'antecedentes', 'dx_actual', 'laboratorios', 'estudios_realizados', 'tratamiento', 'comentarios']
