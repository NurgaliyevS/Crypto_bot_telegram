import telebot
import time
import json
import requests
from pycoingecko import CoinGeckoAPI
from telebot import types
import sqlite3
import time
import crypto_price



cg = CoinGeckoAPI()

# global variables
api_key = 'your_api_key'


link = "https://t.me/yatemez"


bot = telebot.TeleBot('your_token_api')

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
    else:
        bot.send_message(message.chat.id, "Welcome, {0.first_name}!".format(message.from_user, bot.get_me()))


@bot.message_handler(commands=['delete'])
def delete(message):
    # connect DB and create table
    connect = sqlite3.connect('customer.db')
    cursor = connect.cursor()
    # check id in fields
    people_id = message.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
    connect.commit()
    bot.send_message(message.chat.id, "You have been deleted from database, {0.first_name}!".format(message.from_user, bot.get_me()))


@bot.message_handler(commands=['main'])
def main(message):
	bot.send_message(message.chat.id, "I'm working" )


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


def pop():
    # time.sleep(10)
    collect_data()
    myfile = open('file2.txt', 'r')
    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
    coins = {}
    with open("file2.txt") as file:
        for row in file:
            row = row.split()
            name = row[1][row[1].find("'") + 1:row[1].find(":") - 1]
            price = row[2][:row[2].find('}')]
            coins[row[0]] = {name: float(price)}
            # print(name, price)

    print(coins)
# print(pop())


@bot.message_handler(commands=['alert'])
def alert (message):
    #### /alert
    #### пользователь вводит сначала команду alert
    msg = bot.send_message(message.chat.id, "Чтобы поставить оповещение "
                                      "\nНапишите название крипты и цену"
                                      "\nНапример: Bitcoin 50000")
    bot.register_next_step_handler(msg, add_record_db)



@bot.message_handler(content_types=['continue'])
def add_record_db(message):
    #### ПОТОМ ЧЕЛОВЕК ПИШЕТ ОТДЕЛЬНО В ЧАТЕ
    #### НАПРИМЕР
    #### BITCOIN 25000
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
            customer_coin = [message.chat.id, user[0], price, user_up_or_down_price]
            cursor.execute("INSERT INTO CUSTOMER_COIN (note_id, id_customer, id_coin, price_coin, up_or_down_price) VALUES(NULL,?,?, ?, ?);", customer_coin)
            connect.commit()
            bot.register_next_step_handler(bot.send_message(message.chat.id, "Ваша монета найдена."
                                                            f"\n{coin.upper()[0] + coin[1:-1] + coin[-1]}. \nСтавим оповещение."
                                                    "\nWrite to me a word."), make_a_new_alert)
            connect.commit()
        else:
            msg = bot.send_message(message.chat.id, "I don't get it"
                                                    "\nTry again, please"
                                                    "\nExample:"
                                                    "\nBitcoin 50000")
            bot.register_next_step_handler(msg, add_record_db)

    except:
        msg = bot.send_message(message.chat.id, "I don't get it"
                                                "\nTry again, please"
                                                "\nExample:"
                                                "\nBitcoin 50000")
        bot.register_next_step_handler(msg, add_record_db)


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
                            FOREIGN KEY(id_customer) REFERENCES CUSTOMER(id),
                            FOREIGN KEY(id_coin)REFERENCES COIN(id)
                            )""")
    connect.commit()




def insert_values_into_customer_coin():
    connect = sqlite3.connect('customer.db')
    cursor = connect.cursor()
    customer_coin = [11, 12, 123, 1]
    cursor.execute("INSERT INTO CUSTOMER_COIN (note_id, id_customer, id_coin, price_coin, up_or_down_price) VALUES(NULL,?,?, ?, ?);",
                   customer_coin)
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





@bot.message_handler(commands=['notification'])
def make_a_new_alert(message):
    bot.send_message(message.chat.id, "Do you want to continue?"
                                            "\nType: "
                                            "\n/alert"
                                            "\nIf you want to exit?"
                                            "\ntype: "
                                            "\n/main")


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

        # sqlite_select_query = """SELECT cc.note_id, cc.id_customer, cc.id_coin, cc.price_coin, c.customer_name, cn.coin_name from CUSTOMER_COIN cc, CUSTOMER c, Coin cn WHERE cc.id_coin """
        sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin
        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id """
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






bot.polling(none_stop=True, timeout=123)



