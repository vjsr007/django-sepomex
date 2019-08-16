from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer
from django.http import JsonResponse

def index(request):
    return JsonResponse({'foo':'bar'})

def another(request):
    return JsonResponse({'another':'response'})    

class ListUsuarioView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer