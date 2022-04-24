import psycopg2
import sys
from pycoingecko import CoinGeckoAPI
from sqlalchemy import create_engine
sys.path.insert(1, '/Users/constantion/Desktop/CRYPTO BOT/Crypto_bot_telegram')
import settings

# def create_coin_table():
try:
    connection = psycopg2.connect(
        host = settings.host,
        dbname = settings.db_name_2,
        user = settings.user,
        password = settings.password,
        port = settings.port_id
    )
    # Call IT one Time That's it
    connection.autocommit = True

    # CREATE DB
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE database users 
            """
        )

        print("[INFO] Db created successfully")

    # CREATE TABLE
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE coin(
                id smallserial PRIMARY KEY,
                coin_name varchar(75) NOT NULL,
                coin_market_id varchar(75) NOT NULL
            );
            """
        )

        print("[INFO] Table created successfully")

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE SGROUP(
                id smallint PRIMARY KEY,
                group_name VARCHAR(40)
            );
            """
        )
        print("[INFO] Table created successfully")

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE CUSTOMER(
                id integer PRIMARY KEY,
                id_group smallint,
                customer_name VARCHAR(75),
                FOREIGN KEY (id_group) REFERENCES SGROUP (id)
            );
            """
        )
        print("[INFO] Table created successfully")

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE CUSTOMER_COIN(
                note_id smallserial PRIMARY KEY,
                id_customer integer,
                id_coin smallint,
                price_coin real,
                up_or_down_price boolean,
                notified_or_not boolean,
                FOREIGN KEY(id_customer) REFERENCES CUSTOMER(id),
                FOREIGN KEY(id_coin)REFERENCES COIN(id)
            );
            """
        )

    print("[INFO] Table created successfully")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")