# -*- coding: utf-8 -*-
from setup import *
import time
import datetime
from similar import *
from data_access_pega import *
from setup import *

id_cates = [1,2,3,4,5,6,7,8,9,10,11,12,13]

def score_site_cate():
    result = {}
    data_all = []
    sites = get_site()
    # print('sites' , sites)
    for id in id_cates :
        ## get total news in a category_id
        data = get_totalNews_category(id)

        data = sorted(data, key=lambda x:x['total'],reverse=True)
        max_count = data[0]['total']
        for site in data :
            weight = round(float(site['total']) / max_count,4)
            site.update({
                "weight":weight,
                "cate_id":id
            })
        data_all.append(data)
    for site in sites :
        name_site = site['source']
        data = {}
        for data_cateId in data_all :
            for w_site in data_cateId :
                if name_site == w_site['source'] :
                    data.update({w_site['cate_id']:w_site['weight']})
        result.update({
            str(name_site):data
        })

    return result

