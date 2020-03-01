import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from pchome import scrapy

import re

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'HcDTvLuiqFzW3oG5AXN5uq9bH960sEEm7lILqQUVydR3j/95eOAuuhZLppht6fbZXVfcoipDrjLRn08oYHuDkMlxBVxc+CNzfGjzspLJr/oqV6sjP+OZhtgGLPxGe9gt23e1sBHAfHi7nir9td9kMQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('1e4eaba0b066667690bdbb650e0e3df5')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=re.match(
    #     "[a-zA-Z0-9]+-[a-zA-Z0-9]+", event.message.text))
    search_id = re.match(
        "[a-zA-Z0-9]+-[a-zA-Z0-9]+", event.message.text)
    print("搜尋的編號:" + search_id.string)
    machines = scrapy(search_id.string)
    prods = "搜尋到" + str(len(machines)) + "個結果:\n"
    for machine in machines:
        prods += machine
        prods += "\n商品名稱:" + machines[machine]['name']
        prods += "\n商品描述:" + machines[machine]['describe']
        prods += "\n商品價格:" + str(machines[machine]['price'])
        prods += "\n禮物項目" + machines[machine]['gift']
    message = prods
    line_bot_api.reply_message(event.reply_token, prods)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
