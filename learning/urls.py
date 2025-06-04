from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('progress/', views.progress, name='progress'),
    path('progress/data/', views.progress_data, name='progress_data'),
    path('assessment/<int:assessment_id>/', views.take_assessment, name='take_assessment'),
    path('assessment/<int:assessment_id>/submit/', views.submit_assessment, name='submit_assessment'),
] 