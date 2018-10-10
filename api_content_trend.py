from flask import Flask, jsonify
from src.score import *
import time
import threading
from src.data_access_pega import *

application = Flask(__name__)


trend = Trend()
result_all_site = trend.get_score_all_site()


def update_data_each():
    global result_all_site
    global urls
    while True:
        result_temp = trend.get_score_all_site()
        result_all_site = result_temp
        print("===============end=================")
        time.sleep(600)


@application.route("/<content_trend>")
def run_each_site(content_trend):
    result = []
    for rs in result_all_site :
        result.append({
            "news_id": rs['news_id'],
            "source": rs['source'],
            "title": rs['title'],
            "url": rs['url'],
            "type": 6,
            "insert_time": rs['insert_time'],
            "publish_date": rs['publish_date'],
            "update_time": rs['update_time'],
            "hash_url": "",
            "score": rs['score'],
            "reaction": rs['reaction'],
            "comment": rs['comment'],
            "comment_plugin": rs['comment_plugin'],
            "share": rs['share']
        })
    return jsonify(result)

def main():
    thread = threading.Thread(target=update_data_each, args=())
    thread.start()


if __name__ == "__main__":
    main()
    application.run(host="0.0.0.0", port=8081)


