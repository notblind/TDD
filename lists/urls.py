from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('lists/el/', view_list, name='view_list'),
]
