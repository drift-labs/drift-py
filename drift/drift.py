from pathlib import Path
import asyncio
import json
from solana.publickey import PublicKey
from anchorpy import Idl, Program, Provider
import anchorpy
import os
import pandas as pd
import numpy as np
import datetime

from .chmath import calculate_mark_price

IDL_FILE = "drift-py/drift/clearing_house.json"

# program and state account of clearing house program
CH_PID = "dammHkt7jmytvbS3nHTxQNEcP59aE57nxwV21YdqEDN"
CH_SID = "FExhvPycCCwYnZGeDsVtLhpEQ3yEkVY2k1HuPyfLj91L"

MARKET_INDEX_TO_PERP = {
    0: "SOL-PERP",
    1: "BTC-PERP",
    2: "ETH-PERP",
    3: "LUNA-PERP",
    4: "AVAX-PERP",
    5: "BNB-PERP",
    6: "MATIC-PERP",
    7: "ATOM-PERP",
}


def load_config():
    # todo
    if os.path.exists("config.txt"):
        return pd.read_csv("config.txt", header=None).values[0][0]
    else:
        return ""


def load_provider():
    # todo
    if os.path.exists("config.txt"):
        return pd.read_csv("config.txt", header=None).values[1][0]
    else:
        return "https://api.mainnet-beta.solana.com/"


os.environ["ANCHOR_PROVIDER_URL"] = load_provider()


class Drift:
    def __init__(self, USER_AUTHORITY=None):
        # Read the generated IDL.
        idl_f = IDL_FILE
        if not os.path.exists(idl_f):
            idl_f = "/".join(idl_f.split("/")[1:])
            print(idl_f)

        with Path(idl_f).open() as f:
            raw_idl = json.load(f)

        self.idl = Idl.from_json(raw_idl)

        # Address of the deployed program.
        self.program_id = PublicKey(CH_PID)
        self.USER_AUTHORITY = USER_AUTHORITY
        self.last_update = None

    async def open_position(self):
        # Execute the RPC.
        program = Program(self.idl, self.program_id, Provider.env())
        await program.rpc["initialize"]()

    async def load(self):
        # Generate the program client from IDL.
        # print(self.idl, self.program_id, Provider.env())
        program = Program(self.idl, self.program_id, Provider.env())

        program_state_id = PublicKey(CH_SID)

        # print('Drift program accounts:', program.account.keys())
        bot_position = None
        all_users = None
        all_users = await program.account["User"].all()

        # try:
        #     if self.USER_AUTHORITY:
        #         for user in all_users:
        #             user_data = user["account"]["data"]
        #             if str(user_data.authority) == self.USER_AUTHORITY:
        #                 # print(user_data.totalTokenDiscount/1e6)
        #                 bot_position = await program.account["UserPositions"].fetch(
        #                     user_data.positions
        #                 )
        # except:
        #     pass

        account = await program.account["State"].fetch(program_state_id)
        mkt_account = await program.account["Markets"].fetch(account.markets)
        await program.close()

        self.state_account = account

        self.mkt_account = mkt_account
        self.all_users = all_users
        self.bot_position = bot_position

        self.last_update = datetime.datetime.utcnow()

    async def load_account(self, key, pubkey):
        # Generate the program client from IDL.
        program = Program(self.idl, self.program_id, Provider.env())
        account = await program.account[key].fetch(pubkey)
        await program.close()
        self.last_load = account
        return account

    async def load_history(self):
        history = {
            "deposit": await self.load_account(
                "DepositHistory", self.state_account.deposit_history
            ),
            "trade": await self.load_account(
                "TradeHistory", self.state_account.trade_history
            ),
            "liquidation": await self.load_account(
                "LiquidationHistory", self.state_account.liquidation_history
            ),
            "fundingPayment": await self.load_account(
                "FundingPaymentHistory", self.state_account.funding_payment_history
            ),
            "fundingRate": await self.load_account(
                "FundingRateHistory", self.state_account.funding_rate_history
            ),
            "curve": await self.load_account(
                "CurveHistory", self.state_account.curve_history
            ),
        }

        return history

    async def load_history_df(self):
        history = await self.load_history()
        history_df = {}
        for key in history.keys():
            record_key = [x for x in dir(history[key]) if "_records" in x.lower()][0]
            df = pd.DataFrame(history[key].__dict__[record_key]).set_index("ts")
            # df = df[df['marketIndex']==0]
            df.index = (
                pd.to_datetime(df.index * 1000000000)
                .tz_localize("UTC")
                .tz_convert("US/Eastern")
            )
            history_df[key] = df
        return history_df

    def base_asset_imbalance(self, market_index=0):
        market_i = self.mkt_account.markets[market_index]
        return market_i.baseAssetAmount / 1e13

    def market_summary(self):
        market_cols = [
            "initialized",
            "base_asset_amount",
            "base_asset_amount_long",
            "base_asset_amount_short",
            "initialized",
            "open_interest",
        ]

        amm_cols = [
            # '_io',
            "oracle",
            # 'oracle_source',
            "base_asset_reserve",
            "quote_asset_reserve",
            # 'cumulativeRepegRebateLong',
            #    'cumulativeRepegRebateShort',
            "cumulative_funding_rate_long",
            "cumulative_funding_rate_short",
            "last_funding_rate",
            "last_funding_rate_ts",
            # 'funding_period',
            "last_oracle_price_twap",
            "last_mark_price_twap",
            "last_mark_price_twap_ts",
            "sqrt_k",
            "peg_multiplier",
            "total_fee",
            "total_fee_minus_distributions",
            "total_fee_withdrawn",
            # 'minimum_trade_size',
            # 'padding0', 'padding1', 'padding2', 'padding3', 'padding4'
        ]
        mdfs = []
        for marketIndex, marketName in MARKET_INDEX_TO_PERP.items():
            market_drift_account = self.mkt_account.markets[marketIndex]
            # print(market_drift_account))
            mdf = pd.Series(market_drift_account.__dict__)[market_cols]
            for x in [
                "base_asset_amount_long",
                "base_asset_amount_short",
                "base_asset_amount",
            ]:
                mdf[x] /= 1e13

            mdf.loc["market_index"] = marketIndex
            mdf.loc["market_name"] = marketName

            amm_drift_account = pd.Series(market_drift_account.amm.__dict__)
            # print(amm_drift_account.index)
            amm_drift_account = amm_drift_account[amm_cols]
            for x in ["base_asset_reserve", "quote_asset_reserve", "sqrt_k"]:
                amm_drift_account[x] /= 1e13
            for x in [
                "last_mark_price_twap_ts",
                "last_funding_rate_ts",
            ]:
                amm_drift_account[x] = pd.to_datetime(amm_drift_account[x] * 1e9)

            for x in [
                "total_fee",
                "total_fee_minus_distributions",
                "total_fee_withdrawn",
            ]:
                amm_drift_account[x] /= 1e6

            for x in ["peg_multiplier"]:
                amm_drift_account[x] /= 1e3

            for x in [
                "cumulative_funding_rate_long",
                "cumulative_funding_rate_short",
                "last_funding_rate",
            ]:
                amm_drift_account[x] /= 1e14

            for x in ["last_mark_price_twap", "last_oracle_price_twap"]:
                amm_drift_account[x] /= 1e10

            mdf = mdf.append(amm_drift_account)

            markPrice = calculate_mark_price(
                amm_drift_account["base_asset_reserve"],
                amm_drift_account["quote_asset_reserve"],
                amm_drift_account["peg_multiplier"],
            )
            # print(markPrice)

            mdf.loc["mark_price"] = markPrice

            mdfs.append(mdf)

        return pd.concat(mdfs, axis=1)

    def user_summary(self):
        if self.all_users is None:
            return pd.DataFrame()
        users_df = pd.DataFrame([x.account.__dict__ for x in self.all_users])
        users_df["public_key"] = pd.Series([x.public_key for x in self.all_users])

        users_df["Address"] = users_df["authority"].astype(str)
        for field in [
            "cumulative_deposits",
            "total_fee_paid",
            "collateral",
            "total_token_discount",
        ]:
            users_df[field] = (users_df[field] / 1e6).round(3)
        user_summary_df = users_df[
            ["Address", "collateral", "cumulative_deposits", "total_fee_paid"]
        ].sort_values("total_fee_paid", ascending=False)

        # todo: calculate total collateral
        user_summary_df["realized_pnl"] = (
            user_summary_df["collateral"] - user_summary_df["cumulative_deposits"]
        ).round(3)

        # imperfect measure
        user_summary_df["~roi"] = (
            user_summary_df["realized_pnl"]
            / (user_summary_df["cumulative_deposits"]).clip(0, 1e10)
        ).round(3)

        return user_summary_df

    async def user_position_summary(self):
        # if self.all_users is None:
        #     return pd.DataFrame()

        program = Program(self.idl, self.program_id, Provider.env())
        all_user_positions = await program.account["UserPositions"].all()
        position_dfs= {}
        # return all_user_positions
        for position in all_user_positions:
            # print(position)
            position_df = pd.DataFrame([x.__dict__ for x in list(position.account.positions)])   

            if len(position_df):
                position_df = position_df[position_df.base_asset_amount != 0]

                for x in ["quote_asset_amount"]:
                    position_df[x] /= 1e6
                    position_df[x] = position_df[x].round(2)
                for x in ["base_asset_amount"]:
                    position_df[x] /= 1e13
                for x in ["last_cumulative_funding_rate"]:
                    position_df[x] /= 1e14

                position_df = position_df[
                    [
                        "market_index",
                        "quote_asset_amount",
                        "base_asset_amount",
                        "last_cumulative_funding_rate",
                    ]
                ]
                position_df['entry_price'] = (position_df['quote_asset_amount']/position_df['base_asset_amount']).abs()
                position_dfs[str(position.account.user)] = position_df


        # for x in ['markPriceAfter','markPriceBefore','oraclePrice']:
        #     trdf[x] /= 1e10

        res = pd.concat(position_dfs, axis=0)
        res.index.names = ['user_position_pubkey', 'position_index']
        res = res.reset_index()
        position_authority = pd.DataFrame([[x.public_key, x.account.authority] 
        for x in self.all_users], columns=['user_position_pubkey', 'user_authority']).astype(str)
        positions = position_authority.merge(res, how='outer')
        return positions

async def __main__():
    # asyncio.run(main()) # for python
    drift_client = Drift()
    await drift_client.load()  # for jupyter notebook
    account, all_users, bot_pos = (
        drift_client.mkt_account,
        drift_client.all_users,
        drift_client.bot_pos,
    )
