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
    engine = create_engine('postgresql+psycopg2://postgres:Kazakhstan01@localhost:5432/coins')
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
