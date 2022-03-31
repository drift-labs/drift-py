from anchorpy import Idl, Program, Provider
from drift.drift import Drift
import pandas as pd


class ClearingHouseUser:
    """inspect user account values"""

    def __init__(self, drift, authority="BzSJ77zKaqtBk2cEL1XqFL97zTXXMRHmxtkgtXwCc3C"):
        self.authority = authority
        users_df = pd.DataFrame([x.account.__dict__ for x in drift.all_users])  # todo
        self.user_data = users_df[users_df.authority.astype(str) == self.authority]
        self.drift = drift

    def user_positions_account(self):
        user_data_positions = self.user_data["positions"].values[0]
        return user_data_positions

    def user_ch_account(self):
        user_data_positions = self.user_data["authority"].values[0]
        return user_data_positions

    async def positions(self):
        self.position = await self.drift.load_account(
            "UserPositions", self.user_positions_account()
        )
        position_df = pd.DataFrame(self.position.positions)
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

        # for x in ['markPriceAfter','markPriceBefore','oraclePrice']:
        #     trdf[x] /= 1e10

        return position_df


async def open_position(user, direction, amount, market_index):
    """
    todo: instruction index out of bounds
    """

    # direction = history_df['trade']['direction'].values[0] #LONG
    # amount = int(1e6) #($1)
    # market_index = 0 #(SOL)

    accounts = {
        "state": CH_SID,
        "user": user.user_ch_account(),
        "authority": user.authority,
        "markets": drift.state_account.markets,
        "userPositions": user.user_positions_account(),
        "tradeHistory": drift.state_account.trade_history,
        "fundingPaymentHistory": drift.state_account.funding_payment_history,
        "fundingRateHistory": drift.state_account.funding_rate_history,
        "oracle": drift.mkt_account.markets[0].amm.oracle,
    }

    open_position_context = Context(accounts)

    openPositionInstr = program.rpc["openPosition"]
    optional_accounts = {
        "discountToken": False,
        "referrer": False,
    }

    await openPositionInstr(
        direction,
        amount,
        market_index,
        0,
        optional_accounts,
        ctx=Context(accounts, options=opts1),
    )


if __name__ == "__main__":
    # todo
    CH_PID = "dammHkt7jmytvbS3nHTxQNEcP59aE57nxwV21YdqEDN"
    CH_SID = "FExhvPycCCwYnZGeDsVtLhpEQ3yEkVY2k1HuPyfLj91L"
    BOT_AUTHORITY = "BzSJ77zKaqtBk2cEL1XqFL97zTXXMRHmxtkgtXwCc3C"
    user = ClearingHouseUser(BOT_AUTHORITY)
    open_position(user)
