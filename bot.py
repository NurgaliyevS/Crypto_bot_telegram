from binascii import crc32
from typing import Text
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
import settings
import psycopg2

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
    try:
        connection = psycopg2.connect(
                host = settings.host,
                database = settings.db_name_2,
                user = settings.user,
                password = settings.password,
                port = settings.port_id
            )
        # Call IT one Time That's it
        connection.autocommit = True
        with connection.cursor() as cursor:
            people_id = message.chat.id
            cursor.execute(f"SELECT id FROM customer WHERE id = {people_id}")
            data = cursor.fetchone()
            if data is None:
                # add values in fields
                ## Один ?, так как только добавляется одно поле ID
                postgres_insert_query = """INSERT INTO customer (id, id_group, customer_name)
                VALUES (%s, %s, %s);
                """
                record_to_insert = (people_id, 1488, message.from_user.first_name)
                cursor.execute(postgres_insert_query, record_to_insert)
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

    except:
            msg = bot.send_message(message.chat.id, "I don't get it."
                                                    "\nTry again, please."
                                                    "\nExample:"
                                                    "\nBitcoin 50000.")
            bot.register_next_step_handler(msg, add_record_db)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

# @bot.message_handler(commands=['groups'])
def create_groups(message):
    try:
        connection = psycopg2.connect(
                host = settings.host,
                database = settings.db_name_2,
                user = settings.user,
                password = settings.password,
                port = settings.port_id
            )
        # Call IT one Time That's it
        connection.autocommit = True
        with connection.cursor() as cursor:
            postgres_insert_query = """INSERT INTO sgroup (id, group_name)
                VALUES (%s, %s);
                """
            record_to_insert = (1377, 'paid')
            cursor.execute(postgres_insert_query, record_to_insert)
    except:
            msg = bot.send_message(message.chat.id, "I don't get it."
                                                    "\nTry again, please."
                                                    "\nExample:"
                                                    "\nBitcoin 50000.")
            bot.register_next_step_handler(msg, add_record_db)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


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
    if message.text == "/start":
        return start(message)
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
    coin = list()
    price = list()
    crypto_coin = list_coins_2()
    try:
        for i in user_coin:
            try: 
                float(i)
                price.append(i)
            except:        
                if i.isdigit():
                    price.append(i)
                else:
                    coin.append(i)
        coin = ' '.join([str(item) for item in coin])
        crypto_coin = list(crypto_coin)
        for coinsDb in crypto_coin:
            for coinDb in coinsDb:
                coinDb = str(coinDb)
                coinDb = coinDb.lower()
                if coinDb == coin:
                    print('YEEEES')
        try:
            userCoinId = indexUserCoin(coin)
            idUserCoin = 0
            for userCoin in userCoinId:
                for idCoinUser in userCoin:
                    idUserCoin += idCoinUser
            idUserCoin = int(idUserCoin)
            userPrice = ''
            for i in price:
                userPrice += i
            print(crypto_price.check_crypto_price(coin))
            print(type(crypto_price.check_crypto_price(coin)))
            if float(userPrice) >= crypto_price.check_crypto_price(coin):
                user_up_or_down_price = True
                notified_or_not = False
            else:
                user_up_or_down_price = False
                notified_or_not = False
            print('id_customer', message.chat.id, type(message.chat.id), 'id_coin', idUserCoin, type(idUserCoin) , 'price_coin', userPrice, type(int(userPrice)), 'up_or_down_price', user_up_or_down_price, type(user_up_or_down_price), 'notified_or_not', False, type(False) )
            connection = psycopg2.connect(
                host = settings.host,
                database = settings.db_name_2,
                user = settings.user,
                password = settings.password,
                port = settings.port_id
            )
            # Call IT one Time That's it
            connection.autocommit = True
            with connection.cursor() as cursor:
                postgres_insert_query = """INSERT INTO customer_coin (id_customer, id_coin, price_coin, up_or_down_price, notified_or_not)
                    VALUES (%s, %s, %s, %s, %s);
                    """
                record_to_insert = (message.chat.id, idUserCoin, int(userPrice), user_up_or_down_price, notified_or_not )
                cursor.execute(postgres_insert_query, record_to_insert)
                bot.send_message(message.chat.id, "Your cryptocurrency has been found."
                                                            f"\n{coin.upper()[0] + coin[1:]} {userPrice}$."
                                                            "\nMade record to the database."
                                                            "\nYou will receive an alert when"
                                                            "\nyour price matches the current one.")
                make_a_new_alert(message)
        except Exception as _ex:
            msg = ("[INFO] Error while working with PostgreSQL", _ex)
            bot.send_message(message.chat.id, msg)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        
    except:
        msg = bot.send_message(message.chat.id, "I don't get it."
                                                "\nTry again, please."
                                                "\nExample:"
                                                "\nBitcoin 50000."
                                                "\nIf you want to return."
                                                "\n/start")
        bot.register_next_step_handler(msg, add_record_db)

def make_a_new_alert(message):
    bot.send_message(message.chat.id, "Do you want to continue?"
                                        "\n/alert"
                                        "\nIf you want to exit?"
                                        "\n/start")

def list_coins_2():
    try:
        connection = psycopg2.connect(
            host = settings.host,
            database = settings.db_name,
            user = settings.user,
            password = settings.password,
            port = settings.port_id
        )
        # Call IT one Time That's it
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, name
	            FROM coins_info;
                """)
            data = cursor.fetchall()
            coin_id = list()
            coin_name = list()
            for a, b in data:
                coin_id.append(a)
                coin_name.append(b)
            return coin_id, coin_name

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

def indexUserCoin(coin):
    try:
        connection = psycopg2.connect(
            host = settings.host,
            database = settings.db_name,
            user = settings.user,
            password = settings.password,
            port = settings.port_id
        )
        # Call IT one Time That's it
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT market_cap_rank
	            FROM coins_info
                WHERE lower(name) = %s OR id = %s ;
                """, [coin, coin ])
            data = cursor.fetchall()
            coin_id = list()
            for a in data:
                coin_id.append(a)
            return coin_id

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

# @bot.message_handler(commands=['coins'])
def constant_db(message):
    try:
        connection = psycopg2.connect(
            host = settings.host,
            database = settings.db_name,
            user = settings.user,
            password = settings.password,
            port = settings.port_id
        )
        # Call IT one Time That's it
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT id
	            FROM coins_info;
                """)
            data = cursor.fetchall()
            coin_id = list()
            for a in data:
                coin_id.append(a)
        try:
            connection = psycopg2.connect(
                host = settings.host,
                database = settings.db_name,
                user = settings.user,
                password = settings.password,
                port = settings.port_id
            )
            # Call IT one Time That's it
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT name
                    FROM coins_info;
                    """)
                data = cursor.fetchall()
                coin_name = list()
                for b in data:
                    coin_name.append(b)
            try:
                connection = psycopg2.connect(
                    host = settings.host,
                    database = settings.db_name_2,
                    user = settings.user,
                    password = settings.password,
                    port = settings.port_id
                )
                connection.autocommit = True
                with connection.cursor() as cursor:
                    # ALTER SEQUENCE coin_id_seq RESTART WITH 1;
                    # Обнулить smallserial or serial
                    for i in range(len(coin_name)):
                        postgres_insert_query = """INSERT INTO coin (coin_name, coin_market_id)
                            VALUES (%s, %s);
                            """
                        record_to_insert = (coin_name[i], coin_id[i])
                        cursor.execute(postgres_insert_query, record_to_insert)
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")                

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

@bot.message_handler(commands=['record'])
def read_sqlite_table(message):
    try:
        bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
        time.sleep(3)
        people_id = message.chat.id
        connection = psycopg2.connect(
                host = settings.host,
                database = settings.db_name_2,
                user = settings.user,
                password = settings.password,
                port = settings.port_id
            )
            # Call IT one Time That's it
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin
        FROM customer_coin c_c, customer cm, coin c
        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id and cm.id = %s
        ORDER BY c_c.note_id ASC""", [people_id])
            text = cursor.fetchall()
            if text == []:
                msg = bot.send_message(message.chat.id, "You haven't got created records yet."
                "\nRedirect to the alert function."
                "\nWrite if you want to make a new alert."
                "\nyes"
                "\nIf you want to return."
                "\n/start")
                bot.register_next_step_handler(msg, alert)
            else:
                a = []
                for rows in text:
                    a.append(rows)
                c = list()
                for i in range(len(a)):
                    c.append(a[i])
                c = str(c)
                c = c.replace(',',"").replace('(', " ", 1).replace(')',"$",1).replace('(',"\n").replace(")","$").replace("'", "").replace("["," ").replace("]","")
                print(c, 'HEEEYY MAN')
                cursor.close()
                bot.send_message(message.chat.id, f'{c}')
                
    except Exception as _ex:
            bot.send_message(message.chat.id, "[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

def read_records_table(person_id):
    try:
        # time.sleep(3)
        connection = psycopg2.connect(
                host = settings.host,
                database = settings.db_name_2,
                user = settings.user,
                password = settings.password,
                port = settings.port_id
            )
            # Call IT one Time That's it
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT c_c.note_id
        FROM customer_coin c_c, customer cm, coin c
        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id and cm.id = %s""", [person_id])
            data = cursor.fetchall()
            record_idDb = list()
            for a in data:
                record_idDb.append(a)
            record_id = ''.join([str(item) for item in record_idDb])
            record_id = record_id.replace('(', '').replace(')','').replace(',', ' ')
            record_id = record_id.split()
            return record_id
                
    except:
            bot.send_message(person_id, "No such record exists")
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

@bot.message_handler(commands=['delete'])
def delete(message):
    result = read_sqlite_table(message)
    if result is None:
        print('not good Man')
    else:
        msg = bot.send_message(message.chat.id, "Choose a note number which you would like to delete, {0.first_name}!".format(message.from_user, bot.get_me()))
        bot.register_next_step_handler(msg, delete_record_from_db)

def delete_record_from_db(message):
    delete_note_id = message.text
    result = read_records_table(message.chat.id)
    try:
        for i in result:
            if i == delete_note_id:
                print('hello')
                if delete_note_id.isdigit():
                    try:
                        connection = psycopg2.connect(
                            host = settings.host,
                            database = settings.db_name_2,
                            user = settings.user,
                            password = settings.password,
                            port = settings.port_id
                        )
                        # Call IT one Time That's it
                        connection.autocommit = True
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """DELETE from CUSTOMER_COIN where note_id = %s""", [delete_note_id])
                        bot.send_message(message.chat.id, "Your note has been deleted successfully")
                        read_sqlite_table(message)
    
                    except Exception as _ex:
                        bot.send_message(message.chat.id, "[INFO] Error while working with PostgreSQL", _ex)
                    finally:
                        if connection:
                            connection.close()
                            print("[INFO] PostgreSQL connection closed")
                else:
                    msg = bot.send_message(message.chat.id, "No such record exists"
                    "\nTry again.")
                    bot.register_next_step_handler(msg, delete_record_from_db)
            else:
                msg = bot.send_message(message.chat.id, "No such record exists"
                "\nTry again.")
                bot.register_next_step_handler(msg, delete_record_from_db)    
    except:
        msg = bot.send_message(message.chat.id, "No such record exists"
        "\nTry again.")
        bot.register_next_step_handler(msg, delete_record_from_db)    

@bot.message_handler(commands=['records'])
def get_100_coins_db(message):
    crypto_price.get_coins_api_postgres()
    try:
        bot.send_message(message.chat.id, 'Please, wait. I receive an information.')
        connection = psycopg2.connect(
                        host = settings.host,
                        database = settings.db_name,
                        user = settings.user,
                        password = settings.password,
                        port = settings.port_id
                    )
                    # Call IT one Time That's it
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT cm.market_cap_rank, cm.name, cm.current_price, cm.price_change_24h, cm.price_change_percentage_24h, cm.market_cap, cm.market_cap_change_percentage_24h, cm.max_supply, cm.circulating_supply, cm.high_24h, cm.low_24h
            FROM coins_info cm
            """)
            text = cursor.fetchall()
            print("Всего строк: ", len(text))
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
    except:
            bot.send_message(message.chat.id, "I can't do it right now.")
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

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
    try:
        connection = psycopg2.connect(
                        host = settings.host,
                        database = settings.db_name,
                        user = settings.user,
                        password = settings.password,
                        port = settings.port_id
                    )
                    # Call IT one Time That's it
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("""SELECT cm.id, cm.name
                            FROM coins_info cm""")
            data = cursor.fetchall()
            with open("name_coins.txt", 'w') as f:
                for a, b in data:
                    f.write('ID: ')
                    f.write(a.capitalize())
                    f.write('\n')
                    f.write('Name: ')
                    f.write(b.capitalize())
                    f.write('\n')
                    f.write('\n')
                f.close()
                doc = open('name_coins.txt', 'rb')
                bot.send_message(message.chat.id, "Sending...")
                bot.send_document(message.chat.id, doc)
                doc.close()
    except Exception as _ex:
        msg = ("[INFO] Error while working with PostgreSQL", _ex)
        bot.send_message(message.chat.id, msg)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

@bot.message_handler(commands=['find'])
def crypto_handler(message):
    msg = bot.send_message(message.chat.id, "if you want to find information on a specific crypto." 
                                            "\nWrite the name of the coin."
                                            "\nExample: Bitcoin.")
    bot.register_next_step_handler(msg, find_crypto)

def find_crypto(message):
    try:
        crypto_price.get_coins_api_postgres()
        user_coin = message.text
        user_coin = user_coin.lower()
        # coin_plot(user_coin.user_coin)
        print(user_coin)
        connection = psycopg2.connect(
                        host = settings.host,
                        database = settings.db_name,
                        user = settings.user,
                        password = settings.password,
                        port = settings.port_id
                    )
                    # Call IT one Time That's it
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT cm.market_cap_rank,cm.id, lower(cm.name), cm.current_price, cm.price_change_24h, cm.price_change_percentage_24h, cm.market_cap, cm.market_cap_change_percentage_24h,cm.total_volume, cm.circulating_supply, cm.max_supply, cm.high_24h, cm.low_24h
            FROM coins_info cm 
            WHERE lower(cm.name) = %s or cm.id = %s
            """, [user_coin, user_coin])
            data = cursor.fetchone()
            user = []
            print(data)
            print('hey', data[10])
            for i in data:
                user.append(i)
            if user[10] is None:
                user[10] = 0
            result = 'Market Cap Rank: {} \nName: {} \nPrice: {}$ \nPrice Change 24h: {}$ \nPrice Change 24h: {}% \nMarket Cap: {:,} \nMarket Cap 24h: {}% \nTotal Volume: {:,} \nCirculating Supply: {:,} \nMax suply: {:,} \nLow Price 24h: {}$ \nHigh price 24h: {}$'.format(user[0], user[2].capitalize(), user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10], user[12], user[11])
            bot.send_message(message.chat.id, result)
            result = CurrencyPlot.get_exact_value_json(user_coin)
            CurrencyPlot.paint_plot(user_coin, 1)
            print('hello')
            usd = cg.get_price(ids='{}'.format(result), vs_currencies='usd')['{}'.format(result)]['usd']
            img = open('foo.png', 'rb')
            bot.send_photo(message.chat.id, img, caption='Price of the last {} day of {}\n'
                                                        'Current price {}$'.format(1,user[2].capitalize(), usd))
            img.close()

    except:
        bot.send_message(message.chat.id, "I can't find crypto with this name"
        "\nCheck this file"
        "\n/list_coins"
        "\nCorrect names of coins"
        "\nThen, try again"
        "\n/find")

# bot.polling(none_stop=True, timeout=123)
while True:
    try:
        bot.polling(none_stop=True, timeout=123)
    except Exception as e:
        # logger.error(e)  # или просто print(e) если у вас логгера нет,
        print(e)
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)