from django.urls import path
from . import views

app_name = 'recognition'

urlpatterns = [
    path('', views.recognition_home, name='home'),
] 