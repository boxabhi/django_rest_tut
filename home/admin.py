from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Department)
admin.site.register(Color)
admin.site.register(Student)
