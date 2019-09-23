from django.urls import path
from .views import ListUsuarioView
from . import views

urlpatterns = [
    path('', views.index, name='list'),
    path('usuario/', ListUsuarioView.as_view(), name="usuario-all"),
    path('index/', views.index, name='index'),
    path('another/', views.another, name='another')
]