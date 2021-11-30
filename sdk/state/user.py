from construct import Struct, Padding, Container, Int64ul, Int64sl
from typing import List

from solana.publickey import PublicKey

from sdk.layouts import Int128ul, Int128sl, PUBLIC_KEY_LAYOUT
from sdk.state.core import ElementCore


class UserAccount(ElementCore):
    layout = Struct(
        Padding(8),
        'authority' / PUBLIC_KEY_LAYOUT,
        'collateral' / Int128ul,
        'cumulative_deposits' / Int128sl,
        'total_fee_paid' / Int128ul,
        'total_token_discount' / Int128ul,
        'total_referral_reward' / Int128ul,
        'total_referee_discount' / Int128ul,
        'positions_account' / PUBLIC_KEY_LAYOUT,
        Padding(64)
    )

    def __init__(self, authority: PublicKey, collateral: int, cumulative_deposits: int, total_fee_paid: int,
                 total_token_discount: int, total_referral_reward: int, total_referee_discount: int,
                 positions_account: PublicKey) -> None:
        self.authority = authority
        self.collateral = collateral
        self.cumulative_deposits = cumulative_deposits
        self.total_fee_paid = total_fee_paid
        self.total_token_discount = total_token_discount
        self.total_referral_reward = total_referral_reward
        self.total_referee_discount = total_referee_discount
        self.positions_account = positions_account

    def activate_precision(self):
        self.collateral = self.collateral / 1

    @classmethod
    def from_container(cls, container: Container):
        user_account = cls(
            authority=PublicKey(container.authority),
            collateral=container.collateral,
            cumulative_deposits=container.cumulative_deposits,
            total_fee_paid=container.total_fee_paid,
            total_token_discount=container.total_token_discount,
            total_referral_reward=container.total_referral_reward,
            total_referee_discount=container.total_referee_discount,
            positions_account=PublicKey(container.positions_account)
        )
        return user_account

    def to_dict(self) -> dict:
        my_dict = {
            'authority': self.authority.__str__(),
            'collateral': self.collateral,
            'cumulative_deposits': self.cumulative_deposits,
            'total_fee_paid': self.total_fee_paid,
            'total_token_discount': self.total_token_discount,
            'total_referral_reward': self.total_referral_reward,
            'total_referee_discount': self.total_referee_discount,
            'positions_account': self.positions_account.__str__()
        }
        return my_dict


class MarketPosition(ElementCore):
    layout = Struct(
        'market_index' / Int64ul,
        'base_asset_amount' / Int128sl,
        'quote_asset_amount' / Int128ul,
        'last_cumulative_funding_rate' / Int128sl,
        'last_cumulative_repeg_rebate' / Int128ul,
        'last_funding_rate_ts' / Int64sl,
        'stop_loss_price' / Int128ul,
        'stop_loss_amount' / Int128ul,
        'stop_profit_price' / Int128ul,
        'stop_profit_amount' / Int128ul,
        'transfer_to' / PUBLIC_KEY_LAYOUT,
        Padding(32)
    )

    def __init__(self, market_index: int, base_asset_amount: int, quote_asset_amount: int,
                 last_cumulative_funding_rate: int, last_cumulative_repeg_rebate: int, last_funding_rate_ts: int,
                 stop_loss_price: int, stop_loss_amount: int, stop_profit_price: int, stop_profit_amount: int,
                 transfer_to: PublicKey) -> None:
        self.market_index = market_index
        self.base_asset_amount = base_asset_amount
        self.quote_asset_amount = quote_asset_amount
        self.last_cumulative_funding_rate = last_cumulative_funding_rate
        self.last_cumulative_repeg_rebate = last_cumulative_repeg_rebate
        self.last_funding_rate_ts = last_funding_rate_ts
        self.stop_loss_price = stop_loss_price
        self.stop_loss_amount = stop_loss_amount
        self.stop_profit_price = stop_profit_price
        self.stop_profit_amount = stop_profit_amount
        self.transfer_to = transfer_to

    @classmethod
    def from_container(cls, container: Container):
        market_position = cls(
            market_index=container.market_index,
            base_asset_amount=container.base_asset_amount,
            quote_asset_amount=container.quote_asset_amount,
            last_cumulative_funding_rate=container.last_cumulative_funding_rate,
            last_cumulative_repeg_rebate=container.last_cumulative_repeg_rebate,
            last_funding_rate_ts=container.last_funding_rate_ts,
            stop_loss_price=container.stop_loss_price,
            stop_loss_amount=container.stop_loss_amount,
            stop_profit_price=container.stop_profit_price,
            stop_profit_amount=container.stop_profit_amount,
            transfer_to=PublicKey(container.transfer_to)
        )
        return market_position

    def to_dict(self) -> dict:
        my_dict = {
            'market_index': self.market_index,
            'base_asset_amount': self.base_asset_amount,
            'quote_asset_amount': self.quote_asset_amount,
            'last_cumulative_funding_rate' : self.last_cumulative_funding_rate,
            'last_cumulative_repeg_rebate': self.last_cumulative_repeg_rebate,
            'last_funding_rate_ts': self.last_funding_rate_ts,
            'stop_loss_price': self.stop_loss_price,
            'stop_loss_amount': self.stop_loss_amount,
            'stop_profit_price': self.stop_profit_price,
            'stop_profit_amount': self.stop_profit_amount,
            'transfer_to': self.transfer_to.__str__()
        }
        return my_dict


class UserPositions(ElementCore):
    layout = Struct(
        Padding(8),
        'user' / PUBLIC_KEY_LAYOUT,
        'positions' / MarketPosition.layout[5]
    )

    def __init__(self, user: PublicKey, positions: List[MarketPosition]) -> None:
        self.user = user
        self.positions = positions

    @classmethod
    def from_container(cls, container: Container):
        user_positions = cls(
            user=PublicKey(container.user),
            positions=[MarketPosition.from_container(c) for c in container.positions]
        )
        return user_positions

    def to_dict(self) -> dict:
        my_dict = {
            'user': self.user.__str__(),
            'positions': [position.to_dict() for position in self.positions]
        }
        return my_dict