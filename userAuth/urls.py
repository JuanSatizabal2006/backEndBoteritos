from django.urls import path
from .views import Login, ValidarToken

urlpatterns = [
    path('login/', Login, name='login'),
    path('token/', ValidarToken, name='token')
]