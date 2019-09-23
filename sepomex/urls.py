from django.urls import path
from .views import ListUsuarioView, CustomAuthToken
from rest_framework.authtoken import views
from . import views

urlpatterns = [
    path('', views.index, name='list'),
    path('usuario/', ListUsuarioView.as_view(), name="usuario-all"),
    path('index/', views.index, name='index'),
    path('gettoken/', views.get_token, name='get_token'),
    path('another/', views.another, name='another'),
    path('api-token-auth/', CustomAuthToken.as_view())
]