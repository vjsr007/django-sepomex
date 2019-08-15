from django.urls import path
from .views import ListUsuarioView

urlpatterns = [
    path('usuario/', ListUsuarioView.as_view(), name="usuario-all")
]