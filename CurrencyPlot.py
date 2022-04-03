import matplotlib
import pandas as pd
import mplfinance as mpf
from matplotlib.pyplot import savefig
from pycoingecko import CoinGeckoAPI
import datetime

reformatted_data = dict()

def paint_plot(id_of_cur):

    currency = CoinGeckoAPI().get_coin_ohlc_by_id(id=id_of_cur, vs_currency='usd', days=7)

    reformatted_data['Date'] = []
    reformatted_data['Open'] = []
    reformatted_data['High'] = []
    reformatted_data['Low'] = []
    reformatted_data['Close'] = []
    for dict in currency:
        reformatted_data['Date'].append(datetime.datetime.fromtimestamp(dict[0]/1000))
        reformatted_data['Open'].append(dict[1])
        reformatted_data['High'].append(dict[2])
        reformatted_data['Low'].append(dict[3])
        reformatted_data['Close'].append(dict[4])

    pdata = pd.DataFrame.from_dict(reformatted_data)
    pdata.set_index('Date', inplace=True)
    mpf.plot(pdata, type='line', savefig='foo.png')

