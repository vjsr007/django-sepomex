from django.urls import path
from .views import ListUsuarioView
from . import views

urlpatterns = [
    path('', ClassificationListview.as_view(), name='list'),
    path('create/', ClassificationCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ClassificationUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ClassificationDeleteView.as_view(), name='delete'),
    path('usuario/', ListUsuarioView.as_view(), name="usuario-all"),
    path('index/', views.index, name='index'),
    path('another/', views.another, name='another')
]