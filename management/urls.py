from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.management_main, name='management_main'),
    path('users/', views.management_user, name='management_user'),
    path('users/add/', views.user_form, name='user_form'),
    path('users/<int:user_id>/edit/', views.user_form, name='edit_user_profile'),
    path('tutorials/', views.management_tutorial, name='management_tutorial'),
    path('tutorials/add/', views.topic_form, name='topic_form'),
    path('tutorials/<int:category_id>/edit/', views.topic_form, name='edit_topic'),
    path('tutorials/<int:category_id>/words/', views.management_word, name='management_word'),
    path('tutorials/<int:category_id>/words/add/', views.word_form, name='add_word_to_category'),
    path('tutorials/word/<int:tutorial_id>/edit/', views.word_form, name='edit_word'),
    path('users/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
    path('tutorials/<int:tutorial_id>/delete/', views.delete_tutorial, name='delete_tutorial'),
    path('categories/', views.management_category, name='management_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
] 