from setup import *
import time
import datetime
import re
import time
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


tokenizer = RegexpTokenizer(r'\w+')
class Similar:
    def __init__(self, text1, text2):
        self.text1 = text1
        self.text2 = text2

    def cleanhtml(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def load_stoplist(self,file):
        stop_words = []
        for x in open(file, 'r').read().split('\n'):
            stop_words.append(x)
        return stop_words

    def cosine_sim(self):
        stop_words = self.load_stoplist(stop_path)
        data = [self.text1.strip().lower(), self.text2.strip().lower()]
        model = TfidfVectorizer(analyzer='word', stop_words=stop_words, )
        model.fit_transform(data)
        tfidf_text1 = model.transform([self.text1])
        tfidf_text2 = model.transform([self.text2])
        cosine = cosine_similarity(tfidf_text1, tfidf_text2)

        return cosine[0][0]

    def check_similar(self,):
        check = False
        cosine = self.cosine_sim()
        # print(cosine)
        if (cosine > threshold_similar):
            check = True

        return check





