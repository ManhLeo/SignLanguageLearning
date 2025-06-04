from django.urls import path
from . import views

app_name = 'recognition'

urlpatterns = [
    path('', views.recognition_home, name='home'),
    path('practice/', views.practice_recognition, name='practice'),
    path('result/', views.recognition_result, name='result'),
] 