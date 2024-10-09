from django.urls import path
from .views import RecuperarContrasena, ActualizarContrasena, CambiarContrasena

urlpatterns = [
    path('recuperar/', RecuperarContrasena),
    path('cambiar/', CambiarContrasena),
    path('actualizar/', ActualizarContrasena)
]