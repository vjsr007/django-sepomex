from ..model.user import User
from ..serializer.user import UserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class get_delete_update_user(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_queryset(self, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return user

    # Get a user
    def get(self, request, pk):

        user = self.get_queryset(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a user
    def put(self, request, pk):
        
        user = self.get_queryset(pk)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a user
    def delete(self, request, pk):

        user = self.get_queryset(pk)

        user.delete()
        content = {
            'status': 'NO CONTENT'
        }
        return Response(content, status=status.HTTP_204_NO_CONTENT)

class get_post_user(ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
       users = User.objects.all()
       return users

    # Get all users
    @authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])    
    def get(self, request):
        user = self.get_queryset()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)

    # Create a new user
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(pass_field=request.data['password'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   