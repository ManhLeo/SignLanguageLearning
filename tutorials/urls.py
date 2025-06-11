from django.urls import path
from . import views

app_name = 'tutorials'

urlpatterns = [
    path('', views.tutorial_list, name='tutorial_list'),
    path('<int:tutorial_id>/', views.tutorial_detail, name='tutorial_detail'),
    path('category/<str:category>/', views.tutorials_by_category, name='tutorials_by_category'),
    path('difficulty/<str:difficulty>/', views.tutorials_by_difficulty, name='tutorials_by_difficulty'),
    path('search/', views.tutorial_search, name='tutorial_search'),
    path('topic/<int:topic_id>/vocabulary/', views.vocabulary_detail, name='vocabulary_detail'),
    path('practice/', views.practice_home, name='practice_home'),
    path('practice/<int:topic_id>/', views.practice_detail, name='practice_detail'),
    path('vocabulary/', views.vocabulary, name='vocabulary'),
    path('vocabulary/<int:tutorial_id>/', views.vd_vocabulary, name='vd_vocabulary'),
    path('exam/', views.exam_page, name='exam_page'),
] 