from pathlib import Path
import asyncio
import json
from solana.publickey import PublicKey
from anchorpy import Idl, Program, Provider
import anchorpy
import os
import pandas as pd
import numpy as np

from .chmath import calculate_mark_price

IDL_FILE = './drift/clearing_house.json'

# program and state account of clearing house program
CH_PID = 'dammHkt7jmytvbS3nHTxQNEcP59aE57nxwV21YdqEDN'
CH_SID = 'FExhvPycCCwYnZGeDsVtLhpEQ3yEkVY2k1HuPyfLj91L'

MARKET_INDEX_TO_PERP = {0:'SOL-PERP',
                       1:'BTC-PERP',
                       2:'ETH-PERP',
                      }

def load_config():
    #todo
    if os.path.exists('config.txt'):
        return pd.read_csv('config.txt', header=None).values[0][0]
    else:
        return ''

def load_provider():
    #todo
    if os.path.exists('config.txt'):
        return pd.read_csv('config.txt', header=None).values[1][0]
    else:
        return 'https://api.mainnet-beta.solana.com/'

os.environ['ANCHOR_PROVIDER_URL'] = load_provider()

    
class Drift:
    def __init__(self, USER_AUTHORITY=None):
        # Read the generated IDL.
        with Path(IDL_FILE).open() as f:
            raw_idl = json.load(f)
        self.idl = Idl.from_json(raw_idl)

        # Address of the deployed program.
        self.program_id = PublicKey(CH_PID)
        self.USER_AUTHORITY = USER_AUTHORITY

        
    async def open_position(self):
        # Execute the RPC.
        program = Program(self.idl, self.program_id, Provider.env())
        await program.rpc["initialize"]()
        
    async def load(self):
        # Generate the program client from IDL.
        program = Program(self.idl, self.program_id, Provider.env())
                
        program_state_id = PublicKey(CH_SID)
        
        # print('Drift program accounts:', program.account.keys())
        all_users = await program.account['User'].all()
        bot_position = None

        if self.USER_AUTHORITY:
            for user in all_users:
                user_data = user['account']['data']
                if str(user_data.authority) == self.USER_AUTHORITY:
                    # print(user_data.totalTokenDiscount/1e6)
                    bot_position = await program.account['UserPositions'].fetch(user_data.positions)

        account = await program.account['State'].fetch(program_state_id)
        mkt_account = await program.account['Markets'].fetch(account.markets)
        await program.close()        

        self.state_account = account
        
        self.mkt_account = mkt_account
        self.all_users = all_users
        self.bot_position = bot_position 

    async def load_account(self, key, pubkey):
        # Generate the program client from IDL.
        program = Program(self.idl, self.program_id, Provider.env())  
        account = await program.account[key].fetch(pubkey)
        await program.close()        
        self.last_load = account
        return account
    
    async def load_history(self):
        history = {
            'deposit': await self.load_account('DepositHistory', self.state_account.depositHistory),
            'trade': await self.load_account('TradeHistory', self.state_account.tradeHistory),
            'liquidation': await self.load_account('LiquidationHistory', self.state_account.liquidationHistory),
            'fundingPayment': await self.load_account('FundingPaymentHistory', self.state_account.fundingPaymentHistory),
            'fundingRate': await self.load_account('FundingRateHistory', self.state_account.fundingRateHistory),
            'curve': await self.load_account('CurveHistory', self.state_account.curveHistory)
        }

        return history
    
    async def load_history_df(self):
        history = await self.load_history()
        history_df = {}
        for key in history.keys():
            record_key = [x for x in history[key].keys() if 'records' in x.lower()][0]
            df = pd.DataFrame(history[key][record_key]).set_index('ts')
            # df = df[df['marketIndex']==0]
            df.index = pd.to_datetime(df.index*1000000000).tz_localize('UTC').tz_convert('US/Eastern')
            history_df[key] = df
        return history_df

    def base_asset_imbalance(self, market_index=0):
        market_i = self.mkt_account.markets[market_index]
        return market_i.baseAssetAmount/1e13
    
    def market_summary(self):
        market_cols = ['initialized', 
               'baseAssetAmountLong', 'baseAssetAmountShort', 'baseAssetAmount', 
               'openInterest']

        amm_cols = [
            # '_io',
            'oracle',
            # 'oracleSource',
            'baseAssetReserve',
               'quoteAssetReserve', 
            # 'cumulativeRepegRebateLong',
            #    'cumulativeRepegRebateShort',
            'cumulativeFundingRateLong',
               'cumulativeFundingRateShort',
            'lastFundingRate', 'lastFundingRateTs',
               # 'fundingPeriod', 
            'lastOracleMarkSpreadTwap', 'lastMarkPriceTwap',
               'lastMarkPriceTwapTs', 
            'sqrtK', 'pegMultiplier', 
            'totalFee',
               'totalFeeMinusDistributions', 'totalFeeWithdrawn',
            # 'minimumTradeSize',
               # 'padding0', 'padding1', 'padding2', 'padding3', 'padding4'
        ]
        mdfs = []
        for marketIndex, marketName in MARKET_INDEX_TO_PERP.items():
            market_drift_account = self.mkt_account['markets'][marketIndex]
            mdf = pd.Series(market_drift_account)[market_cols]
            for x in ['baseAssetAmountLong', 'baseAssetAmountShort', 'baseAssetAmount']:
                mdf[x] /= 1e13

            mdf.loc['marketIndex'] = marketIndex
            mdf.loc['marketName'] = marketName

            amm_drift_account = pd.Series(market_drift_account.amm)
            # print(amm_drift_account.index)
            amm_drift_account = amm_drift_account[amm_cols]
            for x in ['baseAssetReserve', 'quoteAssetReserve', 'sqrtK']:
                amm_drift_account[x] /= 1e13

            for x in ['totalFee', 'totalFeeMinusDistributions', 'totalFeeWithdrawn']:
                amm_drift_account[x] /= 1e6

            for x in ['pegMultiplier']:
                amm_drift_account[x] /= 1e3

            for x in ['cumulativeFundingRateLong', 'cumulativeFundingRateShort', 'lastFundingRate']:
                amm_drift_account[x] /= 1e14

            for x in ['lastMarkPriceTwap']:
                amm_drift_account[x] /= 1e10

            mdf = mdf.append(amm_drift_account)
            
            markPrice = calculate_mark_price(amm_drift_account['baseAssetReserve'],
                                                        amm_drift_account['quoteAssetReserve'],
                                                        amm_drift_account['pegMultiplier'],
                                                       )
            print(markPrice)
            
            mdf.loc['markPrice'] = markPrice

            mdfs.append(mdf)
            

        return pd.concat(mdfs, axis=1)
    
async def __main__():
    # asyncio.run(main()) # for python 
    drift_client = Drift()
    await drift_client.load() # for jupyter notebook
    account, all_users, bot_pos = drift_client.mkt_account, drift_client.all_users, drift_client.bot_pos,

