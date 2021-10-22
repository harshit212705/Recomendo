from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import CustomUser, Posts, Friendship
from django.db.models import Q
from datetime import datetime
import pytz
from django.db import connection
import pickle
from sklearn.svm import SVC,LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
import urllib.request
import json
import urllib
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import operator
from .personality_predictor import clean_post, predict_personality



@api_view(['GET'])
def get_user_posts(request):

    """API to get user posts data"""

    context = {
        'username': '',
        'personality': '',
        'data': [],
        'error': '',
    }
    
    if request.GET:
        user_id = request.GET.get('user_id', None)
        user_ref = CustomUser.objects.filter(pk=user_id).first()

        if user_ref:
            context['username'] = user_ref.username
            context['personality'] = user_ref.get_predicted_personality_display()
            posts = []

            all_posts_details = Posts.objects.filter(user=user_ref).order_by('timestamp')

            for post in all_posts_details:
                posts.append({
                    'post_id': post.pk, 'post': post.post, 'timestamp': post.timestamp
                })

            context['data'] = posts
        else:
            context['error'] = 'User does not exist'    
    else:
        context['error'] = 'Post request not allowed or query parameter not provided'

    return JsonResponse(context)



def update_user_personality(user_ref):
    cursor = connection.cursor()
    query_str = """SELECT user_id, cleaned_post FROM (SELECT user_id, cleaned_post, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY timestamp DESC) AS row_number 
                    FROM Recommender_posts WHERE user_id="""+ str(user_ref.pk) +""") AS t WHERE t.row_number <= 50;"""
    cursor.execute(query_str)
    data = cursor.fetchall()

    user_posts = ''
    for obj in data:
        user_posts = obj[1] + ' ' + user_posts

    personality_type = predict_personality(user_posts)
    user_ref.predicted_personality = personality_type + 1
    user_ref.save()



@api_view(['GET'])
def add_post(request):

    """API to add new post"""

    context = {
        'post_id': '',
        'error': '',
    }
    
    if request.GET:
        user_id = request.GET.get('user_id', None)
        post = request.GET.get('post', None)

        user_ref = CustomUser.objects.filter(pk=user_id).first()

        if user_ref:
            cleaned_post = clean_post(post)
            new_post = Posts.objects.create(
                user=user_ref,
                post=post,
                cleaned_post=cleaned_post,
                timestamp=datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            new_post.save()
            context['post_id'] = new_post.pk
            update_user_personality(user_ref)
        else:
            context['error'] = 'User does not exist'    
    else:
        context['error'] = 'Post request not allowed or query parameter not provided'

    return JsonResponse(context)



@api_view(['GET'])
def delete_post(request):

    """API to delete a post"""

    context = {
        'error': '',
    }
    
    if request.GET:
        user_id = request.GET.get('user_id', None)
        post_id = request.GET.get('post_id', None)

        user_ref = CustomUser.objects.filter(pk=user_id).first()

        if user_ref:
            post_details = Posts.objects.filter(pk=post_id, user=user_ref).first()

            if post_details:
                post_details.delete()
                update_user_personality(user_ref)
            else:
                context['error'] = 'Either post does not exist or it does not belong to this user'
        else:
            context['error'] = 'User does not exist'    
    else:
        context['error'] = 'Post request not allowed or query parameter not provided'

    return JsonResponse(context)




@api_view(['GET'])
def get_user_friends(request):

    """API to get user friends"""

    context = {
        'data': [],
        'error': '',
    }
    
    if request.GET:
        user_id = request.GET.get('user_id', None)
        user_id = int(user_id)
        user_ref = CustomUser.objects.filter(pk=user_id).first()

        if user_ref:
            friends = []
            friendships = Friendship.objects.filter(Q(user=user_ref) | Q(friend=user_ref))

            for friendship in friendships:
                if user_id == friendship.user.pk:
                    friend_id = friendship.friend.pk
                else:
                    friend_id = friendship.user.id
                friends.append(friend_id)

            friends.sort()
            context['data'] = friends
        else:
            context['error'] = 'User does not exist'    
    else:
        context['error'] = 'Post request not allowed or query parameter not provided'

    return JsonResponse(context)



@api_view(['GET'])
def add_friend(request):

    """API to add new friend"""

    context = {
        'error': '',
    }
    
    if request.GET:
        user_id = request.GET.get('user_id', None)
        friend_id = request.GET.get('friend_id', None)

        user_ref = CustomUser.objects.filter(pk=user_id).first()

        if user_ref:
            user_id = int(user_id)
            friend_ref = CustomUser.objects.filter(pk=friend_id).first()

            if friend_ref:
                friend_id = int(friend_id)

                if user_id != friend_id:
                    already_friends = Friendship.objects.filter(user__pk=min(user_id, friend_id), friend__pk=max(user_id, friend_id)).first()

                    if not already_friends:
                        user1 = user_ref if min(user_id, friend_id) == user_id else friend_ref
                        user2 = user_ref if max(user_id, friend_id) == user_id else friend_ref
                        new_friendship = Friendship.objects.create(
                            user=user1,
                            friend=user2,
                        )
                        new_friendship.save()
                    else:
                        context['error'] = 'They are already friends'
                else:
                    context['error'] = 'One can not be a friend of himself'
            else:
                context['error'] = 'Friend does not exist'
        else:
            context['error'] = 'User does not exist'    
    else:
        context['error'] = 'Post request not allowed or query parameter not provided'

    return JsonResponse(context)



@api_view(['GET'])
def delete_friend(request):

    """API to delete friend"""

    context = {
        'error': '',
    }
    
    if request.GET:
        user_id = request.GET.get('user_id', None)
        friend_id = request.GET.get('friend_id', None)

        user_ref = CustomUser.objects.filter(pk=user_id).first()

        if user_ref:
            user_id = int(user_id)
            friend_ref = CustomUser.objects.filter(pk=friend_id).first()

            if friend_ref:
                friend_id = int(friend_id)

                if user_id != friend_id:
                    already_friends = Friendship.objects.filter(user__pk=min(user_id, friend_id), friend__pk=max(user_id, friend_id)).first()

                    if already_friends:
                        already_friends.delete()
                    else:
                        context['error'] = 'There is no pre-existing friendship between the two'
                else:
                    context['error'] = 'One can not be a friend of himself'
            else:
                context['error'] = 'Friend does not exist'
        else:
            context['error'] = 'User does not exist'    
    else:
        context['error'] = 'Post request not allowed or query parameter not provided'

    return JsonResponse(context)



def get_personality_match_percent(user_personality, recommendation_personality):
    percent = 0.0
    if user_personality[0] == recommendation_personality[0]:
        percent += 0.25
    if user_personality[1] == recommendation_personality[1]:
        percent += 0.25
    if user_personality[2] == recommendation_personality[2]:
        percent += 0.25
    if user_personality[3] == recommendation_personality[3]:
        percent += 0.25
    
    return percent



def find_recommendations(user_ref):
    friends = Friendship.objects.filter(Q(user=user_ref) | Q(friend=user_ref))
    
    friends_list = []
    for friend in friends:
        if user_ref.pk == friend.user.pk:
            friend_id = friend.friend.pk
        else:
            friend_id = friend.user.id
        friends_list.append(friend_id)
    
    friend_of_friends = Friendship.objects.filter(Q(user__in=friends_list) | Q(friend__in=friends_list)).exclude(Q(user=user_ref) | Q(friend=user_ref))
    
    recommendations = {}
    for mf in friend_of_friends:
        first = mf.user.pk
        second = mf.friend.pk

        if first in friends_list:
            if second in recommendations.keys():
                recommendations[second] += 1
            else:
                recommendations.update({second: 1})
        else:
            if first in recommendations.keys():
                recommendations[first] += 1
            else:
                recommendations.update({first: 1})

    recommendations_personality = CustomUser.objects.filter(pk__in=recommendations.keys())
    user_personality_mapping = {}
    for person in recommendations_personality:
        user_personality_mapping[person.pk] = person.get_predicted_personality_display()

    scoring = {}

    for key in recommendations.keys():
        scoring[key] = recommendations[key]*0.5 + get_personality_match_percent(user_ref.get_predicted_personality_display(), user_personality_mapping[key])

    scoring = dict( sorted(scoring.items(), key=operator.itemgetter(1),reverse=True))

    max_value = max(scoring.values(), default=1)
    scoring = {k: v / max_value for k, v in scoring.items()}

    recommendation_list = [{key: val} for key, val in scoring.items() if val >= 0.5]

    return recommendation_list



@api_view(['GET'])
def get_recommendations(request):

    """API to get user recommendations"""

    context = {
        'data': [],
        'error': '',
    }
    
    if request.GET:
        user_id = request.GET.get('user_id', None)
        user_ref = CustomUser.objects.filter(pk=user_id).first()

        if user_ref:
            recommendations = find_recommendations(user_ref)
            context['data'] = recommendations
        else:
            context['error'] = 'User does not exist'    
    else:
        context['error'] = 'Post request not allowed or query parameter not provided'

    return JsonResponse(context)