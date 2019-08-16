from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sepomex/', include('sepomex.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('sepomex.urls'))
]