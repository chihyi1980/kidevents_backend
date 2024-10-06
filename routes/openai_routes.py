from datetime import datetime 
from flask import Blueprint, request, jsonify
from db.option_db import find_all_tag
import json
from util.openai import chat

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

    msg = '''
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
    msg += tags_str
    msg += '''
    裡面幫我挑出1到3個最符合的填入，內容為JSON array 格式，一定只能從這裏面挑選，不能自己創造。
    最後，你的回答只需要寫出標準JSON格式，不要寫任何額外的文字。網站的內容如下:
    '''
    msg += str(eventContent)
    resp = chat(msg)

    # 將純文字轉換為 JSON 物件，由於open ai 回覆內容會在前後加入  ```json 與 ``` ，故將其去除再轉換為JSON
    event_json = json.loads(resp.strip("```json").strip("```").strip())

    #TODO
    print(event_json)

    return event_json, 201

