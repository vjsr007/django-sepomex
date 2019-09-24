from django.urls import path
from .view.auth import CustomAuthToken
from .view.home import index
from django.urls import include, path, re_path
from .view.users import get_delete_update_user, get_post_user

# Users
urlpatterns = [
    re_path('user/(?P<pk>[0-9]+)$', # Url to get update or delete a user
        get_delete_update_user.as_view(),
        name='get_delete_update_user'
    ),
    path('user/', # urls list all and create new one
        get_post_user.as_view(),
        name='get_post_user'
    )
]

# Home
urlpatterns += [
    path('', index, name='home'),
    path('index/', index, name='index'),
]

# Token
urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]