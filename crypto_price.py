import requests
from binance.client import Client
import os
import account_setings
import sqlite3
import pandas as pd
from pycoingecko import CoinGeckoAPI

api_key = os.getenv('binance_api_key')
api_secret = os.getenv('binance_api_secret')

cg = CoinGeckoAPI()

# Authenticate with the client
client = Client(api_key, api_secret)

import psycopg2
import sys
import pandas as pd
from pycoingecko import CoinGeckoAPI
from sqlalchemy import create_engine
sys.path.insert(1, '/Users/constantion/Desktop/CRYPTO BOT/Crypto_bot_telegram')
import settings

cg = CoinGeckoAPI()

def get_coins_api_postgres():
    url = f'postgresql+psycopg2://{settings.user}:{settings.password}@{settings.host}/{settings.db_name}'
    page = 0
    coin_market = cg.get_coins_markets(vs_currency='usd', per_page=250, page=page)
    df_market = pd.DataFrame(coin_market, columns=['market_cap_rank','id','name','current_price',"price_change_24h","price_change_percentage_24h",'market_cap',"market_cap_change_percentage_24h",'total_volume',  "circulating_supply", "max_supply", "high_24h", "low_24h", ])
    engine = create_engine('postgresql+psycopg2://postgres:{}@localhost:5432/coins'.format(settings.password))
    df_market.to_sql('coins_info', engine, if_exists='replace')
    try: 
        engine.execute(
                        """ALTER TABLE coins_info 
                                ALTER COLUMN index TYPE smallint,
                                ALTER COLUMN market_cap_rank TYPE smallint,
                                ALTER COLUMN id TYPE VARCHAR(75),
                                ALTER COLUMN name TYPE VARCHAR(75),
                                ALTER COLUMN current_price TYPE real,
                                ALTER COLUMN price_change_percentage_24h TYPE real,
                                ALTER COLUMN market_cap_change_percentage_24h TYPE real,
                                ALTER COLUMN total_volume TYPE real,
                                ALTER COLUMN circulating_supply TYPE real,
                                ALTER COLUMN max_supply TYPE real,
                                ALTER COLUMN high_24h TYPE real,
                                ALTER COLUMN low_24h TYPE real;
                        """
                    )    
        print('ALL RIGHT MAN')
    except:
        print("Not good MAN")
    
def check_crypto_price(coin):
    try:
        coin = coin.lower()
        get_coins_api_postgres()
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
                """SELECT current_price
	            FROM coins_info
                WHERE lower(name) = %s OR id = %s;
                """, [coin, coin ])
            data = cursor.fetchone()
            strings = [str(integer) for integer in data]
            a_string = "".join(strings)
            a_string = a_string.replace(',','').replace('(','').replace(')','')
            res = float(a_string)
            cursor.close()
            return res

    except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
    # finally:
    #     if connection:
    #         connection.close()
    #         print("[INFO] PostgreSQL connection closed")