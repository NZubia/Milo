import urllib.request
import urllib.parse
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as sw

stopwords =["reproducir", "reproduce", "escuchar", "quiero", "cancion"]

def get_response(message):

    token_list = word_tokenize(str(message), "spanish")
    clean_tokens = []

    for token in token_list:
        token = token.lower()

        if token in stopwords or token in set(sw.words("spanish")):
            continue

        clean_tokens.append(token)

    message = " ".join(clean_tokens)

    query_string = urllib.parse.urlencode({"search_query": message})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

    return "Here you can find your Song!!: http://www.youtube.com/watch?v=" + search_results[0]