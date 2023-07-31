from django.contrib import admin

# Register your models here.
from .models import Post
from .models import UserReg

admin.site.register(UserReg)
admin.site.register(Post)

