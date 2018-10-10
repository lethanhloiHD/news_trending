from setup import *
import time
import datetime
from similar import *
from data_access_pega import *
from setup import *
from set_wei import *
from datetime import timedelta


def init_setup(file):
    with open(file) as config_buffer:
        config = json.loads(config_buffer.read())
    return config

class Trend:

    def __init__(self):
        pass

    def score(self,reac,comm,share,delta_time, g = 1.8):
        return ( 1.0 * (reac * 0.3 + comm* 0.6 + share * 0.7) / (delta_time +1) ** g)


    def score_timeseris(self, list_time_seris, score_of_category):
        # print("first ", str(list_time_seris[0].split(";")[0]))
        time_floor = datetime.datetime.strptime(str(list_time_seris[0].split(";")[0].split(".")[0]),
                                                "%Y-%m-%d %H:%M:%S")
        time_ceil = time_floor + timedelta(hours=3)

        list_items_temp = []
        score_total = 0
        for items in list_time_seris:
            detail_items = items.split(";")
            time_items = datetime.datetime.strptime(detail_items[0].split(".")[0], "%Y-%m-%d %H:%M:%S")
            if time_items >= time_floor and time_items < time_ceil:
                list_items_temp.append(items)
            elif time_items >= time_ceil:
                if len(list_items_temp) > 1:
                    first_items = list_items_temp[0].split(";")
                    end_items = list_items_temp[len(list_items_temp) - 1].split(";")

                    react = int(end_items[1]) - int(first_items[1])
                    comm = int(end_items[2]) + int(end_items[4]) - int(first_items[2]) - int(first_items[4])
                    share = int(end_items[3]) - int(first_items[3])
                    delta_time = round((datetime.datetime.now()
                                        - datetime.datetime.strptime(str(first_items[0].split(".")[0]),
                                                                     "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600, 1)
                    score_ = self.score(react, comm, share, delta_time)
                    score_total += score_

                elif len(list_items_temp) == 1:
                    only_items = list_items_temp[0].split(";")

                    react = int(only_items[1])
                    comm = int(only_items[2]) + int(only_items[4])
                    share = int(only_items[3])
                    delta_time = round((datetime.datetime.now()
                                        - datetime.datetime.strptime(str(only_items[0].split(".")[0]),
                                                                     "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600, 1)
                    score_ = self.score(react, comm, share, delta_time)

                    score_total += score_

                time_floor = time_items
                time_ceil = time_floor + timedelta(hours=3)

        return score_total*score_of_category

    def get_score_with_detail(self, data, score_cate_of_site):
        data_del = []
        ob = datetime.datetime.now() - timedelta(days=1)
        thre_time = datetime.datetime.strftime(ob, "%Y-%m-%d %H:%M:%S")
        # print("threshold time ", thre_time)
        for news in data:
            # print(news['url'], news['detail'])
            detail_time_seris = news['detail'].split("|")
            # time_end = detail_time_seris[len(detail_time_seris) - 1]
            list_time_pre = []
            for items in detail_time_seris:
                detail = items.split(";")
                time_detail = detail[0]
                # print("time ", time_detail)
                if time_detail >= thre_time:
                    list_time_pre.append(items)
            # print("list time_pre : ", list_time_pre)

            cate_id = news['cate_id']
            score_of_category = 1.0
            if cate_id != None and cate_id in score_cate_of_site.keys():
                score_of_category = score_cate_of_site[cate_id]

            score_r = self.score_timeseris(list_time_pre, score_of_category)
            if (score_r > 0.0):
                # print(
                #     "score :", score_r
                # )
                news.update({"score": score_r})
            else:
                data_del.append(news)
        data_final = [d for d in data if d not in data_del]
        result = sorted(data_final, key=lambda k: k['score'], reverse=True)
        return result

    def get_score_a_site(self,site_name, ratio, score_cate_of_site):
        data_site = get_news_site(site_name)
        score_site = []
        if (len(data_site) > 0):
            score_site = self.get_score_with_detail(data_site, score_cate_of_site)
        return score_site[0:int(ratio)]


    def get_score_all_site(self):
        score_of_site_all = score_site_cate()
        #
        result_temp = []
        result = []
        sites = get_site()
        for site in sites:
            data_score = self.get_score_a_site(site['source'], 5, score_of_site_all[site['source']])
            # print(site['source'], "data score" , data_score)
            for data in data_score:
                result_temp.append(data)
        result_temp = sorted(result_temp, key=lambda k: k['score'], reverse=True)
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for rs in result_temp:
            result.append({
                "news_id": rs['news_id'],
                "source": rs['source'],
                "title": rs['title'],
                "content": rs['content'],
                "sapo": rs['sapo'],
                "url": rs['url'],
                "type": 6,
                "insert_time": update_time,
                "publish_date": rs['publish_date'],
                "update_time": update_time,
                "hash_url": "",
                "score": rs['score'],
                "reaction": rs['reaction'],
                "comment": rs['comment'],
                "comment_plugin": rs['comment_plugin'],
                "share": rs['share']
            })

        result = result[:50]
        temp = []
        for i in range(len(result)):
            text1 = result[i]['title'] + " " + result[i]['content']
            for j in range(i + 1, len(result)):
                text2 = result[j]['title'] + " " + result[j]['content']
                # print(result[i]['url'], result[j]['url'])
                check = Similar(text1,text2)
                if (check.check_similar()):
                    temp.append(result[j])
        print(result[0:threshold])
        return result[0:threshold]


