import requests
import time
import sqlite3
import crypto_price



bot_token = 'api_telegram_bot_api'


def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)



def main():
    sqlite_connection = sqlite3.connect('customer.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    sqlite_select_query = """SELECT c_c.note_id, cm.customer_name, c.coin_name, c_c.price_coin, cm.id, up_or_down_price
    FROM CUSTOMER_COIN c_c, CUSTOMER cm, COIN c
    WHERE c_c.id_customer = cm.id and c_c.id_coin = c.id """
    cursor.execute(sqlite_select_query)
    user_info = cursor.fetchall()
    #### ЗАПИСЫВАЕМ ЗНАЧЕНИЯ ИЗ ТАБЛИЦЫ
    #### ДАННЫЕ ИЗ ТАБЛИЦЫ ПЕРЕПИСЫВАЮТСЯ В TEXT
    #### МЫ ПРИ ПОМОЩИ ЦИКЛА ПЕРЕПИСЫВАЕМ В ПЕРЕМЕННУЮ a
    cursor.close()
    print(user_info)

    while True:
        time.sleep(1000)
        for i in range(len(user_info)):
            if user_info[i][2] == 'bitcoin' and user_info[i][5] == 1:
                if crypto_price.check_btc_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                    msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                        f"lower than the current price {crypto_price.check_btc_price()}")
            if user_info[i][2] == 'bitcoin' and user_info[i][5] == 0:
                if crypto_price.check_btc_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_btc_price()}")
            if user_info[i][2] == 'ethereum' and user_info[i][5] == 1:
                if crypto_price.check_eth_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                    msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                        f"lower than the current price {crypto_price.check_eth_price()}")
            if user_info[i][2] == 'ethereum' and user_info[i][5] == 0:
                if crypto_price.check_eth_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_eth_price()}")
            if user_info[i][2] == 'binancecoin' and user_info[i][5] == 1:
                if crypto_price.check_bnb_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_bnb_price()}")
            if user_info[i][2] == 'binancecoin' and user_info[i][5] == 0:
                if crypto_price.check_bnb_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_bnb_price()}")

            if user_info[i][2] == 'litecoin' and user_info[i][5] == 1:
                if crypto_price.check_litecoin_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_litecoin_price()}")
            if user_info[i][2] == 'litecoin' and user_info[i][5] == 0:
                if crypto_price.check_litecoin_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_litecoin_price()}")

            if user_info[i][2] == 'solana' and user_info[i][5] == 1:
                if crypto_price.check_solana_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_solana_price()}")
            if user_info[i][2] == 'solana' and user_info[i][5] == 0:
                if crypto_price.check_litecoin_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_solana_price()}")

            if user_info[i][2] == 'avalanche' and user_info[i][5] == 1:
                if crypto_price.check_avalanche_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_avalanche_price()}")
            if user_info[i][2] == 'avalanche' and user_info[i][5] == 0:
                if crypto_price.check_litecoin_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_avalanche_price()}")

            if user_info[i][2] == 'terra-luna' and user_info[i][5] == 1:
                if crypto_price.ccheck_terra_luna_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_terra_luna_price()}")
            if user_info[i][2] == 'terra-luna' and user_info[i][5] == 0:
                if crypto_price.check_terra_luna_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_terra_luna_price()}")

            if user_info[i][2] == 'ftx-token' and user_info[i][5] == 1:
                if crypto_price.check_ftx_token_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_ftx_token_price()}")

            if user_info[i][2] == 'ftx-token' and user_info[i][5] == 0:
                if crypto_price.check_ftx_token_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_ftx_token_price()}")

            if user_info[i][2] == 'polkadot' and user_info[i][5] == 1:
                if crypto_price.check_polkadot_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_polkadot_price()}")

            if user_info[i][2] == 'polkadot' and user_info[i][5] == 0:
                if crypto_price.check_polkadot_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_polkadot_price()}")

            if user_info[i][2] == 'near' and user_info[i][5] == 1:
                if crypto_price.check_near_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_near_price()}")

            if user_info[i][2] == 'near' and user_info[i][5] == 0:
                if crypto_price.check_near_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_polkadot_price()}")


            if user_info[i][2] == 'uniswap' and user_info[i][5] == 1:
                if crypto_price.check_uniswap_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_uniswap_price()}")

            if user_info[i][2] == 'uniswap' and user_info[i][5] == 0:
                if crypto_price.check_uniswap_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_uniswap_price()}")

            if user_info[i][2] == 'matic-network' and user_info[i][5] == 1:
                if crypto_price.check_polygon_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_polygon_price()}")

            if user_info[i][2] == 'matic-network' and user_info[i][5] == 0:
                if crypto_price.check_polygon_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_polygon_price()}")

            if user_info[i][2] == 'cardano' and user_info[i][5] == 1:
                if crypto_price.check_ada_price() > user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price of {user_info[i][2]} is {user_info[i][3]} "
                                     f"lower than the current price {crypto_price.check_ada_price()}")

            if user_info[i][2] == 'cardano' and user_info[i][5] == 0:
                if crypto_price.check_ada_price() < user_info[i][3]:
                    send_message(chat_id=user_info[i][4],
                                 msg=f"Your set price is {user_info[i][3]} "
                                     f"higher than the current price: {crypto_price.check_ada_price()}")



    #             crypto_price.check_btc_price()
    #             if crypto_price.check_btc_price() >= user_info[i][3]:
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_btc_price()}$ higher than your set price: {user_info[i][3]}$')
    #             if crypto_price.check_btc_price() <= user_info[i][3]:
    #                 send_message(chat_id=user_info[i][4], msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_btc_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'ethereum':
    #             crypto_price.check_eth_price()
    #             if user_info[i][3] <= crypto_price.check_eth_price():
    #                 send_message(chat_id=user_info[i][4], msg = f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_eth_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_eth_price():
    #                 send_message(chat_id=user_info[i][4], msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_eth_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'binancecoin':
    #             crypto_price.check_bnb_price()
    #             if user_info[i][3] <= crypto_price.check_bnb_price():
    #                 send_message(chat_id=user_info[i][4], msg = f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_bnb_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_bnb_price():
    #                 send_message(chat_id=user_info[i][4], msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_bnb_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'litecoin':
    #             crypto_price.check_litecoin_price()
    #             if user_info[i][3] <= crypto_price.check_litecoin_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_litecoin_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_litecoin_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_litecoin_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'solana':
    #             crypto_price.check_solana_price()
    #             if user_info[i][3] <= crypto_price.check_solana_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_solana_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_solana_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_solana_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'avalanche-2':
    #             crypto_price.check_avalanche_price()
    #             if user_info[i][3] <= crypto_price.check_avalanche_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_avalanche_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_avalanche_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_avalanche_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'terra-luna':
    #             crypto_price.check_terra_luna_price()
    #             if user_info[i][3] <= crypto_price.check_terra_luna_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_terra_luna_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_terra_luna_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_terra_luna_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'ftx-token':
    #             crypto_price.check_ftx_token_price()
    #             if user_info[i][3] <= crypto_price.check_ftx_token_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_ftx_token_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_ftx_token_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_ftx_token_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'polkadot':
    #             crypto_price.check_polkadot_price()
    #             if user_info[i][3] <= crypto_price.check_polkadot_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_polkadot_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_polkadot_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_polkadot_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'near':
    #             crypto_price.check_near_price()
    #             if user_info[i][3] <= crypto_price.check_near_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_near_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_near_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_near_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'uniswap':
    #             crypto_price.check_uniswap_price()
    #             if user_info[i][3] <= crypto_price.check_uniswap_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_uniswap_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_uniswap_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_uniswap_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'matic-network':
    #             crypto_price.check_polygon_price()
    #             if user_info[i][3] <= crypto_price.check_polygon_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_polygon_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_polygon_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_polygon_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'cardano':
    #             crypto_price.check_ada_price()
    #             if user_info[i][3] <= crypto_price.check_ada_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_ada_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_ada_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_ada_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'the-graph':
    #             crypto_price.check_the_graph_price()
    #             if user_info[i][3] <= crypto_price.check_the_graph_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_the_graph_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_the_graph_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_the_graph_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         elif user_info[i][2] == 'dogecoin':
    #             crypto_price.check_dogecoin_price()
    #             if user_info[i][3] <= crypto_price.check_dogecoin_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_dogecoin_price()}$ higher than your set price: {user_info[i][3]}$')
    #                 print('yes')
    #             elif user_info[i][3] >= crypto_price.check_dogecoin_price():
    #                 send_message(chat_id=user_info[i][4],
    #                              msg=f'The current price of your crypto {user_info[i][2]} is {crypto_price.check_dogecoin_price()}$ lower than your set price: {user_info[i][3]}$')
    #                 print('no')
    #         # time.sleep(60)



# fancy way to activate the main() function
if __name__ == '__main__':
    main()

