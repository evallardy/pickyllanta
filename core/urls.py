from django.urls import path
from core.api import mensaje_api_view

urlpatterns = [
    path('', mensaje_api_view, name = 'mensajes_api_picky'),
]