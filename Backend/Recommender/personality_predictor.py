import pickle
# from sklearn.svm import SVC,LinearSVC
# from sklearn.feature_extraction.text import TfidfVectorizer
# import pandas as pd
import re
import urllib.request
import json
import urllib
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords



nltk.download('wordnet')
nltk.download('stopwords')

lemmatiser = WordNetLemmatizer() 
cachedStopWords = stopwords.words("english")

# model_linear_svc = pickle.load(open('../Backend/trained_model/finalized_model.sav', 'rb'))
vectorizer = pickle.load(open('../Backend/trained_model/vectorizer_model.pickle', 'rb'))

svm_I_or_E = pickle.load(open('../Backend/trained_model/svm_model_I_or_E.sav', 'rb'))
svm_N_or_S = pickle.load(open('../Backend/trained_model/svm_model_N_or_S.sav', 'rb'))
svm_T_or_F = pickle.load(open('../Backend/trained_model/svm_model_T_or_F.sav', 'rb'))
svm_P_or_J = pickle.load(open('../Backend/trained_model/svm_model_P_or_J.sav', 'rb'))


def get_youtube_video_title(videoID):

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



def predict_personality(posts):
    test_post = vectorizer.transform([posts]).toarray()
    # predicted_target = model_linear_svc.predict(test_post)

    I_or_E_prediction = svm_I_or_E.predict(test_post)
    N_or_S_prediction = svm_N_or_S.predict(test_post)
    T_or_F_prediction = svm_T_or_F.predict(test_post)
    J_or_P_prediction = svm_P_or_J.predict(test_post)

    I_or_E_mapping = {0: 'E', 1: 'I'}
    N_or_S_mapping = {0: 'N', 1: 'S'}
    T_or_F_mapping = {0: 'F', 1: 'T'}
    J_or_P_mapping = {0: 'J', 1: 'P'}

    predicted_target = I_or_E_mapping[I_or_E_prediction[0]] + N_or_S_mapping[N_or_S_prediction[0]] + T_or_F_mapping[T_or_F_prediction[0]] + J_or_P_mapping[J_or_P_prediction[0]]
    personality_mapping = {
      'ENFJ': 0, 'ENFP': 1, 'ENTJ': 2, 'ENTP': 3, 'ESFJ': 4, 'ESFP': 5, 'ESTJ': 6, 'ESTP': 7, 
      'INFJ': 8, 'INFP': 9, 'INTJ': 10, 'INTP': 11, 'ISFJ': 12, 'ISFP': 13, 'ISTJ': 14, 'ISTP': 15
    }

    return personality_mapping[predicted_target]
