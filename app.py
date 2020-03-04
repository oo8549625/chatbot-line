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
line_bot_api = LineBotApi(os.environ.get("LINE_BOT_TOKEN"))
# Channel Secret
handler = WebhookHandler(os.environ.get("LINE_BOT_SECRET"))

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
    search_id = re.match(
        r"\w+(-\w+)+", event.message.text)

    if(search_id):
        print("搜尋的編號:" + str(search_id.group()))
        machines = scrapy(search_id.group())
        if(machines == -1):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="請求失敗"))
        prods = "搜尋到" + str(len(machines)) + "個結果:"
        for machine in machines:
            prods += "\n代號:" + machine
            prods += "\n名稱:" + machines[machine]['name']
            prods += "\n描述:" + machines[machine]['describe']
            prods += "\n價格:" + str(machines[machine]['price'])
            prods += "\n禮物:" + machines[machine]['gift']
            prods += "\n=====================我是分隔線====================="
        message = TextSendMessage(text=prods)
        line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
