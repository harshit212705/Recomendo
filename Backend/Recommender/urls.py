from django.urls import path
from . import views


urlpatterns = [
    path('posts/', views.get_posts, name='get_posts'),
    path('userinfo/', views.get_userinfo, name='get_userinfo'),
    path('interesttags/', views.get_interest_tags, name='get_interest_tags'),
    path('friendsandrecommendation/', views.get_friends_and_recommendations, name='get_friends_and_recommendations'),
    path('addfriend/', views.add_new_friend, name='add_new_friend'),
    path('removefriend/', views.remove_friend, name='remove_friend'),
    path('addnewpost/', views.add_new_post, name='add_new_post'),
    path('deletepost/', views.remove_post, name='remove_post'),
]

