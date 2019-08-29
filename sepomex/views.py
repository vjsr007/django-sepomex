from rest_framework import generics
from .models import Usuario
from .models import Classification
from .serializers import UsuarioSerializer
from django.http import JsonResponse

def index(request):
    return JsonResponse({'foo':'bar'})

def another(request):
    return JsonResponse({'another':'response'})

class ListUsuarioView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ClassificationListview(ListView):
    model = Classification
    template_name= 'cnn/classification_list.html'
    context_object_name = 'items'


class ClassificationCreateView(CreateView):
    model = Classification
    fields = ['img']


class ClassificationUpdateView(UpdateView):
    model = Classification
    fields = ['img']


class ClassificationDeleteView(DeleteView):
    model = Classification
    success_url = '/' 