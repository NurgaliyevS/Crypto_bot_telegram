import telebot
from pycoingecko import CoinGeckoAPI
from collections import OrderedDict
import requests
import json
from time import sleep
import time
import sqlite3
import crypto_price
import os
import settings


link = "https://t.me/yatemez"



api_key = telebot.TeleBot(os.getenv('api_key'))
bot = telebot.TeleBot(os.getenv('bot'))



cg = CoinGeckoAPI()


link = "https://t.me/yatemez"


@bot.message_handler(commands=['btc'])
def bitcoin(message):
	price = cg.get_price(ids='bitcoin', vs_currencies='usd')
	bot.send_message(message.chat.id, f'Bitcoin  {price["bitcoin"]["usd"] }$')


@bot.message_handler(commands=['eth'])
def ethereum(message):
	price = cg.get_price(ids='ethereum', vs_currencies='usd')
	bot.send_message(message.chat.id, f'Ethereum  {price["ethereum"]["usd"] }$')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, """\
You can only set alerts for these coins:

Bitcoin

Ethereum

Binancecoin

Litecoin

Solana

Avalanche-2

Terra-luna

FTX-Token

Polkadot

Uniswap

NEAR

Matic-network

Cardano

The-Graph

Dogecoin

If you want to set alerts on coins that are not in the list, 
write to the creator, I will try to add them.
/creator
""")


@bot.message_handler(commands=['start'])
def start(message):
    # connect DB and create table
    connect = sqlite3.connect('customer.db')
    cursor = connect.cursor()
    username = message.from_user.first_name
    connect.commit()

    # check id in fields
    people_id = message.chat.id
    ## так как people_id это форматирование, поэтому перед SELECT знак f
    cursor.execute(f"SELECT id FROM CUSTOMER WHERE id = {people_id}")
    ## в переменной data = все поля в котором есть мой ID
    data = cursor.fetchone()
    if data is None:
        # add values in fields
        ## Один ?, так как только добавляется одно поле ID
        customer_list = [message.chat.id, 1488, username]
        cursor.execute("INSERT INTO CUSTOMER (id, id_group, customer_name) VALUES(?, ?, ?);", customer_list)
        connect.commit()
        bot.send_message(message.chat.id, "You have been added into database.".format(message.from_user, bot.get_me()))
    bot.send_message(message.chat.id, """\
Hi there, {0.first_name}, I am Alexa bot v3.
I am here to help you! I can send you crypto price.
Just type or click on commands:

/start - Let's start!

/help - Need help? 

/main - Get Current price of the cryptocurrency

/alert - Сreate a cryptocurrency notification

/record - Get a list of created records

/delete - Delete notification

/btc - Get Bitcoin price

/eth - Get Ethereum price

/doge - Get Dogecoin price

/ltc - Get Litecoin price

/creator - Write to the creator
""".format(message.from_user, bot.get_me()))


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
    bot.send_message(message.chat.id, data)




@bot.message_handler(commands=['status'])
def bot_message(message):
	bot.send_message(message.chat.id, "I'm working" )


@bot.message_handler(commands=['creator'])
def callbacks(message):
    bot.send_message(message.chat.id, "Write a message to the creator of the bot: \n{link}!".format(link=link))


def help_crypto_list_with_price(message):
    msg = bot.send_message(message.chat.id, "Please, wait. I receive an information.")
    bot.send_message(message.chat.id, f"""\
You can only set alerts for these coins:

Bitcoin {crypto_price.check_btc_price()}$

Ethereum {crypto_price.check_eth_price()}$

Binancecoin {crypto_price.check_bnb_price()}$

Litecoin {crypto_price.check_litecoin_price()}

Solana {crypto_price.check_solana_price()}$

Avalanche-2 {crypto_price.check_avalanche_price()}$

Terra-luna {crypto_price.check_terra_luna_price()}$

FTX-Token {crypto_price.check_ftx_token_price()}$

Polkadot {crypto_price.check_polkadot_price()}$

Uniswap {crypto_price.check_uniswap_price()}$

NEAR {crypto_price.check_near_price()}$

Matic-network {crypto_price.check_polygon_price()}$

Cardano {crypto_price.check_ada_price()}$
 
The-Graph {crypto_price.check_the_graph_price()}$

Dogecoin {crypto_price.check_dogecoin_price()}$
""")


def help_crypto_list(message):
    # msg = bot.send_message(message.chat.id, "Please, wait. I receive an information.")
    bot.send_message(message.chat.id, f"""\
You can only set alerts for these coins:

Bitcoin 

Ethereum 

Binancecoin 

Litecoin 

Solana

Avalanche-2 

Terra-luna

FTX-Token 

Polkadot 

Uniswap 

NEAR 

Matic-network 

Cardano 

The-Graph 

Dogecoin 
""")


@bot.message_handler(commands=['alert'])
def alert (message):
    #### /alert
    #### пользователь вводит сначала команду alert
    help_crypto_list(message)
    msg = bot.send_message(message.chat.id, "To set an alert."
                                        "\n"
                                      "\nWrite the name of the"
                                      "\ncryptocurrency and the price."
                                      "\n"
                                      "\nExample: "
                                      "\nBitcoin 50000"
                                            "\n"
                                            "\nIf you want to exit?"
                                            "\n/start")
    bot.register_next_step_handler(msg, add_record_db)


def add_record_db(message):
    #### ПОТОМ ЧЕЛОВЕК ПИШЕТ ОТДЕЛЬНО В ЧАТЕ
    #### НАПРИМЕР
    #### BITCOIN 25000
    if message.text == "/start":
        return start(message)

    crypto_coin = ['bitcoin', 'ethereum', 'binancecoin',
     'litecoin', 'solana', 'avalanche-2',
     'terra-luna', 'ftx-token',
     'polkadot', 'near', 'uniswap',
     'matic-network', 'cardano',
     'the-graph', 'dogecoin']
    user_coin = message.text
    user_coin = user_coin.lower()
    user_coin = user_coin.split()
    try:
        coin, price = user_coin[0], user_coin[1]
        if user_coin[1].isdigit() or float(user_coin[1]) and user_coin[0] in crypto_coin:
            print('yes')
            connect = sqlite3.connect('customer.db')
            cursor = connect.cursor()
            ## так как people_id это форматирование, поэтому перед SELECT знак f
            cursor.execute("SELECT id, coin_name FROM COIN WHERE coin_name = ?", (coin,))
            ## в переменной data = выводит поле id, coin_name. Пользователя, который написал команду /alert
            data = cursor.fetchone()
            user = []
            for i in data:
                user.append(i)
            connect.commit()
            user_up_or_down_price = int()
            user[1] = str(user[1])
            user_coin[1] = float(user_coin[1])
            if user_coin[1] >= crypto_price.check_price(user[1]):
                user_up_or_down_price = 1
            else:
                user_up_or_down_price = 0
            connect = sqlite3.connect('customer.db')
            cursor = connect.cursor()
            # connect DB and create table
            customer_coin = [message.chat.id, user[0], price, user_up_or_down_price, 0]
            cursor.execute("INSERT INTO CUSTOMER_COIN (note_id, id_customer, id_coin, price_coin, up_or_down_price, notified_or_not) VALUES(NULL,?,?, ?, ?, ?);", customer_coin)
            connect.commit()
            bot.send_message(message.chat.id, "Ваша монета найдена."
                                                            f"\n{coin.upper()[0] + coin[1:-1] + coin[-1]}. \nСтавим оповещение.")
            make_a_new_alert(message)
        else:
            msg = bot.send_message(message.chat.id, "I don't get it"
                                                    "\nTry again, please"
                                                    "\nExample:"
                                                    "\nBitcoin 50000")
            bot.register_next_step_handler(msg, add_record_db)

    except:
        msg = bot.send_message(message.chat.id, "I don't get it."
                                                "\nTry again, please."
                                                "\nExample:"
                                                "\nBitcoin 50000.")
        bot.register_next_step_handler(msg, add_record_db)


def make_a_new_alert(message):
    bot.send_message(message.chat.id, "Do you want to continue?"
                                            "\n/alert"
                                            "\nIf you want to exit?"
                                            "\n/start")


def create_db():
    connect = sqlite3.connect('customer.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS SGROUP (
                        id INTEGER PRIMARY KEY,
                        group_name VARCHAR(40)
                        )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS CUSTOMER (
                            id INTEGER PRIMARY KEY,
                            id_group INTEGER,
                            customer_name VARCHAR (40),
                            FOREIGN KEY (id_group) REFERENCES SGROUP (id)
                            )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS COIN (
                            id INTEGER PRIMARY KEY,
                            coin_name VARCHAR (40)
                            )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS CUSTOMER_COIN (
                            note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_customer INTEGER,
                            id_coin INTEGER,
                            price_coin INTEGER,
                            up_or_down_price INTEGER NOT NULL CHECK(up_or_down_price in (0,1)),
                            notified_or_not INTEGER NOT NULL CHECK(notified_or_not in (0,1)),
                            FOREIGN KEY(id_customer) REFERENCES CUSTOMER(id),
                            FOREIGN KEY(id_coin)REFERENCES COIN(id)
                            )""")
    connect.commit()




def constant_db():
    connect = sqlite3.connect('customer.db')
    cursor = connect.cursor()
    cursor.executescript("INSERT INTO SGROUP (id, group_name) VALUES(1488, 'free');"
                    "INSERT INTO SGROUP (id, group_name) VALUES(1337, 'paid');")
    cursor.executescript("INSERT INTO COIN (id, coin_name) VALUES(1, 'bitcoin');"
                   "INSERT INTO COIN (id, coin_name) VALUES(2, 'ethereum');"
                   "INSERT INTO COIN (id, coin_name) VALUES(3, 'binancecoin');"
                   "INSERT INTO COIN (id, coin_name) VALUES(4, 'litecoin');"
                   "INSERT INTO COIN (id, coin_name) VALUES(5, 'solana');"
                   "INSERT INTO COIN (id, coin_name) VALUES(6, 'avalanche');"
                   "INSERT INTO COIN (id, coin_name) VALUES(7, 'terra-luna');"
                   "INSERT INTO COIN (id, coin_name) VALUES(8, 'ftx-token');"
                   "INSERT INTO COIN (id, coin_name) VALUES(9, 'polkadot');"
                   "INSERT INTO COIN (id, coin_name) VALUES(10, 'uniswap');"
                   "INSERT INTO COIN (id, coin_name) VALUES(11, 'near');"
                   "INSERT INTO COIN (id, coin_name) VALUES(12, 'matic-network');"
                   "INSERT INTO COIN (id, coin_name) VALUES(13, 'cardano');"
                   "INSERT INTO COIN (id, coin_name) VALUES(14, 'the-graph');"
                   "INSERT INTO COIN (id, coin_name) VALUES(15, 'dogecoin');")

    connect.commit()


def update_constant_db():
    connect = sqlite3.connect('customer.db')
    cursor = connect.cursor()
    cursor.execute("""UPDATE COIN SET id = 16, coin_name = Fantom
    """)
    connect.commit()
    cursor.close
    connect.close()


def new_constant_db():
    connect = sqlite3.connect('customer.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO COIN (id, coin_name) VALUES (16, 'Fantom')")
    connect.commit()
    cursor.close
    connect.close()


#### ЧТЕНИЕ ВСЕГО ЧТО ЕСТЬ В БАЗЕ ДАННЫХ
#### НЕОБХОДИМО БРАТЬ ОБРАБОТАТЬ ЭТИ ДАННЫЕ
@bot.message_handler(commands=['record'])
def read_sqlite_table(message):
    try:
        bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
        time.sleep(10)
        sqlite_connection = sqlite3.connect('customer.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        people_id = message.chat.id
        # people_id = message.chat.id
        # ## так как people_id это форматирование, поэтому перед SELECT знак f
        # cursor.execute(f"SELECT id FROM CUSTOMER WHERE id = {people_id}")
        # sqlite_select_query = """SELECT cc.note_id, cc.id_customer, cc.id_coin, cc.price_coin, c.customer_name, cn.coin_name from CUSTOMER_COIN cc, CUSTOMER c, Coin cn WHERE cc.id_coin """
        sqlite_select_query = f"""SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin
        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id and cm.id = {people_id}"""
        cursor.execute(sqlite_select_query)
        text = cursor.fetchall()
        print("Всего строк: ", len(text))
        # print("Вывод каждой строки")
        a = []
        #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
        #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
        #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
        for rows in text:
            a.append(rows)
        c = list()
        for i in range(len(a)):
            c.append(a[i])
        c = str(c)
        c = c.replace(',',"").replace('(', " ", 1).replace(')',"$",1).replace('(',"\n").replace(")","$").replace("'", "").replace("["," ").replace("]","")
        print(c)
        cursor.close()
        bot.send_message(message.chat.id, f'{c}')

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")



@bot.message_handler(commands=['delete'])
def delete(message):
    read_sqlite_table(message)
    msg = bot.send_message(message.chat.id, "Choose a note number which you would like to delete, {0.first_name}!".format(message.from_user, bot.get_me()))
    bot.register_next_step_handler(msg, delete_record_from_db)



def delete_record_from_db(message):
    delete_note_id = message.text
    try:
        if delete_note_id.isdigit():
            print('YES')
            connect = sqlite3.connect('customer.db')
            cursor = connect.cursor()
            ## так как people_id это форматирование, поэтому перед SELECT знак f
            cursor.execute(f"""DELETE from CUSTOMER_COIN where note_id = {delete_note_id}""")
            connect.commit()
            cursor.close()
            bot.send_message(message.chat.id, "Your note has been deleted successfully")
            read_sqlite_table(message)
        else:
            msg = bot.send_message(message.chat.id, "Try another one:bot.register_next_step_handler(msg, delete_record_from_db) ")
            bot.register_next_step_handler(msg, delete_record_from_db)
    except:
        msg = bot.send_message(message.chat.id, "Try another one: ")
        bot.register_next_step_handler(msg, delete_record_from_db)




# @bot.message_handler(func=lambda message: True)
# def command_default(m):
#     # this is the standard reply to a normal message
#     bot.send_message(m.chat.id, "I don't understand, try with /help")
#


bot.polling(none_stop=True, timeout=123)








