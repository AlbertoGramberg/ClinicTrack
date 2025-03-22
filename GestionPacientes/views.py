from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Session, Paciente, Consulta
from .forms import SessionForm,PacienteForm, ConsultaForm  
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView
from django.contrib.auth.models import User  # Modelo User por defecto de Django
from mistralai import Mistral
import os
from django.db.models import Count, Avg
from datetime import datetime
from django.db.models.functions import ExtractMonth
from .mapa_complemento import generar_mapa




# Listar todas las sesiones


def home(request):
    generar_mapa()
    return render(request, 'home.html')

def mostrar_mapa(request):
    return render(request, 'mapa.html')

@login_required
def session_list(request):
    sessions = Session.objects.filter(user=request.user)
    return render(request, 'sesion_Medicos_list.html', {'sessions': sessions})

# Crear una nueva sesión
def session_create(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect('session_list')
    else:
        form = SessionForm()
    return render(request, 'session_form.html', {'form': form})

# Actualizar una sesión existente
def session_update(request, pk):
    session = get_object_or_404(Session, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('session_list')
    else:
        form = SessionForm(instance=session)
    return render(request, 'session_form.html', {'form': form})

# Eliminar una sesión
def session_delete(request, pk):
    session = get_object_or_404(Session, pk=pk, user=request.user)
    if request.method == 'POST':
        session.delete()
        return redirect('session_list')
    return render(request, 'session_confirm_delete.html', {'session': session})


@login_required
def lista_usuarios(request):
    # Obtener todos los usuarios de la base de datos
    usuarios = User.objects.all().values('username', 'email')
    
    # Pasar los usuarios al contexto de la plantilla
    context = {
        'usuarios': usuarios
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'lista_usuarios.html', context)

@login_required
def subir_paciente(request):
    # Verificar si la solicitud es de tipo POST (envío de formulario)
    if request.method == 'POST':
        # Crear una instancia del formulario con los datos enviados
        paciente_form = PacienteForm(request.POST)
        # Validar el formulario
        if paciente_form.is_valid():
            # Guardar los datos del formulario en una instancia del modelo Paciente, pero no en la base de datos todavía
            nuevo_paciente = paciente_form.save(commit=False)
            # Asignar el usuario actual al campo 'usuario' del paciente
            nuevo_paciente.usuario = request.user
            # Guardar el paciente en la base de datos
            nuevo_paciente.save()
            # Redirigir a una vista de éxito o a la misma página
            return redirect('lista_pacientes')  # Cambia 'lista_pacientes' por la vista que desees
    else:
        # Si la solicitud no es POST, mostrar el formulario vacío
        paciente_form = PacienteForm()

    # Renderizar la plantilla con el formulario
    return render(request, 'crear_paciente.html', {
        'paciente_form': paciente_form,
    })
@login_required
def lista_pacientes(request):
    # Obtener todos los pacientes del usuario actual
    pacientes = Paciente.objects.filter(usuario=request.user)
    
    # Renderizar la plantilla con la lista de pacientes
    return render(request, 'lista_pacientes.html', {
        'pacientes': pacientes,
    })
    

def modificar_paciente(request, id):
    # Obtener el paciente por su ID o mostrar un error 404 si no existe
    paciente = get_object_or_404(Paciente, id=id, usuario=request.user)
    
    if request.method == 'POST':
        # Crear una instancia del formulario con los datos enviados y la instancia del paciente
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')  # Redirigir a la lista de pacientes
    else:
        # Mostrar el formulario con los datos actuales del paciente
        form = PacienteForm(instance=paciente)
    
    return render(request, 'modificar_paciente.html', {
        'form': form,
    }) 
def agregar_consulta(request, id):
    # Obtener el paciente por su ID o mostrar un error 404 si no existe
    paciente = get_object_or_404(Paciente, id=id, usuario=request.user)
    
    if request.method == 'POST':
        # Crear una instancia del formulario con los datos enviados
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente  # Asignar el paciente a la consulta
            consulta.save()
            return redirect('lista_pacientes')  # Redirigir a la lista de pacientes
    else:
        # Mostrar el formulario vacío
        form = ConsultaForm()
    
    return render(request, 'agregar_consulta.html', {
        'form': form,
        'paciente': paciente,
    })

def lista_consultas(request, id):
    # Obtener el paciente por su ID o mostrar un error 404 si no existe
    paciente = get_object_or_404(Paciente, id=id, usuario=request.user)
    # Obtener todas las consultas asociadas al paciente
    consultas = Consulta.objects.filter(paciente=paciente)
    
    # Renderizar la plantilla con la lista de consultas
    return render(request, 'lista_consultas.html', {
        'paciente': paciente,
        'consultas': consultas,
    })

def ver_consulta(request, id):
    # Obtener la consulta por su ID o mostrar un error 404 si no existe
    consulta = get_object_or_404(Consulta, id=id, paciente__usuario=request.user)
    
    # Renderizar la plantilla con los detalles de la consulta
    return render(request, 'ver_consulta.html', {
        'consulta': consulta,
    })

def obtener_diagnostico(historia, lab, signos, estudios):
    # Construye el prompt con los datos clínicos
    prompt = f"""
    Basado en los siguientes datos clínicos, sugiere un diagnóstico diferencial con el siguiente formato:

    Diagnóstico Posible: 
    Otras Enfermedades Posibles: 
    Explicación de la fisiopatología:
    Tratamiento:
    Comentario Adicional:
    Bibliografía:

    Historia Clínica: {historia}
    Parámetros de Laboratorio: {lab}
    Signos y Síntomas: {signos}
    Estudios Adicionales: {estudios}
    """

    # Obtén la clave de API desde las variables de entorno
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("La clave de API no está configurada en la variable de entorno 'MISTRAL_API_KEY'.")

    # Inicializa el cliente de Mistral
    client = Mistral(api_key=api_key)

    # Define el modelo y los mensajes
    model = "mistral-large-latest"
    messages = [{"role": "user", "content": prompt}]

    # Realiza la solicitud a la API
    chat_response = client.chat.complete(model=model, messages=messages, max_tokens=500)

    # Devuelve el texto generado por el modelo
    return chat_response.choices[0].message.content.strip()

def generar_analisis_ai(request, id):
    # Obtener la consulta por su ID o mostrar un error 404 si no existe
    consulta = get_object_or_404(Consulta, id=id, paciente__usuario=request.user)

    if request.method == 'POST':
        # Obtener los datos de la consulta
        historia = consulta.antecedentes or ""
        lab = consulta.laboratorios or ""
        signos = consulta.motivo_de_consulta or ""
        estudios = consulta.estudios_realizados or ""

        # Generar el análisis AI
        analisis_ai = obtener_diagnostico(historia, lab, signos, estudios)

        # Guardar el análisis AI en la consulta
        consulta.analisis_ai = analisis_ai
        consulta.save()

        # Redirigir a la página de detalles de la consulta
        return redirect('ver_consulta', id=consulta.id)

    # Si no es una solicitud POST, redirigir a la página de detalles de la consulta
    return redirect('ver_consulta', id=consulta.id)

@login_required
def metricas_usuario(request):
    # Obtener el usuario actual
    usuario = request.user

    # Número de pacientes atendidos
    numero_pacientes = Paciente.objects.filter(usuario=usuario).count()

    # Gráfica de pacientes vs meses del año
    consultas_por_mes = (
        Consulta.objects.filter(paciente__usuario=usuario)
        .annotate(mes=ExtractMonth('fecha'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    # Preparar datos para la gráfica
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    datos_grafica = [0] * 12  # Inicializar con 0 para cada mes
    for consulta in consultas_por_mes:
        datos_grafica[consulta['mes'] - 1] = consulta['total']

    # Edad promedio de los pacientes
    edad_promedio = Paciente.objects.filter(usuario=usuario).aggregate(avg_edad=Avg('edad'))['avg_edad'] or 0

    # Renderizar la plantilla con las métricas
    return render(request, 'metricas_usuario.html', {
        'numero_pacientes': numero_pacientes,
        'datos_grafica': datos_grafica,
        'meses': meses,
        'edad_promedio': round(edad_promedio, 1),  # Redondear a un decimal
    })