import numpy
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
import account_setings
import pandas as pd
import CurrencyPlot

link = "https://t.me/yatemez"

api_key = telebot.TeleBot(os.getenv('api_key'))
bot = telebot.TeleBot(os.getenv('bot'))

cg = CoinGeckoAPI()

link = "https://t.me/yatemez"

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, """\
You can set alert for 250 top coins. 
/alert

To find information for certain cryptocurrency write. 
/find

To get graph for specific coin write.
/graph

/creator - Write to the creator if you find a bug.

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
    bot.send_message(message.chat.id, """\
Hi there, {0.first_name}, I am Alexa bot v3.
I am here to help you! I can send you crypto price.
Just type or click on commands:

/start - Let's start!

/help - Need help? 

/main - Get сurrent prices for my favorite cryptocurrencies

/find - Get information for specific cryptocurrency

/alert - Сreate a cryptocurrency notification

/graph - Get graph for specific cryptocurrency

/record - Get a list of created records

/delete - Delete record from database

/records - Get information of 250 cryptocurrencies in txt file

/creator - Write to the creator
""".format(message.from_user, bot.get_me()))

def collect_data():
    s = requests.Session()
    response = s.get(url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cftx-token%2Ccardano%2Cthe-graph%2Cnear%2Cpolkadot%2Cavalanche-2%2Cdogecoin%2Cethereum%2Cterra-luna%2Clitecoin%2Cmatic-network%2Csolana%2Cbinancecoin%2Cuniswap&vs_currencies=usd")
    data = response.json()
    result_data = sorted(data.items(), key=lambda i: i[1]['usd'], reverse=True)
    f = open('file2.txt', 'w')
    for i in result_data:
        line = ' '.join(str(x) for x in i)
        f.write(line + '\n')
    f.close()
    result = []
    file = open('crypto_list_price.txt', 'w', encoding='utf-8')
    with open('file2.txt','r', encoding='utf-8') as f: 
        for line in f.readlines():
            result = line.strip()
            result_2 = result.split()
            try:
                if (result_2[2].isnumeric):
                    if (result_2[1].find('usd')):
                        if (result_2[0].isalpha):
                            result = result_2[0][0].upper() + result_2[0][1:] + ' ' + result_2[1] + ' ' + result_2[2]
                            file.write(''.join(result))
                            file.write('\n')
            except:
                print('bad')
        file.close()

@bot.message_handler(commands=['main'])
def pop(message):
    bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
    time.sleep(3)
    collect_data()
    myfile = open('crypto_list_price.txt', 'r')
    data = myfile.read()
    data = data.replace("{", '~').replace("'","").replace("}","$").replace("usd","").replace(":", "")
    bot.send_message(message.chat.id, data)
    bot.send_message(message.chat.id, "If you want to get prices"
                                      "\nof top 250 coins"
                                      "\n/records"
                                      "\nInformation for a certain cryptocurrency"
                                      "\n/find")

@bot.message_handler(commands=['status'])
def bot_message(message):
	bot.send_message(message.chat.id, "I'm working" )

@bot.message_handler(commands=['creator'])
def callbacks(message):
    bot.send_message(message.chat.id, "Write a message to the creator of the bot: \n{link}!".format(link=link))

@bot.message_handler(commands=['alert'])
def alert (message):
    #### /alert
    #### пользователь вводит сначала команду alert
    msg = bot.send_message(message.chat.id, "To set an alert."
                                        "\n"
                                      "\nWrite the name of the"
                                      "\ncryptocurrency and the price."
                                      "\nYou can put alerts on the top 250 coins."
                                      "\nExample: "
                                      "\nBitcoin 50000"
                                            "\n"
                                            "\nIf you want to exit?"
                                            "\n/start")
    bot.register_next_step_handler(msg, add_record_db)

def add_record_db(message):
    if message.text == "/start":
        return start(message)
    user_coin = message.text
    user_coin = user_coin.lower()
    user_coin = user_coin.split()
    crypto_coin = list_coins_2()
    try:
        coin, price = user_coin[0], user_coin[1]
        if user_coin[1].isdigit() or float(user_coin[1]) and user_coin[0] in crypto_coin:
            connect = sqlite3.connect('coins.db')
            cursor = connect.cursor()
            cursor.execute("SELECT cm.id, cm.market_cap_rank ,lower(cm.name), cm.current_price FROM Coins_Markets cm WHERE lower(cm.name) = '{}' or cm.id = '{}'".format(user_coin[0], user_coin[0]))
            data = cursor.fetchone()
            user = []
            for i in data:
                user.append(i)
            connect.commit()
            connect.close()
            user_up_or_down_price = int()
            user[1] = str(user[1])
            user_coin[1] = float(user_coin[1])
            if user_coin[1] >= crypto_price.check_crypto_price(user[2]):
                user_up_or_down_price = 1
            else:
                user_up_or_down_price = 0
            connect = sqlite3.connect('customer.db')
            cursor = connect.cursor()
            customer_coin = [message.chat.id, user[1], price, user_up_or_down_price, 0]
            cursor.execute("INSERT INTO CUSTOMER_COIN (note_id, id_customer, id_coin, price_coin, up_or_down_price, notified_or_not) VALUES(NULL, ?,?, ?, ?, ?);", customer_coin)
            connect.commit()
            bot.send_message(message.chat.id, "Your cryptocurrency has been found."
                                                            f"\n{coin.upper()[0] + coin[1:]}. \nMade record to the database."
                                                            "\nYou will receive an alert when your price matches the current one.")
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

def list_coins_2():
    sqlite_connection = sqlite3.connect('coins.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    sqlite_select_query = f"""SELECT cm.id, cm.name
    FROM Coins_Markets cm"""
    cursor.execute(sqlite_select_query)
    text = cursor.fetchall()
    cursor.close()
    text = str(text)
    result = text.replace("[", "").replace("(", "").replace("'","").replace(",","").replace(")","\n").replace("]","")
    return result

def make_a_new_alert(message):
    bot.send_message(message.chat.id, "Do you want to continue?"
                                            "\n/alert"
                                            "\nIf you want to exit?"
                                            "\n/start")

# @bot.message_handler(commands=['create_db'])
def create_db(message):
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
                            coin_name VARCHAR (65),
                            coin_market_id VARCHAR(65)
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
    bot.send_message(message.chat.id, "You database has been created.")

# @bot.message_handler(commands=['constant_db'])
def constant_db(message):
    connect = sqlite3.connect('coins.db')
    cursor = connect.cursor()
    data = cursor.execute("SELECT cm.market_cap_rank, lower(cm.name), cm.id FROM Coins_Markets cm")
    allCoins = []
    for value in data:
        allCoins.append(value)
    cursor.close()
    # print(allCoins)
    connect = sqlite3.connect('customer.db')
    cursor = connect.cursor()
    user = []
    for i in range(len(allCoins)):
        cursor.execute("INSERT INTO COIN (id, coin_name, coin_market_id) VALUES(?,?, ?);", allCoins[i])
        connect.commit()
    cursor.close()
    bot.send_message(message.chat.id, "You constants has been added to database.")

#### ЧТЕНИЕ ВСЕГО ЧТО ЕСТЬ В БАЗЕ ДАННЫХ
#### НЕОБХОДИМО БРАТЬ ОБРАБОТАТЬ ЭТИ ДАННЫЕ
@bot.message_handler(commands=['record'])
def read_sqlite_table(message):
    try:
        bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
        time.sleep(3)
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

@bot.message_handler(commands=['records'])
def get_100_coins_db(message):
    crypto_price.get_top_250_coins()
    try:
        bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
        sqlite_connection = sqlite3.connect('coins.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sqlite_select_query = f"""SELECT cm.market_cap_rank, cm.name, cm.current_price, cm.price_change_24h, cm.price_change_percentage_24h, cm.market_cap, cm.market_cap_change_percentage_24h, cm.max_supply, cm.circulating_supply, cm.high_24h, cm.low_24h
        FROM Coins_Markets cm"""
        cursor.execute(sqlite_select_query)
        text = cursor.fetchall()
        print("Всего строк: ", len(text))
        # print("Вывод каждой строки")
        a = []
        #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
        #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
        #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
        with open("crypto.txt", 'w') as f:
            for i in range(len(text)):
                if text[i][0]:
                    f.write('Market_Cap_Rank: ')
                    f.write(str(text[i][0]))
                    f.write('\n')
                if text[i][1]:
                    f.write('Coin: ')
                    f.write(str(text[i][1]))
                    f.write('\n')
                if text[i][2]:
                    f.write('Current_Price: ')
                    f.write(str(text[i][2]))
                    f.write('\n')
                if text[i][3]:
                    f.write('Price_Change_24h: ')
                    f.write(str(text[i][3]))
                    f.write('\n')
                if text[i][4]:
                    f.write('Price_Change_Percentage_24h: ')
                    f.write(str(text[i][4]))
                    f.write('\n')
                if text[i][5]:
                    numbers = "{:,}".format(text[i][5])
                    f.write('Market_Cap: ')
                    f.write(str(numbers))
                    f.write('\n')
                if text[i][6]:
                    f.write('Market_Cap_Change_Percentage_24h: ')
                    f.write(str(text[i][6]))
                    f.write('\n')
                if text[i][7]:
                    numbers = "{:,}".format(text[i][7])
                    f.write('Max_Supply: ')
                    f.write(str(numbers))
                    f.write('\n')
                if text[i][8]:
                    numbers = "{:,}".format(text[i][8])
                    f.write('Circulating_Supply: ')
                    f.write(str(numbers))
                    f.write('\n')
                if text[i][9]:
                    f.write('Price_High_24h: ')
                    f.write(str(text[i][9]))
                    f.write('\n')
                if text[i][10]:
                    f.write('Price_low_24h: ')
                    f.write(str(text[i][10]))
                    f.write('\n')
                f.write('\n')
            f.close()
        cursor.close()
        doc = open('crypto.txt', 'rb')
        bot.send_message(message.chat.id, "Sending...")
        bot.send_document(message.chat.id, doc)
        doc.close()
        
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

@bot.message_handler(commands=['graph'])
def crypto_graph(message):
    msg = bot.send_message(message.chat.id, "if you want to get a cryptocoin chart." 
                                            "\nWrite a coin name and days."
                                            "\nFor Example: " 
                                            "\nCardano 1"
                                            "\nBitcoin 365"
                                            "\nSecond paramets is days"
                                            "\nOnly supported 1, 7, 14, 30, 90, 180, 365"
                                            )
    bot.register_next_step_handler(msg, coin_plot)

def coin_plot(message):
    try:
        userCoin = message.text
        userCoin = userCoin.lower()
        userCoin = userCoin.split()
        print(userCoin)
        print(userCoin[0])
        print(userCoin[1])
        result = CurrencyPlot.get_exact_value_json(userCoin[0])
        if int(userCoin[1]) == 1:
            CurrencyPlot.paint_plot(userCoin[0], int(userCoin[1]))
            print('hello')
            usd = cg.get_price(ids='{}'.format(result), vs_currencies='usd')['{}'.format(result)]['usd']
            img = open('foo.png', 'rb')
            bot.send_photo(message.chat.id, img, caption='Price of the last {} day of {}\n'
                                                        'Current price {}$'.format(userCoin[1],userCoin[0][0].upper() + userCoin[0][1:], usd))
            img.close()
        else:
            CurrencyPlot.paint_plot(result, int(userCoin[1]))
            usd = cg.get_price(ids='{}'.format(result), vs_currencies='usd')['{}'.format(result)]['usd']
            img = open('foo.png', 'rb')
            bot.send_photo(message.chat.id, img, caption='Price of the last {} days of {}\n'
                                                        'Current price {}$'.format(userCoin[1],userCoin[0][0].upper() + userCoin[0][1:], usd))
            img.close()
    except:
        bot.send_message(message.chat.id, "I can't find crypto with this name"
        "\nCheck this file"
        "\n/list_coins"
        "\nCorrect names of coins"
        "\nThen, try again"
        "\n/graph")

@bot.message_handler(commands=['list_coins'])
def list_coins(message):
    bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
    sqlite_connection = sqlite3.connect('coins.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    sqlite_select_query = f"""SELECT cm.id
    FROM Coins_Markets cm"""
    cursor.execute(sqlite_select_query)
    text = cursor.fetchall()
    cursor.close()
    with open("name_coins.txt", 'w') as f:
        for line in text:
            line = str(line)
            # print(line[2].upper() + line[:2])
            line = line.replace("(", '').replace(")","").replace(",","").replace("'", "")
            f.write(line[0].upper() + line[1:])
            f.write('\n')
    f.close()
    doc = open('name_coins.txt', 'rb')
    bot.send_message(message.chat.id, "Sending...")
    bot.send_document(message.chat.id, doc)
    doc.close()

@bot.message_handler(commands=['find'])
def crypto_handler(message):
    msg = bot.send_message(message.chat.id, "if you want to find information on a specific crypto." 
                                            "\nWrite the name of the coin."
                                            "\nExample: Bitcoin.")
    bot.register_next_step_handler(msg, find_crypto)

def find_crypto(message):
    try:
        crypto_price.get_top_250_coins()
        user_coin = message.text
        user_coin = user_coin.lower()
        # coin_plot(user_coin.user_coin)
        print(user_coin)
        sqlite_connection = sqlite3.connect('coins.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        cursor.execute("SELECT cm.market_cap_rank,cm.id, lower(cm.name), cm.current_price, cm.price_change_24h, cm.price_change_percentage_24h, cm.market_cap, cm.market_cap_change_percentage_24h,cm.total_volume, cm.circulating_supply, cm.max_supply, cm.high_24h, cm.low_24h FROM Coins_Markets cm WHERE lower(cm.name) = '{}' or cm.id = '{}'".format(user_coin, user_coin))
        data = cursor.fetchone()
        user = []
        print(data)
        print('hey', data[10])
        for i in data:
            user.append(i)
        if user[10] is None:
            user[10] = 0
        sqlite_connection.commit()
        cursor.close()
        result = 'Market Cap Rank: {} \nName: {} \nPrice: {}$ \nPrice Change 24h: {}$ \nPrice Change 24h: {}% \nMarket Cap: {:,} \nMarket Cap 24h: {}% \nTotal Volume: {:,} \nCirculating Supply: {:,} \nMax suply: {:,} \nLow Price 24h: {}$ \nHigh price 24h: {}$'.format(user[0], user[2].capitalize(), user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10], user[12], user[11])
        bot.send_message(message.chat.id, result)
        result = CurrencyPlot.get_exact_value_json(user_coin)
        CurrencyPlot.paint_plot(user_coin, 1)
        print('hello')
        usd = cg.get_price(ids='{}'.format(result), vs_currencies='usd')['{}'.format(result)]['usd']
        img = open('foo.png', 'rb')
        bot.send_photo(message.chat.id, img, caption='Price of the last {} day of {}\n'
                                                    'Current price {}$'.format(1,result[0].upper() + result[1:], usd))
        img.close()

    except:
        bot.send_message(message.chat.id, "I can't find crypto with this name"
        "\nCheck this file"
        "\n/list_coins"
        "\nCorrect names of coins"
        "\nThen, try again"
        "\n/find")

bot.polling(none_stop=True, timeout=123)