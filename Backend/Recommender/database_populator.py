# for shuffling the alphabetically ordered names

'''
with open('../Backend/datasets/names_alphabetically.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

print(lines)

import numpy as np

arr = np.array(lines)
np.random.shuffle(arr)

print(arr)

fp = open("../Backend/datasets/list_of_names.txt","a")
for ele in arr:
    fp.write(ele + '\n')

fp.close()
'''



# for populating users data in CustomUsers model

'''
from .models import CustomUser

import pandas as pd
data = pd.read_csv('../Backend/datasets/profiles_104.csv')

with open('../Backend/datasets/list_of_names.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

personality_no_mapping = {
    'ENFJ': 1, 'ENFP': 2, 'ENTJ': 3, 'ENTP': 4, 'ESFJ': 5, 'ESFP': 6, 'ESTJ': 7, 'ESTP': 8, 
    'INFJ': 9, 'INFP': 10, 'INTJ': 11, 'INTP': 12, 'ISFJ': 13, 'ISFP': 14, 'ISTJ': 15, 'ISTP': 16
}

profiles = []
for i in range(0, len(lines)):
    profiles.append(
        CustomUser(
            username=lines[i],
            personality_type=personality_no_mapping[data.iloc[i].Type],
        )
    )

users = CustomUser.objects.bulk_create(profiles)
'''



# for populating Posts model

'''
def get_youtube_video_title(videoID):
  # print(videoID)

  params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % videoID}
  url = "https://www.youtube.com/oembed"
  query_string = urllib.parse.urlencode(params)
  url = url + "?" + query_string

  try:
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return data['title']
  except:
    return ''


def remove_link_from_post(post):

    post_after_links_removal = post
    urls = []
    url_regex = re.compile('(?:https?|ftp):\/\/[\w\/\-?=%.]+\.[\w\/\-&?=%.]+')
    for match in url_regex.finditer(post):
      # print(match.group())

      url = match.group()
      youtube_link = re.findall('https?:\/\/www.youtube.com\/watch\?', url)
      if len(youtube_link):
        youtube_link = url
        params_list = youtube_link.split('?')[1].split('&')
        video_id = [param[2:] for param in params_list if len(param) > 2 and param[0:2] == 'v=']
        if len(video_id):
          video_title = get_youtube_video_title(video_id[0])
          post_after_links_removal = post_after_links_removal.replace(match.group(), video_title)
      else:
        post_after_links_removal = post_after_links_removal.replace(match.group(), '')

    return post_after_links_removal


def clean_post(post):
    post = remove_link_from_post(post)
    post = post.lower()
    
    # removing other symbols
    post = re.sub('[^a-z]',' ',post)

    # Remove spaces > 1
    post = re.sub(' +', ' ', post)

    # Lemmatizing the words in post
    post = " ".join([lemmatiser.lemmatize(w) for w in post.split(' ') if w not in cachedStopWords])

    return post



import pandas as pd
import re
import urllib.request
import json
import urllib
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from datetime import datetime, timedelta, date
from django.utils import timezone
import pytz
from .models import CustomUser, Posts


nltk.download('wordnet')
nltk.download('stopwords')

lemmatiser = WordNetLemmatizer()

# Cache the stop words for speed 
cachedStopWords = stopwords.words("english")

data = pd.read_csv('../Backend/datasets/profiles_104.csv')
# print(data.iloc[2].Posts)

total_posts = 0
all_posts = []
for i in range(0, len(data.index)):
    posts = data.iloc[i].Posts.split('|||')
    total_posts += len(posts)

    user_ref = CustomUser.objects.filter(pk=i+1).first()

    base_datetime = datetime.now(pytz.timezone('Asia/Kolkata')) - timedelta(days=2)
    print(base_datetime)
    for post in posts:
        cleaned_post = clean_post(post)
        all_posts.append(
            Posts(
                user=user_ref,
                post=post,
                cleaned_post=cleaned_post,
                timestamp=base_datetime
            )
        )
        base_datetime += timedelta(minutes=30)

    print(i)


posts = Posts.objects.bulk_create(all_posts)

print(len(all_posts))
print('done')
'''



# for populating Friendship model

'''
from .models import CustomUser, Friendship

friends_list = [[13, 43, 46, 61, 95],
[30, 31, 33, 68],
[47, 81, 85, 89, 97],
[13, 45, 72, 80],
[25, 58, 77, 83],
[32, 38, 73, 91],
[2, 5, 16, 52, 83],
[7, 35, 59],
[41, 55, 83, 87],
[8, 75, 91],
[5, 37, 59, 78],
[54, 82, 90, 96],
[17, 55, 80],
[29, 61, 63, 72, 73],
[2, 41, 52, 53, 93],
[10, 22, 62, 80],
[2, 8, 82],
[15, 39, 79],
[60, 70, 83, 85, 89],
[9, 21, 34],
[3, 14, 26, 47],
[3, 14, 38, 50],
[40, 42, 43, 62],
[27, 49, 85, 88],
[27, 64, 75],
[9, 14, 28, 41, 79],
[24, 29, 68, 79, 86],
[48, 61, 76],
[1, 19, 71, 80, 100],
[11, 33, 40, 65],
[18, 36, 76, 82, 93],
[59, 79, 95],
[5, 34, 36, 48, 65],
[39, 62, 70],
[25, 44, 89],
[11, 43, 57, 69, 91],
[41, 78, 91],
[3, 24, 42, 43, 60],
[1, 66, 76],
[29, 72, 101],
[6, 74, 76, 86, 93],
[10, 26, 61, 73, 104],
[2, 87, 92, 96, 100],
[3, 51, 89],
[56, 95, 98],
[42, 45, 68, 78, 84],
[21, 48, 92, 103],
[22, 64, 84],
[32, 89, 104],
[20, 21, 72],
[7, 38, 47, 49, 67],
[14, 34, 96],
[34, 49, 64, 94],
[13, 17, 20, 46],
[4, 59, 93],
[23, 52, 62],
[19, 32, 50],
[18, 31, 88, 102],
[5, 17, 51, 98],
[11, 24, 32, 87, 100],
[15, 26, 68, 82, 87],
[25, 78, 99],
[11, 29, 44, 88],
[37, 57, 90],
[1, 71, 89],
[21, 50, 69, 94],
[9, 25, 47],
[24, 54, 74, 103],
[50, 92, 103],
[15, 28, 44, 63],
[40, 65, 84],
[15, 17, 100, 104],
[16, 42, 75, 94],
[28, 69, 98, 102],
[18, 26, 65],
[10, 66, 88],
[13, 23, 67],
[24, 30, 51, 77],
[7, 34, 66],
[6, 22, 37, 102],
[31, 90, 92, 95],
[36, 58, 60],
[6, 40, 67, 69],
[9, 35, 55, 66, 73],
[1, 31, 36, 74, 97],
[10, 85, 94, 101],
[19, 44, 86],
[20, 22, 36, 54],
[11, 37, 63],
[70, 71, 75, 81],
[50, 56, 57],
[4, 55, 58, 77, 84],
[59, 77, 99],
[23, 27, 67, 96],
[16, 18, 19, 50, 63],
[4, 30, 38, 53],
[33, 56, 104],
[6, 15, 46, 101],
[9, 88, 103],
[8, 19, 45, 70],
[35, 46, 99],
[33, 52, 101],
[20, 48, 53],
[12, 98, 99]]

friends_count = {}
total_friendships = 0
arr = []
for i in range(0, len(friends_list)):
    friends = set(friends_list[i])
    for j in range(0, len(friends_list)):
        if i != j:
            for k in friends_list[j]:
                if k == i+1:
                    friends.add(j+1)

    total_friendships += len(friends)
    # print(i+1, friends, len(friends))
    arr.append(list(friends))

# print(arr)
# print(total_friendships)

mmap = {}

for i in range(0, len(arr)):
    for num in arr[i]:
        if (min(i+1, num), max(i+1, num)) in mmap:
            mmap[(min(i+1, num), max(i+1, num))] += 1
        else:
            mmap.update({(min(i+1, num), max(i+1, num)): 1})

# print(mmap)
data = []
for key, val in mmap.items():
    user_id = key[0]
    friend_id = key[1]
    user_ref = CustomUser.objects.filter(pk=user_id).first()
    friend_ref = CustomUser.objects.filter(pk=friend_id).first()
    data.append(
        Friendship(
            user=user_ref,
            friend=friend_ref,
        )
    )


objs = Friendship.objects.bulk_create(data)
print('done')
'''



# for populating predicted_personality field in CusomUser model

'''
def predict_personality(posts):
    test_post = vectorizer.transform([posts]).toarray()
    predicted_target = model_linear_svc.predict(test_post)
    return predicted_target[0]
    

from .models import CustomUser, Posts
from django.db.models import Count
import pickle
from sklearn.svm import SVC,LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from django.db import connection


# load the model from disk
model_linear_svc = pickle.load(open('../Backend/trained_model/finalized_model.sav', 'rb'))
vectorizer = pickle.load(open('../Backend/trained_model/vectorizer_model.pickle', 'rb'))

personality_mapping = {0: 'ENFJ', 1: 'ENFP', 2: 'ENTJ', 3: 'ENTP', 4: 'ESFJ', 5: 'ESFP', 6: 'ESTJ', 7: 'ESTP',
       8: 'INFJ', 9: 'INFP', 10: 'INTJ', 11: 'INTP', 12: 'ISFJ', 13: 'ISFP', 14: 'ISTJ', 15: 'ISTP'}

count_of_posts = Posts.objects.values('user').annotate(dcount=Count('user')).order_by()
# for row in count_of_posts:
#     print(row['user'], row['dcount'])


cursor = connection.cursor()
query_str = """SELECT user_id, cleaned_post FROM (SELECT user_id, cleaned_post, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY timestamp DESC) AS row_number 
                FROM Recommender_posts) AS t WHERE t.row_number <= 50;"""
cursor.execute(query_str)
data = cursor.fetchall()

# print(data)

user_posts = {}

for obj in data:
    if obj[0] not in user_posts.keys():
        user_posts[obj[0]] = obj[1]
    else:
        user_posts[obj[0]] = obj[1] + ' ' + user_posts[obj[0]]

# print(user_posts)

predicted_personality = {}
for key, val in user_posts.items():
    predicted_personality[key] = predict_personality(val)
    user_ref = CustomUser.objects.filter(pk=key).first()
    user_ref.predicted_personality = predicted_personality[key] + 1
    user_ref.save()
    print(key, personality_mapping[predicted_personality[key]])

print('done')
'''



# for recommendation system scoring logic

'''
from .models import CustomUser, Friendship
from django.db.models import Q
import operator

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




user_id = 1
user_ref = CustomUser.objects.filter(pk=1).first()
friends = Friendship.objects.filter(Q(user=user_ref) | Q(friend=user_ref))
# print(friends)

friends_list = []
for friend in friends:
    if user_id == friend.user.pk:
        friend_id = friend.friend.pk
    else:
        friend_id = friend.user.id
    friends_list.append(friend_id)
# print(friends_list)

friend_of_friends = Friendship.objects.filter(Q(user__in=friends_list) | Q(friend__in=friends_list)).exclude(Q(user=user_ref) | Q(friend=user_ref))
# print(len(first_friends))

recommendations = {}
for mf in friend_of_friends:
    # print(mf.user.pk, mf.friend.pk)
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
    
# print(len(recommendations))
# print(recommendations)


recommendations_personality = CustomUser.objects.filter(pk__in=recommendations.keys())
user_personality_mapping = {}
for person in recommendations_personality:
    user_personality_mapping[person.pk] = person.get_predicted_personality_display()

# print(user_personality_mapping)

scoring = {}

for key in recommendations.keys():
    scoring[key] = recommendations[key]*0.5 + get_personality_match_percent(user_ref.get_predicted_personality_display(), user_personality_mapping[key])

scoring = dict( sorted(scoring.items(), key=operator.itemgetter(1),reverse=True))

max_value = max(scoring.values(), default=1)
scoring = {k: v / max_value for k, v in scoring.items()}

# print(scoring)
recommendation_list = [key for key, val in scoring.items() if val >= 0.5]
recommendation_list.sort()
# print(recommendation_list)
'''



# for shuffling the user interest tags

'''
with open('../Backend/datasets/user_interests_tags_list.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

print(lines)

import numpy as np

arr = np.array(lines)
np.random.shuffle(arr)

print(arr)

fp = open("../Backend/datasets/jumbled_tags.txt", "a")
for ele in arr:
    fp.write(ele + '\n')

fp.close()
'''



# for populating tags data in model TagsOfInterest model

'''
from .models import TagsOfInterest

with open('../Backend/datasets/user_interests_tags_list.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

data = []
for tag in lines:
    data.append(
        TagsOfInterest(
            tag_name=tag,
        )
    )


objs = TagsOfInterest.objects.bulk_create(data)
print('done')
'''



# for populating user interest tags data

'''
from .models import TagsOfInterest, UserInterestTags, CustomUser

user_interest_tags_list = [
    [37, 52, 65, 71, 74, 78, 89],
    [11, 12, 34, 49, 51, 76, 82, 83],
    [18, 20, 27, 39, 50, 59, 62, 82, 93],
    [13, 29, 38, 72, 74, 81],
    [6, 23, 28, 34, 41, 61, 66],
    [2, 9, 34, 43, 81, 83, 86, 90, 93],
    [1, 34, 64, 68, 79, 81, 93],
    [25, 43, 44, 91, 97, 99],
    [4, 5, 7, 8, 16, 25, 51, 53, 61, 75],
    [1, 27, 62, 64, 86, 98],
    [19, 21, 25, 29, 30, 75, 81],
    [19, 39, 42, 50, 58, 60, 67, 83, 90, 96],
    [12, 56, 65, 70, 80, 95],
    [11, 18, 49, 64, 71, 74, 75, 81],
    [21, 39, 74, 79, 89, 93],
    [8, 53, 73, 78, 87, 88],
    [3, 16, 25, 36, 39, 55, 69, 88, 92, 95],
    [8, 24, 50, 66, 71, 72, 83, 94],
    [2, 10, 25, 44, 52, 71, 77],
    [2, 5, 7, 38, 41, 48, 96, 99],
    [9, 22, 23, 24, 30, 36, 51, 75, 87],
    [19, 47, 48, 75, 78, 100],
    [6, 10, 26, 33, 54, 81, 89, 99],
    [21, 28, 31, 40, 46, 88, 94],
    [37, 41, 44, 68, 80, 92],
    [22, 23, 24, 32, 70, 79],
    [10, 16, 53, 61, 65, 77],
    [9, 15, 32, 44, 45, 60, 75, 76, 82, 86],
    [4, 10, 26, 37, 42, 45, 52, 65, 70, 73],
    [5, 27, 55, 60, 75, 91],
    [1, 29, 57, 76, 83, 92],
    [4, 9, 24, 29, 70, 98],
    [5, 20, 31, 47, 50, 77, 87],
    [2, 48, 50, 59, 63, 71, 80, 84],
    [29, 43, 47, 48, 61, 65, 86],
    [14, 22, 49, 73, 84, 86],
    [7, 16, 20, 51, 73, 89, 97],
    [8, 30, 41, 48, 53, 69, 72, 76, 93],
    [2, 19, 27, 58, 63, 79, 94, 97],
    [6, 9, 14, 28, 52, 66, 73, 77, 97],
    [36, 38, 57, 70, 76, 92, 98],
    [4, 26, 48, 51, 57, 63, 68, 70],
    [9, 12, 19, 22, 24, 39, 79, 88, 95],
    [11, 18, 31, 35, 49, 57, 96],
    [3, 7, 13, 43, 59, 61, 64, 87],
    [13, 15, 18, 28, 43, 53, 57, 87, 92],
    [5, 17, 25, 46, 54, 94],
    [3, 13, 29, 49, 67, 86],
    [11, 13, 36, 39, 56, 63, 66],
    [5, 12, 23, 24, 36, 100],
    [7, 10, 13, 35, 37, 79, 83, 95],
    [7, 27, 31, 32, 60, 72, 80, 87],
    [21, 34, 40, 52, 58, 67, 69, 73, 83, 88],
    [1, 12, 31, 69, 85, 86],
    [14, 18, 29, 41, 60, 75, 91],
    [49, 55, 79, 85, 89, 93, 95],
    [40, 47, 59, 69, 87, 88, 100],
    [17, 28, 29, 32, 50, 57, 71, 74, 79, 82],
    [10, 23, 30, 33, 46, 65, 66, 67, 93, 95],
    [35, 37, 39, 42, 43, 62, 63, 86],
    [5, 15, 40, 47, 49, 53, 59],
    [4, 26, 31, 33, 34, 55, 65],
    [27, 38, 56, 82, 95, 96],
    [3, 5, 26, 34, 66, 73, 84, 89],
    [1, 3, 8, 77, 82, 91, 94, 100],
    [22, 38, 60, 62, 70, 75, 82, 84, 93],
    [8, 13, 32, 34, 40, 44, 45, 62, 96],
    [2, 8, 16, 30, 35, 45, 88, 97],
    [3, 5, 18, 27, 30, 61, 64, 99],
    [1, 26, 49, 55, 98, 99, 100],
    [6, 12, 17, 30, 65, 76, 81],
    [30, 33, 34, 38, 68, 76, 84, 85, 90, 96],
    [15, 21, 27, 40, 43, 47, 68, 77, 97, 100],
    [6, 17, 27, 48, 50, 77, 90],
    [31, 43, 44, 51, 57, 96],
    [2, 19, 35, 45, 55, 67, 70, 71, 78],
    [17, 25, 28, 55, 62, 99],
    [14, 40, 54, 67, 77, 85, 88, 92],
    [2, 51, 54, 72, 82, 90],
    [3, 38, 41, 48, 50, 54, 55, 69, 81, 92],
    [11, 20, 51, 55, 68, 82, 83, 91],
    [11, 17, 23, 68, 74, 90],
    [11, 13, 14, 59, 77, 81, 89],
    [12, 20, 31, 60, 73, 95],
    [12, 14, 18, 31, 41, 54, 56, 62, 98, 100],
    [33, 35, 53, 89, 96, 100],
    [16, 24, 34, 35, 46, 55, 80],
    [17, 19, 22, 23, 24, 30, 65, 77],
    [40, 62, 67, 72, 74, 85],
    [18, 33, 42, 45, 52, 66, 80, 89],
    [7, 20, 25, 44, 46, 47, 64, 69, 70, 98],
    [7, 13, 28, 41, 66, 99],
    [4, 6, 9, 32, 44, 45, 54],
    [6, 10, 13, 58, 63, 74],
    [16, 17, 45, 47, 63, 99],
    [4, 9, 10, 58, 62, 79],
    [29, 51, 52, 64, 82, 83, 91],
    [20, 38, 39, 45, 67, 69, 85, 88],
    [17, 60, 61, 63, 66, 69, 72, 78, 92, 98],
    [3, 5, 6, 9, 15, 33, 35, 58, 78, 84],
    [9, 25, 26, 45, 52, 57, 80],
    [7, 14, 18, 24, 48, 71, 72],
    [1, 10, 19, 46, 51, 63, 64, 71, 91, 99],
    [15, 37, 42, 56]
]


total_count = 0
data = []
for i in range(0, len(user_interest_tags_list)):
    row = user_interest_tags_list[i]
    total_count += len(row)
    user_id = i + 1
    user_ref = CustomUser.objects.filter(pk=user_id).first()
    for tag_id in row:
        tag_ref = TagsOfInterest.objects.filter(pk=tag_id).first()
        data.append(
            UserInterestTags(
                user=user_ref,
                tag=tag_ref,
            )
        )

print(total_count)
objs = UserInterestTags.objects.bulk_create(data)
print('done')
'''



# for populating users age value

'''
from .models import CustomUser

user_ages = [
    26, 27, 41, 25, 54, 59, 22, 21, 38, 38, 38, 59, 45, 59, 56, 53, 50, 
    51, 48, 53, 26, 13, 20, 31, 21, 26, 57, 19, 36, 35, 33, 41, 36, 12, 
    26, 13, 12, 45, 45, 41, 45, 42, 30, 23, 60, 26, 58, 35, 20, 19, 40, 
    58, 48, 26, 50, 54, 39, 44, 27, 14, 27, 28, 15, 47, 18, 53, 41, 23, 
    46, 60, 33, 22, 29, 46, 24, 17, 42, 34, 49, 18, 51, 22, 45, 53, 35, 
    60, 25, 41, 42, 20, 42, 54, 39, 50, 33, 57, 12, 35, 19, 54, 43, 57, 
    34, 58]

for i in range(0, 104):
    user_id = i + 1
    user_ref = CustomUser.objects.filter(pk=user_id).first()
    user_ref.age = user_ages[i]
    user_ref.save()

print('done')
'''