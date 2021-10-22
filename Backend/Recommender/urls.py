from django.urls import path
from .database_populator import *
from . import views


urlpatterns = [
    path('get_user_posts/', views.get_user_posts, name='get_user_posts'),
    path('add_post/', views.add_post, name='add_post'),
    path('delete_post/', views.delete_post, name='delete_post'),
    path('get_user_friends/', views.get_user_friends, name='get_user_friends'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('delete_friend/', views.delete_friend, name='delete_friend'),
    path('get_recommendations/', views.get_recommendations, name='get_recommendations'),
]

