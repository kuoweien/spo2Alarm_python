# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 16:02:35 2019

@author: Albert
"""

#from flask import Flask, request, abort
import sys

from linebot import (
    LineBotApi, WebhookHandler
)
#from linebot.exceptions import (
#    InvalidSignatureError
#)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from linebot.exceptions import LineBotApiError

#from linebot.exceptions import LineBotApiError

#app = Flask(__name__)



# 老師 mobile C 帳號
# access token
#NjIkL+CsyF0V53ANiHJg8DnyijQgvr3wuuOhIdLiFIJ+lh7YrJDRh5mOIRZ58ggE63UrQeJSjazl2DItfYoKeoa0eNPtXEd//EcohfScdntpoooPfTwWVHjCqvSSRgav2uhi9PPhuatmhn3+PZTTmQdB04t89/1O/w1cDnyilFU=
line_bot_api = LineBotApi('aWlDgFHAaNNRFlgZNHLV7PFnwYEx+XnX1DkAtNow8dB+XqRo6lCBn8W0yfGp7Lm17xkJsm9QfYgkbr367NyyMyWnGzy4b8ndk0xyP8TPxliK4e2ZSX50R/MMgWoKIQyXr23nHOhm2ru0leAsVKmy0AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6c1d526b9e189596b20b28285a31dbb0')

def push_message(send_message):
  to="C23cd143e9f3da3854d713078b99b8e23"
  try:
    line_bot_api.push_message(to, TextSendMessage(text=send_message))
  except LineBotApiError as e:
    # error handle
    raise e
    
#push_message("C23cd143e9f3da3854d713078b99b8e23","XXXXX")

# 'U5e57b9949af64b17d289ecd70d6d1eb7' 郭老師 userID
# 'C4667ba43436daf87f06b6c4574aec170' 群組GroupID
# 'Uc72a943914f7734368145c9ab770a276' 名仁 userID
# 'C534b9043d5cd44baca950fd4859d5a37' 遠端加護監測 GroupID
# 'C94ef7a4a34ca0a5f6aae136e1a31ab8e' 陳昌明

if __name__ == "__main__":

  push_message(sys.argv[1])
#    push_message(sys.argv[2],sys.argv[1])

# "C23cd143e9f3da3854d713078b99b8e23" 血氧機通報群組
