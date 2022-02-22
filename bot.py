import telebot
from pycoingecko import CoinGeckoAPI
from collections import OrderedDict
import requests
import json
from time import sleep
# from telegram.ext import ParseMode
import time

link = "https://t.me/yatemez"

cg = CoinGeckoAPI()
# delay = 60


bot = telebot.TeleBot('your token')


@bot.message_handler(commands=['btc'])
def bitcoin(message):
	price = cg.get_price(ids='bitcoin', vs_currencies='usd')
	bot.send_message(message.chat.id, f'Bitcoin  {price["bitcoin"]["usd"] }$')


@bot.message_handler(commands=['eth'])
def ethereum(message):
	price = cg.get_price(ids='ethereum', vs_currencies='usd')
	bot.send_message(message.chat.id, f'Ethereum  {price["ethereum"]["usd"] }$')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	bot.send_message(message.chat.id, """\
Hi there, {0.first_name}, I am Alexa bot v3.
I am here to help you! I can send you crypto price.
Just type or click on commands:
/main
/btc
/eth
/ltc
/doge
/creator
""".format(message.from_user, bot.get_me()))
# bot.send_message(message.chat.id, "Welcome, {0.first_name}! What do you want?".format(message.from_user, bot.get_me()))


@bot.message_handler(commands=['doge'])
def ethereum(message):
	price = cg.get_price(ids='dogecoin', vs_currencies='usd')
	bot.send_message(message.chat.id, f'Doge  {price["dogecoin"]["usd"] }$')

@bot.message_handler(commands=['ltc'])
def ethereum(message):
	price = cg.get_price(ids='litecoin', vs_currencies='usd')
	bot.send_message(message.chat.id, f'Litecoin  {price["litecoin"]["usd"] }$')


def collect_data():
    s = requests.Session()
    response = s.get(url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cftx-token%2Ccardano%2Cthe-graph%2Cnear%2Cpolkadot%2Cavalanche-2%2Cdogecoin%2Cethereum%2Cterra-luna%2Clitecoin%2Cmatic-network%2Csolana%2Cbinancecoin%2Cuniswap&vs_currencies=usd")
    data = response.json()
    result_data = sorted(data.items(), key=lambda i: i[1]['usd'], reverse=True)
    f = open('file2.txt', 'w')
    for i in result_data:
        line = ' '.join(str(x) for x in i)
        f.write(line + '\n')
    # sleep(delay)
    f.close()





@bot.message_handler(commands=['main'])
def pop(message):
    bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
    time.sleep(10)
    collect_data()
    myfile = open('file2.txt', 'r')
    data = myfile.read()
    data = data.replace("{", " ~").replace("'","").replace("}","$").replace("usd","").replace(":", " ")
    # space = list()
    # for i in range(0, len(data)):
    #     if data[i] in "\n":
    #         count = data.find('\n', i)
    #         space.append(count)
    bot.send_message(message.chat.id, data)




@bot.message_handler(commands=['status'])
def bot_message(message):
	bot.send_message(message.chat.id, "I'm working" )



@bot.message_handler(commands=['creator'])
def callbacks(message):
    bot.send_message(message.chat.id, "Write a message to the creator of the bot: \n{link}!".format(link=link))


@bot.message_handler(func=lambda message: True)
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand, try with /help")

bot.polling(none_stop=True, interval=0)






