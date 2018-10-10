# coding=utf-8
import os
from gensim import corpora
from sklearn.externals import joblib
from scipy.sparse import csr_matrix
from setup import *
import re
import json
from src.score import *

def init():
    cate_ids  = init_setup(config_cat_id)
    return cate_ids

def cleanhtml(raw_html):
    """
    Clear tag <.*?>  in the content of news
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_sparse_representation(doc, vocab_size):
    """  Run program classify news """

    row = []
    col = []
    data = []
    total_sum = 0.0
    for i in range(len(doc)):
        (wid, fre) = doc[i]
        row.append(0)
        col.append(wid)
        data.append(fre)
        total_sum += fre
    for i in range(len(doc)):
        data[i] = data[i] / total_sum
    vector = csr_matrix((data, (row, col)), shape=(1, vocab_size), dtype=float)
    return vector



def get_cat(text, file_model,file_dict):
    """ Return the id of news """

    classifier = joblib.load(file_model)
    dictionary = corpora.Dictionary.load_from_text(file_dict)
    doc = dictionary.doc2bow(text.split())
    caterogy = []
    if (len(doc) > 0):
        vecto = get_sparse_representation(doc, len(dictionary.token2id))
        caterogy = classifier.predict(vecto)

    return caterogy[0]


def get_news_none_cat():
    """
    :return: the array of news dont have id of category and update
            if it have  id of category
    """
    cate_ids = init()
    data_all = get_content_none_cateId()
    result = []
    for news in data_all :
        if news[u'topic_name'].lower() not in category_id :
            result.append(news)
        elif news[u'topic_name'].lower() in category_id :
            print(news[u'topic_name'].lower(),news['id'] ,cate_ids[news[u'topic_name'].lower()] )
            update_cateId(news['id'], cate_ids[news[u'topic_name'].lower()])
    return result


def update_category_news(data):
    for news in data :
        title = news['title']
        sapo = news['sapo']
        content = cleanhtml(news['content'])
        text = title.lower() + " " + sapo.lower() + " " + content.lower()
        cate_id = get_cat(text, file_model, file_dict)
        update_cateId(news['id'], cate_id)







