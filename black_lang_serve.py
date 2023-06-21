# This Python file uses the following encoding: utf-8
# 作者：black_lang
# 创建时间：2023/6/19 1:52
# 文件名：black_lang_serve.py

import requests
import re
from flask import Flask, request
'''注意，这里的import api是另一个py文件，下文会提及'''

app = Flask(__name__)

f=open('keys.txt','r',encoding='utf-8')
keys=[re.sub('[\n \t]','',key) for key in f.readlines()]
f.close()
aim_qqs=keys[0].split(':')[-1].split(',')
false_group=keys[1].split(':')[-1].split(',')

@app.route('/', methods=["POST"])
def L_post_data():
    global keys
    data=request.get_json()
    # print(data)
    if data['post_type'] == 'message':
        if data['message_type'] == 'group':
            message=data['message']
            if data['group_id'] not in false_group:
                for key in keys[3:]:
                    if key in message:
                        group_info=requests.get(f"http://127.0.0.1:5700/get_group_info?group_id={data['group_id']}").json()
                        # print(group_info)
                        global aim_qqs
                        send_message=f"昵称:{data['sender']['nickname']}\n" \
                                     f"qq号:{data['user_id']}\n" \
                                     f"群名：{group_info['data']['group_name']}\n" \
                                     f"群号：{data['group_id']}\n" \
                                     f"关键词：{key}\n" \
                                     f"信息：{data['message']}"
                        print('\n'+send_message+'\n')
                        for aim_qq in aim_qqs:
                            requests.get(f'http://127.0.0.1:5700/send_private_msg?user_id={aim_qq}&message={send_message}')
                        # print(res1)
                        break

    return 'OK'
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5701)
