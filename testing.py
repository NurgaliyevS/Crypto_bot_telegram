# import asyncio
# from tabnanny import check
# import asyncpg
# from binance.client import Client
# import os
# import pandas as pd
# from pycoingecko import CoinGeckoAPI
# from aiohttp import web
# import psycopg2

# import settings

# cg = CoinGeckoAPI()


# # async def main():
# #     conn = await asyncpg.connect(f'postgresql://{settings.user}:{settings.password}@{settings.host}/{settings.db_name_2}')    
# #     name = "bitcoin"
# #     result = await conn.fetch("""
# #     SELECT id, coin_name, coin_market_id
# #     FROM coin
# #     WHERE lower(coin_name) = $1::varchar
# #     """, name)
# #     print(result)
# #     # Close the connection.
# #     await conn.close()

# async def get_coins_api_postgres():
#     conn = await asyncpg.connect(f'postgresql://{settings.user}:{settings.password}@{settings.host}/{settings.db_name}')
#     await conn.execute("TRUNCATE coins_info")
#     page = 0    
#     coin_market = cg.get_coins_markets(vs_currency='usd', per_page=250, page=page)
#     df_market = pd.DataFrame(coin_market,columns=['market_cap_rank','id','name','current_price',"price_change_24h","price_change_percentage_24h",'market_cap',"market_cap_change_percentage_24h",'total_volume',  "circulating_supply", "max_supply", "high_24h", "low_24h", ])
#     tuples = list(df_market.itertuples(index=False, name=None))
#     await conn.copy_records_to_table('coins_info', records=tuples, columns=list(df_market), timeout=10)
#     await conn.close()

# async def check_crypto_price(coin):
#     get_coins_api_postgres()
#     conn = await asyncpg.connect(f'postgresql://{settings.user}:{settings.password}@{settings.host}/{settings.db_name}')
#     res = await conn.fetch("""SELECT current_price
# 	            FROM coins_info
#                 WHERE lower(name) = $1::varchar OR id = $2::varchar;
#                 """, coin, coin)
#     await conn.close()
#     strings = [str(integer) for integer in res]
#     a_string = "".join(strings)
#     a_string = a_string.replace('<', '').replace('>','').replace('Record ','')
#     print(a_string)
#     return a_string

# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.gather(get_coins_api_postgres(), check_crypto_price('')))

# def check_crypto_price(coin):
#     try:
#         coin = coin.lower()
#         get_coins_api_postgres()
#         connection = psycopg2.connect(
#                 host = settings.host,
#                 database = settings.db_name,
#                 user = settings.user,
#                 password = settings.password,
#                 port = settings.port_id
#             )
#             # Call IT one Time That's it
#         connection.autocommit = True
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """SELECT current_price
# 	            FROM coins_info
#                 WHERE lower(name) = %s OR id = %s;
#                 """, [coin, coin ])
#             data = cursor.fetchone()
#             strings = [str(integer) for integer in data]
#             a_string = "".join(strings)
#             a_string = a_string.replace(',','').replace('(','').replace(')','')
#             res = float(a_string)
#             cursor.close()
#             return res

#     except Exception as _ex:
#             print("[INFO] Error while working with PostgreSQL", _ex)    

# async def handle(request):
#     """Handle incoming requests."""
#     pool = request.app['pool']
#     power = int(request.match_info.get('power', 10))

#     # Take a connection from the pool.
#     async with pool.acquire() as connection:
#         # Open a transaction.
#         async with connection.transaction():
#             # Run the query passing the request argument.
#             result = await connection.fetchval('select 2 ^ $1', power)
#             return web.Response(
#                 text="2 ^ {} is {}".format(power, result))


# async def init_app():
#     """Initialize the application server."""
#     app = web.Application()
#     # Create a database connection pool
#     app['pool'] = await asyncpg.create_pool(database='postgres',
#                                             user='postgres')
#     # Configure service routes
#     app.router.add_route('GET', '/{power:\d+}', handle)
#     app.router.add_route('GET', '/', handle)
#     return app


# loop = asyncio.get_event_loop()
# app = loop.run_until_complete(init_app())
# web.run_app(app)

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.gather(main()))