from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer

class ListUsuarioView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer