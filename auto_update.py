from flask import Flask, jsonify
from src.score import *
import time
import threading
from src.data_access_pega import *

trend = Trend()
result_all_site = trend.get_score_all_site()
# print("result_all_site " ,result_all_site)
urls = [news['url'] for news in result_all_site]


def update_data_each():
    global result_all_site
    global urls
    while True:
        temp_update = []
        temp_insert = []

        result_all_site_seconds = trend.get_score_all_site()
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for news in result_all_site_seconds:
            if (news['url'] in urls ) :
                # print("url trung lap ", news['url'])
                for news_prev in result_all_site :
                    if news_prev['url'] == news['url']:
                        news_prev['update_time'] = update_time
                        temp_update.append(news_prev)
                        break
            elif news['url'] not in urls :
                temp_insert.append(news)
        # print("lenght temp_update", len(temp_update))
        result_all_site = result_all_site_seconds
        urls = [news['url'] for news in result_all_site]
        for news in temp_insert :
            print("insert ", news['url'], news['insert_time'], news['update_time'])
            insert(news['source'], news['url'], news['hash_url'], news['type'],
                   news['insert_time'], news['update_time'])
        for news in temp_update :
            print("update ", news['url'], news['insert_time'], news['update_time'])
            update_updateTime(news['url'],news['update_time'])

        print("===============end=================")
        time.sleep(600)



def main():
    thread = threading.Thread(target=update_data_each, args=())
    thread.start()


if __name__ == "__main__":
    main()
