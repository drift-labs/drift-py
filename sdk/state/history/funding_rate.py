"""This module models a funding-rate-history buffer account."""
from construct import Int64ul, Int64sl, Struct, Container, Padding
from typing import List
from solana.publickey import PublicKey
from sdk.layouts import Int128ul, Int128sl
from sdk.state.core import ElementCore
from sdk.state.history.core import HistoryCore


class FundingRateRecord(ElementCore):
    """Object to model a single-funding-rate-record."""
    layout = Struct(
        'ts' / Int64sl,
        'record_id' / Int128ul,
        'market_index' / Int64ul,
        'funding_rate' / Int128sl,
        'cumulative_funding_rate_long' / Int128sl,
        'cumulative_funding_rate_short' / Int128sl,
        'oracle_price_twap' / Int128sl,
        'mark_price_twap' / Int128ul
    )

    def __init__(
            self, ts: int, record_id: int, user_authority: PublicKey, user: PublicKey, market_index: int,
            funding_payment: int, base_asset_amount: int, user_last_cumulative_funding: int,
            user_last_funding_rate_ts: int, amm_cumulative_funding_long: int,
            amm_cumulative_funding_short: int
    ) -> None:
        self.ts = ts
        self.record_id = record_id
        self.user_authority = user_authority
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
        """Create a funding-rate record from a container."""
        funding_rate_record = cls(
            ts=container.ts,
            record_id=container.record_id,
            user_authority=container.user_authority,
            user=container.user,
            market_index=container.market_index,
            funding_payment=container.funding_payment,
            base_asset_amount=contianer.base_asset_amount,
            user_last_cumulative_funding=container.user_last_cumulative_funding,
            user_last_funding_rate_ts=container.user_last_funding_rate_ts,
            amm_cumulative_funding_long=container.amm_cumulative_funding_long,
            amm_cumulative_funding_short=container.amm_cumulative_funding_short
        )
        return funding_rate_record

    def to_dict(self) -> dict:
        """For pretty printing."""
        my_dict = {
            'ts': self.ts,
            'record_id': self.record_id,
            'user_authority': self.user_authority.__str__(),
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


class FundingRateHistory(HistoryCore):
    """Object to model a funding-rate-history buffer account."""
    layout = Struct(
        Padding(8),
        'head' / Int64ul,
        'records' / FundingRateRecord.layout[1024]
    )

    def __init__(self, head: int, records: List[FundingRateRecord]) -> None:
        self.head = head
        self.records = records

    @classmethod
    def from_container(cls, container: Container):
        """Create a funding-rate-history account from a container."""
        history = cls(
            head=container.head,
            records=[FundingRateRecord.from_container(c) for c in container.records]
        )
        return history
