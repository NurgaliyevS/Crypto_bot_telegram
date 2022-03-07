import requests
import time
import sqlite3
import crypto_price
import os
import settings



bot_token = os.getenv('bot')


# fn to send_message through telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)



def main():
    sqlite_connection = sqlite3.connect('customer.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
    FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
    WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
    cursor.execute(sqlite_select_query)
    user_info = cursor.fetchall()
    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
    cursor.close()
    print(user_info)
    while True:
        for i in range(len(user_info)):
            print(i)
            if user_info[i][2] == 'bitcoin' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_btc_price() > user_info[i][3]:
                    print('yes')
                    send_message(chat_id=user_info[i][4],
                    msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                        f"lower than the current price {crypto_price.check_btc_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'bitcoin' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_btc_price() < user_info[i][3]:
                    print('yes')
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_btc_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1 WHERE note_id = {id}""")
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'ethereum' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_eth_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                    msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                        f"lower than the current price {crypto_price.check_eth_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'ethereum' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_eth_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                    msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                    f"higher than the current price: {crypto_price.check_eth_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'binancecoin' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_bnb_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_bnb_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'binancecoin' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_bnb_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_bnb_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'litecoin' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_litecoin_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_litecoin_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'litecoin' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_litecoin_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_litecoin_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'solana' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_solana_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_solana_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'solana' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_solana_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_solana_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'avalanche' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_avalanche_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_avalanche_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'avalanche' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_avalanche_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_avalanche_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'terra-luna' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.ccheck_terra_luna_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_terra_luna_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'terra-luna' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_terra_luna_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_terra_luna_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'ftx-token' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_ftx_token_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_ftx_token_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'ftx-token' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_ftx_token_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_ftx_token_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'polkadot' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_polkadot_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_polkadot_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'polkadot' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_polkadot_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_polkadot_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'near' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_near_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_near_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'near' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_near_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_polkadot_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'uniswap' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_uniswap_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_uniswap_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'uniswap' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_uniswap_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_uniswap_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'matic-network' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_polygon_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_polygon_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'matic-network' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_polygon_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_polygon_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'cardano' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_ada_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_ada_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    # id_customer = {user_info[i][4]}
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'cardano' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_ada_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_ada_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    # id_customer = {user_info[i][4]}
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'the-graph' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_the_graph_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_the_graph_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    # print(i)
                    # id_customer = {user_info[i][4]}
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'the-graph' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_the_graph_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_the_graph_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'dogecoin' and user_info[i][5] == 1 and user_info[i][6] == 0:
                if crypto_price.check_dogecoin_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                    msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                    f"lower than the current price {crypto_price.check_dogecoin_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)

            if user_info[i][2] == 'dogecoin' and user_info[i][5] == 0 and user_info[i][6] == 0:
                if crypto_price.check_dogecoin_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_dogecoin_price()}")
                    connect = sqlite3.connect('customer.db')
                    cursor = connect.cursor()
                    id = user_info[i][0]
                    cursor.execute(f"""UPDATE CUSTOMER_COIN SET notified_or_not = 1  WHERE note_id = {id} """)
                    connect.commit()
                    cursor.close()

                    sqlite_connection = sqlite3.connect('customer.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price, c_c.notified_or_not
                        FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
                        WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id"""
                    cursor.execute(sqlite_select_query)
                    user_info = cursor.fetchall()
                    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
                    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
                    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
                    cursor.close()
                    print(user_info)
        time.sleep(100)


# fancy way to activate the main() function
if __name__ == '__main__':
    main()
