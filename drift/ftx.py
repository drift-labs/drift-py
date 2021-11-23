import ccxt
import pandas as pd
import time
import os

# pd.options.plotting.backend = "plotly"

#store ftx secret json in ~/.ftx
import json
FTX_SECRET = None
with open(os.path.expanduser('~/.ftx'), 'r') as f:
    FTX_SECRET = json.load(f)

ftx = ccxt.ftx(FTX_SECRET)

MAX_LONG = 250
MAX_SHORT = 88

MIN_TRADE = 1

PASSIVE_SPREAD = .075
PATIENCE = 4


def ftx_trade_to_target_position(arb_amount, retry=PATIENCE):
    ''' have a target position, useful when holding a large OI'''
    if arb_amount > MAX_LONG:
        arb_amount = MAX_LONG
        
    if arb_amount < -MAX_SHORT:
        arb_amount = -MAX_SHORT
    
    positions = pd.DataFrame(ftx.fetch_positions())
    # print(positions.columns)
    positions[['symbol','notional',
               'unrealizedPnl','contracts',
               'markPrice', 'percentage', 'liquidationPrice',
               'side',
              ]]

    positions['contractsSide'] = (positions['side'].apply(lambda x: {'long':1, 'short':-1}[x]) * positions['contracts'])

    current_position = positions.set_index('symbol')['contractsSide'].loc['SOL-PERP']
    mark_price_now = positions.set_index('symbol')['markPrice'].loc['SOL-PERP']

    trade_size = round(arb_amount - current_position, 2)
    
    if abs(trade_size) < MIN_TRADE:
        print('skipping trade: too small:', trade_size)
        return
    elif trade_size > 0:
        ftx.cancelAllOrders()
        limit = mark_price_now - PASSIVE_SPREAD
        ftx.createLimitOrder('SOL-PERP', 'buy', abs(trade_size), limit)
    else:
        ftx.cancelAllOrders()
        limit = mark_price_now + PASSIVE_SPREAD
        ftx.createLimitOrder('SOL-PERP', 'sell', abs(trade_size), limit)

    print('ARBING', trade_size, '@', mark_price_now)

    def open_orders_df():
        return pd.DataFrame(ftx.fetch_open_orders()).dropna(how='all',axis=1)
    oo = open_orders_df()
    
    count = 0
    while len(oo) and count < retry:
        print('open order:', oo)
        time.sleep(3)
        oo = open_orders_df()
        count+=1
        
    ftx.cancelAllOrders()

    positions = pd.DataFrame(ftx.fetch_positions())
    # print(positions.columns)
    print(positions[['symbol','notional',
               'unrealizedPnl','contracts',
               'markPrice', 'percentage', 'liquidationPrice',
               'side',
              ]])

def recent_ftx_trades():
    mytrades = pd.DataFrame(ftx.fetch_my_trades())
    # print(mytrades.columns)
    mytrades = mytrades[['datetime', 'symbol', 'takerOrMaker', 'side', 'amount', 'price', 'cost', 'fee']]
    # print(mytrades.fee.values[-2])
    mytrades.fee = mytrades.fee.apply(lambda x: x['cost'])
    return mytrades.tail(10)