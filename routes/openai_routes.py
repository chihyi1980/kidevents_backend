from datetime import datetime 
from flask import Blueprint, request, jsonify
from db.option_db import find_all_tag
import json
from model.openai import chat
from model.crawler import get_page_content
from db.events_db import insert_event
from db.option_db import find_all_loc, find_all_tag
import pytz
from utils.tokens import count_tokens, trim_content

openai_bp = Blueprint('openai_bp', __name__)

#輸入活動文字內容，交給open ai api之後產出JSON 內容，自動寫入event DB
@openai_bp.route('/openai/create_event', methods=['POST'])
def add_openai_new_event():
    data = request.get_json()

    #TODO
    print(data)

    eventContent = data['eventContent']

    tags = find_all_tag()
    # 过滤掉 isEnable != True 的 tags
    tags = filter(lambda x: x.get('is_enabled', 0) == True, tags)
    tags_value = [tag['value'] for tag in tags]
    # 將 JSON 物件轉換為字串
    tags_str = json.dumps(tags_value, ensure_ascii=False)

    msg_template = '''
    我會輸入一個網站內容，請幫我分析這個網站內容幫我轉化為標準JSON格式，格式如下:  {
	"event_name",  //活動名稱
	"event_start_date",  //活動開始日期，格式為 yyyy-MM-dd
	"event_end_date",    //活動結束日期，格式為 yyyy-MM-dd
	"event_min_age"		//最小參與活動年齡，若是國小生則最小年齡為6歲
	"event_max_age",    //最大參與活動年齡，若是國小生則最大年齡為12歲
	"event_price",	//活動費用
	"event_content",  //活動內容文字
	"event_loc_detail",  //活動詳細地址
	"event_img"  //活動圖片
	"event_tag_name" //活動類型，後面會詳細說明
    }
    如果內文並沒有寫出 max_age  min_age event_price event_img ，該欄位可以空著。
    event_tag_name 欄位請從
    '''
    msg_template += tags_str
    msg_template += '''
    裡面幫我挑出1到3個最符合的填入，內容為JSON array 格式，一定只能從這裏面挑選，不能自己創造。
    最後，你的回答只需要寫出標準JSON格式，不要寫任何額外的文字。網站的內容如下:
    '''
    msg_template += str(eventContent)
    resp = chat(msg_template)

    # 將純文字轉換為 JSON 物件，由於open ai 回覆內容會在前後加入  ```json 與 ``` ，故將其去除再轉換為JSON
    event_json = json.loads(resp.strip("```json").strip("```").strip())

    #TODO
    print(event_json)

    return event_json, 201

#先爬取 URL網站內容，接下來丟給open ai 去直接生成 json ，再加入活動列表
@openai_bp.route('/openai/create_by_url', methods=['POST'])
def add_event_url():
    req_data = request.get_json()

    eventContent = get_page_content(req_data['url'])

    #取得網站中所有文字內容
    eventText = eventContent.get_text()
    
    # 找出所有 <img> 標籤
    img_tags = eventContent.find_all('img')
    # 將 <img> 標籤字串加入到 eventText 的最尾端
    for img in img_tags:
        eventText += '\n' + str(img)
        #只抓第一張圖片，後面放棄
        break

    #找出目前所有活動類型
    tags = find_all_tag()
    # 过滤掉 isEnable != True 的 tags
    tags = filter(lambda x: x.get('is_enabled', 0) == True, tags)
    tags_value = [tag['value'] for tag in tags]
    # 將 JSON 物件轉換為字串
    tags_str = json.dumps(tags_value, ensure_ascii=False)

    msg_template = '''
    我會輸入一個網站內容，請幫我分析這個網站內容幫我轉化為標準JSON格式，格式如下:  {
	"event_name",  //活動名稱
	"event_start_date",  //活動開始日期，格式為 yyyy-MM-dd
	"event_end_date",    //活動結束日期，格式為 yyyy-MM-dd
	"event_min_age"		//最小參與活動年齡，若是國小生則最小年齡為6歲
	"event_max_age",    //最大參與活動年齡，若是國小生則最大年齡為12歲
	"event_price",	//活動費用
	"event_content",  //活動內容文字
	"event_loc_detail",  //活動詳細地址
	"event_img"  //活動圖片
	"event_tag_name" //活動類型，後面會詳細說明
    }
    如果內文並沒有寫出 max_age  min_age event_price event_img ，該欄位可以空著。
    event_tag_name 欄位請從
    '''
    msg_template += tags_str
    msg_template += '''
    裡面幫我挑出1到3個最符合的填入，內容為JSON array 格式，一定只能從這裏面挑選，不能自己創造。
    最後，你的回答只需要寫出標準JSON格式，不要寫任何額外的文字。網站的內容如下:
    '''

    # 裁減 eventText 如果超過 token 限制
    trimmed_eventText = trim_content(msg_template, tags_str, eventText)
    msg = msg_template + trimmed_eventText

    resp = chat(msg)

    # 將純文字轉換為 JSON 物件，由於open ai 回覆內容會在前後加入  ```json 與 ``` ，故將其去除再轉換為JSON
    data = json.loads(resp.strip("```json").strip("```").strip())

    #TODO
    print(data)

    #先建立 loc map，將 縣市名稱 轉換為 id
    """
    locs = find_all_loc()
    locs_dict = {}
    for loc in locs:
        locs_dict[loc['value']] = str(loc['_id']) 

    #轉換 loc_name to loc
    data['event_loc'] = locs_dict[data['event_loc_name']]
    del data['event_loc_name']
    """

    tags = find_all_tag()
    tags_dict = {}
    for tag in tags:
        tag['_id'] = str(tag['_id'])
        tags_dict[tag['value']] = tag

    data['event_tag'] = []
    for tag_name in data['event_tag_name']:
        try:
            data['event_tag'].append(tags_dict[tag_name])
        except KeyError:
            continue
    del data['event_tag_name']

    data['event_link'] = req_data['url']
       
    utc_now = datetime.now(pytz.utc)
    local_time = utc_now.astimezone(pytz.timezone('Asia/Taipei'))
    data['created_at'] = local_time.isoformat()
    data['updated_at'] = local_time.isoformat()
    data['is_online'] = False
    data['is_enabled'] = True
    insert_event(data)
    return jsonify({"msg_template": "Event added successfully"}), 201
