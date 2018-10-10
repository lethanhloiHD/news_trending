#-*- coding: utf-8 -*-

from setup import *
from src.score import *
import datetime
from src.similar import *
import json
from src.data_access_pega import *
import re
from src.category_classify import *
from src.set_wei import *
import time


if __name__ == '__main__':
    while True :
        data = get_news_none_cat()
        print(len(data))
        update_category_news(data)
        time.sleep(60   )