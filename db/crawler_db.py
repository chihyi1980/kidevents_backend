from pymongo import MongoClient
from bson import ObjectId
from config import Config

client = MongoClient(Config.MONGO_URI)
crawler_db = client['crawler_db']

#紀錄已經爬取過的url
used_url_collection = crawler_db['used_url']

#爬蟲設置JSON
#範例
"""
{
    'host' : 'https://tam.gov.taipei/',  //爬取主網址
    'list_url': 'News.aspx?n=49854D6439EC40C0&sms=72544237BBE4C5F6',  //列表頁
    'event_url_p': 'News_Content.aspx',  //每個 event page的抓取特徵值
    'encoding' : 'utf-8',  //網頁編碼
    'target_id' : 'CCMS_Content',   //活動內容div id
    'event_loc' : '臺北市',   //地區
    'event_org' : '台北市立天文科學教育館'   //活動機構名稱
}
"""
crawler_config_collection = crawler_db['crawler_config']


def insert_used_url(url):
    return used_url_collection.insert_one(url)

def is_url_exist(url):
    query = {"value": url}
    result = used_url_collection.find_one(query)
    return result is not None

def insert_crawler_config(config):
    return crawler_config_collection.insert_one(config)

def find_all_crawler_config():
    return list(crawler_config_collection.find())

def update_crawler_config(config_id, data):
    crawler_config_collection.update_one({'_id': ObjectId(config_id)}, {'$set': data})