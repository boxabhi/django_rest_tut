from django.contrib import admin
from django.urls import path
from .views import *




urlpatterns = [
    path('' , home, ),
    path('<socket_url>' , home),

    path('upload/' , upload),

]

