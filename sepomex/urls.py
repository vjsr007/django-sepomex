from django.urls import path
from .view.users import ListUserView
from .view.auth import CustomAuthToken, get_token
from .view.home import index

# Home
urlpatterns = [
    path('', index, name='home'),
    path('index/', index, name='index'),
]

# Users
urlpatterns += [
    path('user/', ListUserView.as_view(), name="user-all"),
]

# Token
urlpatterns += [
    path('gettoken/', get_token , name='get_token'),
    path('api-token-auth/', CustomAuthToken.as_view())
]