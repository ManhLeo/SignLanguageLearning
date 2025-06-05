from django.urls import path
from . import views

app_name = 'tutorials'

urlpatterns = [
    path('', views.tutorial_list, name='tutorial_list'),
    path('<int:tutorial_id>/', views.tutorial_detail, name='tutorial_detail'),
    path('category/<str:category>/', views.tutorials_by_category, name='tutorials_by_category'),
    path('difficulty/<str:difficulty>/', views.tutorials_by_difficulty, name='tutorials_by_difficulty'),
    path('search/', views.tutorial_search, name='tutorial_search'),
    path('topic/', views.topic, name='topic'),
    path('vd_vocabulary/', views.vd_vocabulary, name='vd_vocabulary'),
]