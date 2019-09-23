from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Usuario
from .serializers import UsuarioSerializer
from django.http import JsonResponse
import tensorflow as tf
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    return JsonResponse({'tfver': tf.__version__})

def another(request):
    return JsonResponse({'another':'response'})

def get_token(request):
    from rest_framework.authtoken.models import Token
    user = User.objects.all()[0]
    token, created = Token.objects.get_or_create(user=user)
    return JsonResponse({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })

class ListUsuarioView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class CustomAuthToken(ObtainAuthToken):
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })