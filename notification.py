import requests
import time
import sqlite3
import crypto_price
import os
import account_setings
import psycopg2
import settings

bot_token = os.getenv('bot_2')

# fn to send_message through telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)

def main():
        while True:
            try: 
                connection = psycopg2.connect(
                    host = settings.host,
                    database = settings.db_name_2,
                    user = settings.user,
                    password = settings.password,
                    port = settings.port_id)
                connection.autocommit = True
                with connection.cursor() as cursor:
                    cursor.execute(
                    """
                    SELECT c_c.note_id, cm.customer_name, c.coin_name, c.coin_market_id ,c_c.price_coin, cm.id, c_c.up_or_down_price, c_c.notified_or_not
                    FROM customer_coin c_c
                    INNER JOIN customer cm 
                    ON c_c.id_customer =  cm.id
                    INNER JOIN coin c
                    ON c_c.id_coin = c.id;
                    """)
                    user_info = cursor.fetchall()
                    # cursor.close()
            finally:
                if connection is not None:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            for i in range(len(user_info)):
                print(i)
                print("I AM WORKING DON'T WORRY")
                if user_info[i][6] == True and user_info[i][7] == False:
                    if crypto_price.check_crypto_price(user_info[i][2]) > user_info[i][4]:
                        send_message(chat_id=user_info[i][5],
                            msg=f"Your set price of {user_info[i][2].capitalize()} is {user_info[i][4]} "
                            f"lower than the current price {crypto_price.check_crypto_price(user_info[i][2])}")
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
                                cursor.execute("""
                                UPDATE customer_coin SET notified_or_not = true WHERE note_id = %s
                                """, [user_info[i][0]])
                                cursor.close()
                                print("[INFO] PostgreSQL connection closed")
                        except Exception as _ex:
                            print("[INFO] Error while working with PostgreSQL", _ex)
                        finally:
                            if connection is not None:
                                connection.close()
                                print("[INFO] PostgreSQL connection closed")
                        
                elif user_info[i][6] == False and user_info[i][7] == False:
                    if crypto_price.check_crypto_price(user_info[i][2]) < user_info[i][4]:
                        send_message(chat_id=user_info[i][5],
                            msg=f"Your set price of {user_info[i][2].capitalize()} is {user_info[i][4]} "
                            f"higher than the current price: {crypto_price.check_crypto_price(user_info[i][2])}")
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
                                cursor.execute("""
                                UPDATE customer_coin SET notified_or_not = true WHERE note_id = %s
                                """, [user_info[i][0]])
                        except Exception as _ex:
                            print("[INFO] Error while working with PostgreSQL", _ex)
                        finally:
                            if connection is not None:
                                connection.close()
                                print("[INFO] PostgreSQL connection closed")
                                                    
            time.sleep(10)                         

# fancy way to activate the main() function
if __name__ == '__main__':
    main()
