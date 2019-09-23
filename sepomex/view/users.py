from rest_framework import generics
from ..model.user import User
from ..serializer.user import UserSerializer

class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer