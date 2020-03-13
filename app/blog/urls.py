from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('posts/', post_list, name='post'),
]