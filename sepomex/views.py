from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer
from django.http import JsonResponse
from tensorflow import keras
import tensorflow as tf

def index(request):
    return JsonResponse({'tfver': tf.__version__})

def another(request):
    return JsonResponse({'another':'response'})

class ListUsuarioView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
