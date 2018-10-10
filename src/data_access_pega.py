#-*- coding: utf-8 -*-

from pymysql import connect
from pymysql import cursors
import json
from setup import *

def init():
    with open(config_path_pega) as config_buffer:
        config = json.loads(config_buffer.read())
    return config['HOST'],config['DB_NAME'],config['USER_NAME'],config['PASSWORD']

def get_connection():
    HOST,DB_NAME,USER_NAME, PASSWORD = init()
    conn = connect(host=HOST, user=USER_NAME, passwd=PASSWORD, db=DB_NAME, charset='utf8')
    conn.autocommit(False)
    return conn

def get_cursor(conn):
    """

    :rtype: pymysql.cursors.Cursor
    :param conn:
    :return:
    """
    cur = conn.cursor()
    return cur


def get_dict_cursor(conn):
    """
    :rtype: pymysql.cursors.Cursor
    :param conn:
    :return:
    """
    cur = conn.cursor(cursors.DictCursor)
    return cur

def free_connection(conn, cur):
    """

    :param conn:
    :param cur:
    :return:
    """
    try:
        cur.close()
        conn.close()
    except:
        pass

def get_content_none_cateId():
    query = """ select *
                from NewsDb.pega_news
                where NewsDb.pega_news.cate_id is Null
                order by NewsDb.pega_news.publish_date desc
                limit 1000;"""
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row

def get_totalNews_category(cate_id):
    query = """ select source, count(id) as total
                from NewsDb.pega_news
                where cate_id ='%s'
                group by source;""" %cate_id
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row

def get_site():
    query = """ select distinct NewsDb.pega_news.source
                from NewsDb.pega_interaction
                inner join NewsDb.pega_news on NewsDb.pega_interaction.news_id = NewsDb.pega_news.id
                where NewsDb.pega_news.publish_date > now() - interval 2 day 
                      and NewsDb.pega_news.publish_date < now();"""
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row

#get news in a site
def get_news_site(site):
    query = """ select *
                from NewsDb.pega_interaction
                inner join NewsDb.pega_news on NewsDb.pega_interaction.news_id = NewsDb.pega_news.id
                where NewsDb.pega_news.publish_date > now() - interval 2 day 
                and NewsDb.pega_news.publish_date < now()
                and NewsDb.pega_news.source = "%s"
                order by NewsDb.pega_news.publish_date desc
                limit 100""" %site
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row

def get_news_for_api():
    query = """ SELECT * 
                FROM NewsDb.special_news
                where type = 6
                order by update_time desc
                LIMIT 10;"""
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row


def insert(source,url,hash_url,type,insert_time,update_time) :
    query = "INSERT INTO NewsDb.special_news (source,url,hash_url,type,insert_time,update_time)" \
            " VALUES ('%s', '%s','%s','%s','%s','%s')" % (source, url, hash_url, type,insert_time,update_time)
    print(query)
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print(e,"\n")
    finally:
        free_connection(conn, cur)


def update_cateId(id, cate_id) :

    query = """ update NewsDb.pega_news
                set NewsDb.pega_news.cate_id = '%s'
                where NewsDb.pega_news.id = '%s'""" %(cate_id,id)
    print(query)
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print(e,"\n")
    finally:
        free_connection(conn, cur)

def update_updateTime(url, updateTime) :

    query = """ update NewsDb.special_news
                set NewsDb.special_news.update_time = '%s'
                where NewsDb.special_news.url = '%s';""" %(updateTime,url)
    print(query)
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print(e,"\n")
    finally:
        free_connection(conn, cur)