from django.contrib import admin

# Register your models here.
from .model.user import User

admin.site.register(User)