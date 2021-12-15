"""This module models a funding-payment-history buffer account."""
from construct import Int64ul, Int64sl, Struct, Container, Padding
from typing import List
from solana.publickey import PublicKey
from sdk.layouts import Int128ul, Int128sl, PUBLIC_KEY_LAYOUT
from sdk.state.core import ElementCore
from sdk.state.history.core import HistoryCore


class FundingPaymentRecord(ElementCore):
    """Object to model a single funding-payment record."""
    layout = Struct(
        'ts' / Int64sl,
        'record_id' / Int128ul,
        'user' / PUBLIC_KEY_LAYOUT,
        'market_index' / Int64ul,
        'funding_payment' / Int128sl,
        'base_asset_amount' / Int128sl,
        'user_last_cumulative_funding' / Int128ul,
        'user_last_funding_rate_ts' / Int64sl,
        'amm_cumulative_funding_long' / Int128sl,
        'amm_cumulative_funding_short' / Int128sl
    )

    def __init__(
            self, ts: int, record_id: int, user: PublicKey, market_index: int, funding_payment: int,
            base_asset_amount: int, user_last_cumulative_funding: int, user_last_funding_rate_ts: int,
            amm_cumulative_funding_long: int, amm_cumulative_funding_short: int
    ) -> None:
        self.ts = ts
        self.record_id = record_id
        self.user = user
        self.market_index = market_index
        self.funding_payment = funding_payment
        self.base_asset_amount = base_asset_amount
        self.user_last_cumulative_funding = user_last_cumulative_funding
        self.user_last_funding_rate_ts = user_last_funding_rate_ts
        self.amm_cumulative_funding_long = amm_cumulative_funding_long
        self.amm_cumulative_funding_short = amm_cumulative_funding_short

    @classmethod
    def from_container(cls, container: Container):
        """Create a funding-payment record from a container."""
        funding_payment_record = cls(
            ts=container.ts,
            record_id=container.record_id,
            user=container.user,
            market_index=container.market_index,
            funding_payment=container.funding_payment,
            base_asset_amount=container.base_asset_amount,
            user_last_cumulative_funding=container.user_last_cumulative_funding,
            user_last_funding_rate_ts=container.user_last_funding_rate_ts,
            amm_cumulative_funding_long=container.amm_cumulative_funding_long,
            amm_cumulative_funding_short=container.amm_cumulative_funding_short
        )
        return funding_payment_record

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'ts': self.ts,
            'record_id': self.record_id,
            'user': self.user.__str__(),
            'market_index': self.market_index,
            'funding_payment': self.funding_payment,
            'base_asset_amount': self.base_asset_amount,
            'user_last_cumulative_funding': self.user_last_cumulative_funding,
            'user_last_funding_rate_ts': self.user_last_funding_rate_ts,
            'amm_cumulative_funding_long': self.amm_cumulative_funding_long,
            'amm_cumulative_funding_short': self.amm_cumulative_funding_short
        }
        return my_dict


class FundingPaymentHistory(HistoryCore):
    """Object to model a funding-payment-history buffer account."""
    layout = Struct(
        Padding(8),
        'head' / Int64ul,
        'records' / FundingPaymentRecord.layout[1024]
    )

    def __init__(self, head: int, records: List[FundingPaymentRecord]) -> None:
        self.head = head
        self.records = records

    @classmethod
    def from_container(cls, container: Container):
        """Create a funding-payment-history account from a container."""
        history = cls(
            head=container.head,
            records=[FundingPaymentRecord.from_container(c) for c in container.records]
        )
        return history
