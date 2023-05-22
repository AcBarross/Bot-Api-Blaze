import telegram
import time

TOKEN = '5793864346:AAEq4Z6lKXzXumyMw-CxVLMJs8vXOKBB8Mo'

bot = telegram.Bot(TOKEN)


def delete(chat_id, msg):
        bot.send_message(chat_id=chat_id, text = msg)

chat = '6290068374'
message = 'ola Robot'

delete(chat, message)