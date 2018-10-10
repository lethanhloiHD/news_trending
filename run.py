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
from datetime import timedelta


if __name__ == '__main__':
    trend = Trend()
    a = trend.get_score_all_site()
    for i in a :
        print(i)

