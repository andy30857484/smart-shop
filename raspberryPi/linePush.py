from chatBotConfig import channel_secret, channel_access_token, lineId
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import  TextSendMessage

line_bot_api = LineBotApi(channel_access_token)

alertMessage = TextSendMessage(text='alert! please check your phone!!!')

def linePush(cost,alertFlag):
    if alertFlag == 'True':
        print("alertFlag = True")
        line_bot_api.push_message(lineId,alertMessage)
        powerValueMessage = TextSendMessage(text='your total cost has arrived %s'%(cost))
        line_bot_api.push_message(lineId,powerValueMessage)
    if alertFlag == 'False':
        print("alertFlag = False")
    else:
        print("alertFlag is not boolen")
    
    
