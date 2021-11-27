from construct import Int8ul, Int64ul, Int64sl, Struct, Container, Flag, Padding
from typing import List
from solana.publickey import PublicKey
from drift.layouts import Int128ul, Int128sl, PUBLIC_KEY_LAYOUT
from drift.state.core import ElementCore
from drift.state.history.core import HistoryCore

class TradeRecord(ElementCore):
    layout = Struct(
        'ts' / Int64sl,
        'record_id' / Int128ul,
        'user_authority' / PUBLIC_KEY_LAYOUT,
        'user' / PUBLIC_KEY_LAYOUT,
        'direction' / Int8ul,
        'base_asset_amount' / Int128ul,
        'quote_asset_amount' / Int128ul,
        'mark_price_before' / Int128ul,
        'mark_price_after' / Int128ul,
        'fee' / Int128ul,
        'referrer_discount' / Int128ul,
        'referee_reward' / Int128ul,
        'token_discount' / Int128ul,
        'liquidation' / Flag,
        'market_index' / Int64ul,
        'oracle_price' / Int128sl
    )

    def __init__(self, ts: int, record_id: int, user_authority: PublicKey, user: PublicKey, direction: int,
                 base_asset_amount: int, quote_asset_amount: int, mark_price_before: int, mark_price_after: int,
                 fee: int, referrer_discount: int, referee_reward: int, token_discount: int, liquidation: bool,
                 market_index: int, oracle_price: int) -> None:
        self.ts = ts
        self.record_id = record_id
        self.user_authority = user_authority
        self.user = user
        self.direction = direction
        self.base_asset_amount = base_asset_amount
        self.quote_asset_amount = quote_asset_amount
        self.mark_price_before = mark_price_before
        self.mark_price_after = mark_price_after
        self.fee = fee
        self.referrer_discount = referrer_discount
        self.referee_reward = referee_reward
        self.token_discount = token_discount
        self.liquidation = liquidation
        self.market_index = market_index
        self.oracle_price = oracle_price

    @classmethod
    def from_container(cls, container: Container):
        trade_record = cls(
            ts=container.ts,
            record_id=container.record_id,
            user_authority=PublicKey(container.user_authority),
            user=PublicKey(container.user),
            direction=container.direction,
            base_asset_amount=container.base_asset_amount,
            quote_asset_amount=container.quote_asset_amount,
            mark_price_before=container.mark_price_before,
            mark_price_after=container.mark_price_after,
            fee=container.fee,
            referrer_discount=container.referrer_discount,
            referee_reward=container.referee_reward,
            token_discount=container.token_discount,
            liquidation=container.liquidation,
            market_index=container.market_index,
            oracle_price=container.oracle_price
        )
        return trade_record

    def to_dict(self) -> dict:
        my_dict = {
            'ts': self.ts,
            'record_id': self.record_id,
            'user_authority': self.user_authority.__str__(),
            'user': self.user.__str__(),
            'direction': self.direction,
            'base_asset_amount': self.base_asset_amount,
            'quote_asset_amount': self.quote_asset_amount,
            'mark_price_before': self.mark_price_before,
            'mark_price_after': self.mark_price_after,
            'fee': self.fee,
            'referrer_discount': self.referrer_discount,
            'referee_reward': self.referee_reward,
            'token_discount': self.token_discount,
            'liquidation': self.liquidation,
            'market_index': self.market_index,
            'oracle_price': self.oracle_price
        }
        return my_dict


class TradeHistory(HistoryCore):
    layout = Struct(
        Padding(8),
        'head' / Int64ul,
        'records' / TradeRecord.layout[1024]
    )

    def __init__(self, head: int, records: List[TradeRecord]) -> None:
        self.head = head
        self.records = records

    @classmethod
    def from_container(cls, container: Container):
        history = cls(
            head=container.head,
            records=[TradeRecord.from_container(c) for c in container.records]
        )
        return history