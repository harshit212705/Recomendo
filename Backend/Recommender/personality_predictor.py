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



nltk.download('wordnet')
nltk.download('stopwords')

lemmatiser = WordNetLemmatizer() 
cachedStopWords = stopwords.words("english")

model_linear_svc = pickle.load(open('../Backend/trained_model/finalized_model.sav', 'rb'))
vectorizer = pickle.load(open('../Backend/trained_model/vectorizer_model.pickle', 'rb'))


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
    predicted_target = model_linear_svc.predict(test_post)
    return predicted_target[0]
