from django.urls import path
from . import views
from .views import subir_paciente, lista_pacientes, lista_usuarios, subir_paciente,modificar_paciente, agregar_consulta, lista_consultas, ver_consulta, generar_analisis_ai, metricas_usuario,mostrar_mapa
urlpatterns = [
    
    path('',views.metricas_usuario),
    path('home/',metricas_usuario, name='home'),
    path('lista_usuarios/', lista_usuarios, name='lista_usuarios'),
    path('subir_paciente/', subir_paciente, name='subir_paciente'),
    path('lista_pacientes/', lista_pacientes,  name='lista_pacientes'),
    path('modificar-paciente/<int:id>/', modificar_paciente, name='modificar_paciente'),
    path('agregar-consulta/<int:id>/', agregar_consulta, name='agregar_consulta'),
    path('lista_consultas/<int:id>/', lista_consultas, name='lista_consultas'),
    path('ver_consulta/<int:id>/', ver_consulta, name='ver_consulta'),
    path('generar_analisis_ai/<int:id>/', generar_analisis_ai, name='generar_analisis_ai'),
    path('mapa/', mostrar_mapa, name='mapa_complemento'),



]